"""
Arceus Phase 3: Tier 1 Faker-based Data Generator
Maps column types and name patterns to Faker providers.
Respects: types, nullability, max_length, numeric precision/scale, unique constraints.
Does NOT resolve FK values — that is Phase 4.
Flags unsupported column types visibly instead of guessing silently.
"""
from __future__ import annotations
import json
import random
import re
from faker import Faker
from schema_introspector import introspect
from dependency_graph import get_generation_order

fake = Faker()
Faker.seed(42)
random.seed(42)

# ---------- Name-pattern → Faker provider mapping (Tier 1) ----------

NAME_PATTERNS: dict[str, callable] = {
    r"(?i)^(first_?name)$": lambda: fake.first_name(),
    r"(?i)^(last_?name|surname)$": lambda: fake.last_name(),
    r"(?i)^(full_?name|name|user_?name|username)$": lambda: fake.name(),
    r"(?i)^(email|e_?mail)$": lambda: fake.email(),
    r"(?i)^(phone|phone_?number|mobile|tel)$": lambda: fake.phone_number(),
    r"(?i)^(address|street_?address)$": lambda: fake.address().replace("\n", ", "),
    r"(?i)^(city)$": lambda: fake.city(),
    r"(?i)^(state|province)$": lambda: fake.state(),
    r"(?i)^(country)$": lambda: fake.country(),
    r"(?i)^(zip|zip_?code|postal_?code)$": lambda: fake.zipcode(),
    r"(?i)^(company|company_?name|org|organization)$": lambda: fake.company(),
    r"(?i)^(url|website|homepage)$": lambda: fake.url(),
    r"(?i)^(description|bio|about|summary)$": lambda: fake.paragraph(nb_sentences=3),
    r"(?i)^(notes?|comment|remarks?)$": lambda: fake.sentence(),
    r"(?i)^(title|subject|headline)$": lambda: fake.sentence(nb_words=5),
    r"(?i)^(sku|product_?code|item_?code)$": lambda: fake.bothify("???-#####").upper(),
    r"(?i)^(status)$": lambda: random.choice(["active", "inactive", "pending"]),
    r"(?i)^(category|type|kind)$": lambda: random.choice(
        ["Electronics", "Books", "Clothing", "Home", "Sports", "Food", "Toys"]
    ),
    r"(?i)^(password|pass|pwd)$": lambda: fake.password(),
    r"(?i)^(ip|ip_?address)$": lambda: fake.ipv4(),
}


def match_name_pattern(column_name: str) -> callable | None:
    """Try to match a column name to a known Faker provider."""
    for pattern, provider in NAME_PATTERNS.items():
        if re.match(pattern, column_name):
            return provider
    return None


# ---------- Type-based fallback generators ----------

# Known type categories
SUPPORTED_TYPES = {
    "integer", "bigint", "smallint", "int4", "int8", "int2",
    "numeric", "decimal", "real", "double precision", "float4", "float8",
    "character varying", "varchar", "character", "char", "text",
    "boolean", "bool",
    "timestamp without time zone", "timestamp with time zone",
    "timestamp", "timestamptz",
    "date",
    "time without time zone", "time with time zone",
    "uuid",
    "json", "jsonb",
}


def generate_by_type(col: dict) -> any:
    """Generate a value based on column type metadata."""
    dtype = col["type"]
    udt = col["udt"]
    max_len = col["max_length"]
    precision = col["numeric_precision"]
    scale = col["numeric_scale"]

    # Integer types
    if udt in ("int4", "int2", "int8") or dtype in ("integer", "bigint", "smallint"):
        return random.randint(1, 10000)

    # Numeric/decimal
    if dtype in ("numeric", "decimal") or udt == "numeric":
        int_digits = (precision or 10) - (scale or 0)
        max_val = 10 ** int_digits - 1
        val = round(random.uniform(0.01, min(max_val, 99999)), scale or 2)
        return val

    # Float
    if dtype in ("real", "double precision") or udt in ("float4", "float8"):
        return round(random.uniform(0.01, 10000.0), 2)

    # Varchar / char
    if dtype in ("character varying", "character") or udt in ("varchar", "char"):
        text = fake.text(max_nb_chars=max(20, min(max_len or 50, 100)))
        if max_len:
            text = text[:max_len]
        return text

    # Text
    if dtype == "text" or udt == "text":
        return fake.paragraph(nb_sentences=2)

    # Boolean
    if dtype == "boolean" or udt == "bool":
        return random.choice([True, False])

    # Timestamp
    if "timestamp" in dtype or udt in ("timestamp", "timestamptz"):
        return fake.date_time_between(start_date="-2y", end_date="now").isoformat()

    # Date
    if dtype == "date":
        return fake.date_between(start_date="-2y", end_date="today").isoformat()

    # Time
    if "time" in dtype and "timestamp" not in dtype:
        return fake.time()

    # UUID
    if dtype == "uuid" or udt == "uuid":
        return str(fake.uuid4())

    # JSON/JSONB
    if dtype in ("json", "jsonb") or udt in ("json", "jsonb"):
        return {"key": fake.word(), "value": fake.word()}

    # UNSUPPORTED — flag it, don't guess
    return None


def is_serial(col: dict) -> bool:
    """Check if a column is auto-incrementing (serial/sequence)."""
    default = col.get("default") or ""
    return "nextval(" in default


def is_fk(col: dict, fk_columns: set) -> bool:
    """Check if this column is a foreign key."""
    return col["column"] in fk_columns


def generate_table_data(
    table_name: str,
    columns: list[dict],
    num_rows: int,
    fk_columns: set[str],
    unique_cols: list[dict],
) -> tuple[list[dict], list[str]]:
    """
    Generate num_rows of fake data for a single table.
    Returns (rows, flags) where flags contains any warnings.
    FK columns are SKIPPED (placeholder None) — resolved in Phase 4.
    Serial/auto-increment columns are SKIPPED — DB handles them.
    """
    rows = []
    flags = []
    unique_trackers: dict[str, set] = {}  # column_name -> set of used values

    # Identify single-column unique constraints
    for uc in unique_cols:
        if len(uc["columns"]) == 1:
            unique_trackers[uc["columns"][0]] = set()

    # Check for unsupported types
    for col in columns:
        if is_serial(col) or is_fk(col, fk_columns):
            continue
        dtype = col["type"]
        udt = col["udt"]
        if dtype not in SUPPORTED_TYPES and udt not in SUPPORTED_TYPES:
            flags.append(
                f"⚠️  unsupported column type: {table_name}.{col['column']} "
                f"has type '{dtype}' (udt: '{udt}'), using generic string fallback"
            )

    for _ in range(num_rows):
        row = {}
        for col in columns:
            col_name = col["column"]

            # Skip serial/auto-increment — DB will assign
            if is_serial(col):
                continue

            # Skip FK columns — Phase 4 will resolve these
            if is_fk(col, fk_columns):
                row[col_name] = None  # placeholder
                continue

            # Nullable: 15% chance of null
            if col["nullable"] and random.random() < 0.15:
                row[col_name] = None
                continue

            # Try name-pattern match first (higher quality)
            name_provider = match_name_pattern(col_name)
            if name_provider:
                value = name_provider()
                # Respect max_length
                if isinstance(value, str) and col["max_length"]:
                    value = value[: col["max_length"]]
            else:
                # Fall back to type-based generation
                value = generate_by_type(col)
                if value is None and not col["nullable"]:
                    # Unsupported type, NOT NULL — use generic string
                    value = fake.word()

            # Enforce uniqueness for single-column unique constraints
            if col_name in unique_trackers:
                attempts = 0
                while value in unique_trackers[col_name] and attempts < 100:
                    if name_provider:
                        value = name_provider()
                        if isinstance(value, str) and col["max_length"]:
                            value = value[: col["max_length"]]
                    else:
                        value = generate_by_type(col)
                    attempts += 1
                if attempts >= 100:
                    # Force uniqueness with suffix
                    value = f"{value}_{len(unique_trackers[col_name])}"
                unique_trackers[col_name].add(value)

            row[col_name] = value
        rows.append(row)

    return rows, flags


def generate_all(schema: dict, rows_per_table: int = 5) -> dict:
    """
    Generate mock data for all tables in dependency order.
    Returns {table_name: {rows: [...], flags: [...]}} and overall metadata.
    """
    order_info = get_generation_order(schema)
    generation_order = order_info["generation_order"]
    fks = schema["foreign_keys"]
    uniques = order_info["unique_constraints"]

    # Build FK column lookup: {table: set of FK column names}
    fk_lookup: dict[str, set[str]] = {}
    for fk in fks:
        fk_lookup.setdefault(fk["child_table"], set()).add(fk["child_column"])

    result = {
        "generation_order": generation_order,
        "tables": {},
        "all_flags": [],
    }

    for table in generation_order:
        columns = schema["tables"][table]
        table_fk_cols = fk_lookup.get(table, set())
        table_uniques = uniques.get(table, [])

        rows, flags = generate_table_data(
            table, columns, rows_per_table, table_fk_cols, table_uniques
        )

        result["tables"][table] = {
            "row_count": len(rows),
            "rows": rows,
            "flags": flags,
            "fk_columns_pending": sorted(list(table_fk_cols)) if table_fk_cols else [],
        }
        result["all_flags"].extend(flags)

    return result


if __name__ == "__main__":
    schema = introspect()
    data = generate_all(schema, rows_per_table=5)

    # Print summary first, then full data
    print("=" * 60)
    print("ARCEUS — Tier 1 Generation Report")
    print("=" * 60)
    print(f"Generation order: {data['generation_order']}")
    print()

    for table in data["generation_order"]:
        info = data["tables"][table]
        print(f"--- {table} ({info['row_count']} rows) ---")
        if info["fk_columns_pending"]:
            print(f"  ⏳ FK columns pending Phase 4: {info['fk_columns_pending']}")
        if info["flags"]:
            for f in info["flags"]:
                print(f"  {f}")
        for i, row in enumerate(info["rows"]):
            print(f"  [{i+1}] {json.dumps(row, default=str)}")
        print()

    if data["all_flags"]:
        print("=" * 60)
        print("FLAGS:")
        for f in data["all_flags"]:
            print(f"  {f}")
    else:
        print("No flags — all column types supported.")
