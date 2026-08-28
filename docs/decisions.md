# Architectural Decisions

---

## [2026-08-28] Product Concept — Arceus
**Decision:** Build an automated mock data generator (Arceus) over forking TrueForge or building a different tool.
**Alternatives considered:** Incident responder, multi-agent research desk, forking TrueForge directly.
**Why this one:** Most scoped-down idea that hits all hackathon judging criteria (MCP, Sandbox, Human Approval, Qodo). Forking TrueForge would violate "Use of sponsor tools" criteria.
**Trade-off accepted:** Less flashy than a complex multi-agent system.
**Confidence:** High
**Reversible:** No (48-hour time constraint)

---

## [2026-08-28] Drop Faker — Use Standard Python Libraries
**Decision:** Use Python's `random`, `string`, `datetime` (and later `Faker`) instead of requiring `faker` inside TrueForge's sandbox.
**Alternatives considered:** Install faker via custom Docker image, pip install at sandbox runtime.
**Why this one:** Custom Docker image failed (no public `trueforge` base image). Installing at runtime adds fragility. Standard libraries cover basic generation; we'll add Faker as a host-side dependency (not sandbox) for Phase 3.
**Trade-off accepted:** Less realistic data from standard libs alone, mitigated by adding Faker as a host dependency later.
**Confidence:** High
**Reversible:** Yes (can add Faker later)

---

## [2026-08-28] Run TrueForge via npx, Not Docker
**Decision:** Use `npx @truefoundry/trueforge` to run TrueForge locally instead of cloning the repo or building a Docker image.
**Alternatives considered:** `git clone truefoundry/trueforge`, custom Dockerfile.
**Why this one:** `npx` keeps the repo clean (no bloat from cloned repos), auto-updates, and matches TrueFoundry's recommended standalone usage.
**Trade-off accepted:** Less control over TrueForge configuration vs. a cloned repo.
**Confidence:** High
**Reversible:** Yes

---

## [2026-08-28] Schema Introspection via information_schema
**Decision:** Query `information_schema.columns`, `information_schema.table_constraints`, and `information_schema.key_column_usage` to extract schema metadata.
**Alternatives considered:** `pg_catalog` system tables directly, `psycopg2.sql.Identifier` + manual `\d` parsing, SQLAlchemy `inspect()`.
**Why this one:** `information_schema` is SQL-standard (works on Postgres AND MySQL with minimal changes), well-documented, and returns structured data without needing ORM overhead.
**Trade-off accepted:** Slightly less Postgres-specific detail than `pg_catalog` (e.g., no CHECK constraints, no custom enum values). Will add `pg_catalog` queries if needed in later phases.
**Confidence:** High
**Reversible:** Yes (can swap to pg_catalog queries)

---

## [2026-08-28] 4-Table Test Schema Design
**Decision:** Use `users`, `products`, `orders`, `order_items` as the test schema for Phase 1 verification.
**Alternatives considered:** Simpler 2-table schema, a more complex 6+ table schema.
**Why this one:** 4 tables covers all required patterns: parent tables with no FKs (`users`, `products`), single-FK child (`orders` → `users`), multi-FK grandchild (`order_items` → `orders` + `products`), composite unique constraint, varied types (varchar, text, numeric, boolean, timestamp, serial).
**Trade-off accepted:** Doesn't test circular FKs or self-referencing tables — will add if encountered.
**Confidence:** High
**Reversible:** Yes

---

## [2026-08-28] Dependency Ordering — Kahn's Topological Sort
**Decision:** Use Kahn's algorithm (BFS-based topological sort) for table generation ordering.
**Alternatives considered:** DFS-based topological sort, `networkx.topological_sort()`, manual ordering.
**Why this one:** Kahn's algorithm naturally detects cycles (any node with remaining in-degree > 0 is in a cycle), which we need to flag explicitly per the hard rules. No external dependency needed (`networkx` avoided). Deterministic output via sorted tie-breaking.
**Trade-off accepted:** Slightly more code than a one-liner `networkx` call, but avoids adding a dependency for a single function.
**Confidence:** High
**Reversible:** Yes