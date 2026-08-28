"""
Arceus Phase 1: Schema Introspector
Connects to a PostgreSQL database and extracts:
  - All tables and columns (types, nullability, defaults)
  - Primary keys
  - Foreign key relationships
  - Unique constraints
"""
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection(conn_str: str | None = None):
    """Connect using a connection string or env vars."""
    if conn_str:
        return psycopg2.connect(conn_str)
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        dbname=os.getenv("POSTGRES_DB", "arceus"),
    )


def introspect_columns(cur) -> dict:
    """Return {table_name: [column_info, ...]} for all public tables."""
    cur.execute("""
        SELECT
            table_name,
            column_name,
            data_type,
            udt_name,
            character_maximum_length,
            numeric_precision,
            numeric_scale,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    tables: dict[str, list] = {}
    for row in cur.fetchall():
        t = row["table_name"]
        tables.setdefault(t, []).append({
            "column": row["column_name"],
            "type": row["data_type"],
            "udt": row["udt_name"],
            "max_length": row["character_maximum_length"],
            "numeric_precision": row["numeric_precision"],
            "numeric_scale": row["numeric_scale"],
            "nullable": row["is_nullable"] == "YES",
            "default": row["column_default"],
        })
    return tables


def introspect_primary_keys(cur) -> dict:
    """Return {table_name: [pk_column, ...]}."""
    cur.execute("""
        SELECT
            tc.table_name,
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
            AND tc.table_name = kcu.table_name
            AND tc.table_catalog = kcu.table_catalog
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = 'public'
        ORDER BY tc.table_name, kcu.ordinal_position;
    """)
    pks: dict[str, list] = {}
    for row in cur.fetchall():
        pks.setdefault(row["table_name"], []).append(row["column_name"])
    return pks


def introspect_foreign_keys(cur) -> list:
    """Return list of FK relationships."""
    cur.execute("""
        SELECT
            tc.table_name       AS child_table,
            kcu.column_name     AS child_column,
            ccu.table_name      AS parent_table,
            ccu.column_name     AS parent_column,
            tc.constraint_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
            AND tc.table_name = kcu.table_name
            AND tc.table_catalog = kcu.table_catalog
        JOIN information_schema.referential_constraints rc
            ON rc.constraint_name = tc.constraint_name
            AND rc.constraint_schema = tc.table_schema
            AND rc.constraint_catalog = tc.table_catalog
        JOIN information_schema.key_column_usage ccu
            ON ccu.constraint_name = rc.unique_constraint_name
            AND ccu.table_schema = rc.unique_constraint_schema
            AND ccu.table_catalog = rc.unique_constraint_catalog
            AND ccu.ordinal_position = kcu.position_in_unique_constraint
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_schema = 'public'
        ORDER BY tc.table_name;
    """)
    return [dict(row) for row in cur.fetchall()]


def introspect_unique_constraints(cur) -> dict:
    """Return {table_name: [{constraint_name, columns: [...]}, ...]}."""
    cur.execute("""
        SELECT
            tc.table_name,
            tc.constraint_name,
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
            AND tc.table_name = kcu.table_name
            AND tc.table_catalog = kcu.table_catalog
        WHERE tc.constraint_type = 'UNIQUE'
          AND tc.table_schema = 'public'
        ORDER BY tc.table_name, tc.constraint_name, kcu.ordinal_position;
    """)
    uniques: dict[str, list] = {}
    current: dict[str, list] = {}  # constraint_name -> columns
    current_table = None
    for row in cur.fetchall():
        t = row["table_name"]
        cn = row["constraint_name"]
        if t != current_table:
            if current_table and current:
                uniques[current_table] = [
                    {"constraint": k, "columns": v} for k, v in current.items()
                ]
            current = {}
            current_table = t
        current.setdefault(cn, []).append(row["column_name"])
    # flush last table
    if current_table and current:
        uniques[current_table] = [
            {"constraint": k, "columns": v} for k, v in current.items()
        ]
    return uniques


def introspect(conn_str: str | None = None) -> dict:
    """Full introspection: returns a structured schema dict."""
    conn = get_connection(conn_str)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            columns = introspect_columns(cur)
            pks = introspect_primary_keys(cur)
            fks = introspect_foreign_keys(cur)
            uniques = introspect_unique_constraints(cur)
    finally:
        conn.close()

    return {
        "tables": columns,
        "primary_keys": pks,
        "foreign_keys": fks,
        "unique_constraints": uniques,
    }


if __name__ == "__main__":
    schema = introspect()
    print(json.dumps(schema, indent=2, default=str))
