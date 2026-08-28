# Progress & Changelog

---

## [2026-08-28] Phase 0: Project Kickoff & Initialization
**Status:** done
**What was done:** Selected "Arceus" as the product concept. Initialized `/docs` folder with `goal.md`, `decisions.md`, `progress.md`, `assumptions.md`, `skill.md`. Replaced all "DataForge" references with "Arceus".
**How it was tested:** Manual review of all doc files for naming consistency.
**Result:** All 5 doc files created. 0 remaining "DataForge" references.
**Open issues:** none

---

## [2026-08-28] Phase 0: Environment Setup (Next.js + Docker)
**Status:** done
**What was done:** Ran `npx create-next-app` in `/frontend` (App Router, Tailwind, TypeScript). Created `docker-compose.yml` with `postgres:15`. Created `.gitignore`. Purged cached `.venv` and `node_modules` from git tracking.
**How it was tested:** `npm run dev` starts on localhost:3000. `docker-compose up -d` starts Postgres container. `git status` confirms no tracked junk.
**Result:** Next.js dev server runs. Postgres container healthy on port 5432. `.gitignore` active.
**Open issues:** none

---

## [2026-08-28] Phase 0: Architecture Pivot — Drop Faker, Use npx TrueForge
**Status:** done
**What was done:** Deleted `Dockerfile.trueforge`. Reverted `docker-compose.yml` to Postgres-only. Switched from faker to standard Python libraries. Adopted `npx @truefoundry/trueforge` as the agent runner to avoid repo bloat.
**How it was tested:** `docker-compose up -d` succeeds. `npx @truefoundry/trueforge` starts on port 8790. No build errors.
**Result:** Architecture simplified. TrueForge runs standalone via npx. Postgres container healthy.
**Open issues:** none

---

## [2026-08-28] Phase 0: Dashboard UI & Approval Loop
**Status:** done
**What was done:** Built Arceus dashboard in `page.tsx` with Table Name input, Row Count input, Generate Data button, and Approve Injection button. Created `/api/approve/route.ts` and `/api/generate/route.ts` API routes. Added success/error banners and Cancel/Clear functionality.
**How it was tested:** Loaded dashboard at localhost:3000. Clicked Generate, verified table populates. Clicked Approve, verified success banner appears and table clears. Clicked Cancel, verified table clears.
**Result:** Full generate → preview → approve/reject cycle works in the UI. API routes return correct responses.
**Open issues:** 🟡 Generate route currently returns mock data from the API, not from TrueForge agent — will be replaced in Phase 3+.

---

## [2026-08-28] Phase 0: MCP Server & DB Init Script
**Status:** done
**What was done:** Created `init.sql` with test schema. Updated `docker-compose.yml` to mount `init.sql` into Postgres init dir. Implemented `mcp_server.py` with `MCPServer` class exposing `get_table_schema()` and `insert_mock_data()` tools via psycopg2.
**How it was tested:** `docker-compose down -v && docker-compose up -d` to reinitialize DB. Ran `python3 -c "import mcp_server; print(mcp_server.get_table_schema('users'))"` inside `.venv`.
**Result:** MCP tool returns correct schema: `id (integer)`, `name (character varying)`, `email (character varying)`, `created_at (timestamp without time zone)`.
**Open issues:** none

---

## [2026-08-28] Phase 0: README & Hackathon Compliance
**Status:** done
**What was done:** Wrote production-grade `README.md` with project explanation, Getting Started steps, and `## Qodo Code Review Evidence` section with placeholder PR link.
**How it was tested:** Reviewed README content against hackathon requirements checklist.
**Result:** README contains all required sections. Qodo evidence section present with correct heading.
**Open issues:** none

---

## [2026-08-28] Phase 1: Schema Introspection
**Status:** done
**What was done:** Created `schema_introspector.py` that queries `information_schema` to extract all tables, columns (types, nullability, defaults), primary keys, foreign keys, and unique constraints. Replaced `init.sql` with a 4-table relational schema (`users`, `products`, `orders`, `order_items`) with FKs, composite unique constraints, and varied column types.
**How it was tested:** Ran `python3 schema_introspector.py` inside `.venv` against live Postgres container with the 4-table test schema.
**Result:** All 4 tables detected. All 24 columns with correct types/nullability/defaults. All 4 PKs found. All 3 FK relationships correct (`orders→users`, `order_items→orders`, `order_items→products`). All 3 unique constraints found including composite `(order_id, product_id)`.
**Open issues:** none — awaiting approval to proceed to Phase 2.

---

## [2026-08-28] Phase 2: Dependency Graph + Generation Order
**Status:** done
**What was done:** Created `dependency_graph.py` using Kahn's topological sort. Builds adjacency list from FK relationships, produces a generation order (parents before children), and explicitly detects/flags self-referencing FKs and circular dependencies instead of guessing.
**How it was tested:** Ran `python3 dependency_graph.py` inside `.venv` against live Postgres container with 4-table schema (`users`, `products`, `orders`, `order_items`).
**Result:** Correct order: `products → users → orders → order_items`. All 3 FK edges respected. 0 self-referencing FKs. 0 circular dependencies. Composite unique constraint `(order_id, product_id)` carried through.
**Open issues:** none

---

## [2026-08-28] Phase 3: Tier 1 Faker Generation
**Status:** done
**What was done:** Created `data_generator.py` with 20+ name-pattern→Faker mappings (email, name, phone, sku, status, category, etc.) and type-based fallbacks for all standard Postgres types. Respects `max_length`, `numeric(p,s)` precision, nullable (15% null chance), and single-column unique constraints. Serial PKs are skipped (DB auto-assigns). FK columns output as `null` placeholders with visible `⏳ pending Phase 4` flags. Unsupported types are flagged visibly, never silently guessed.
**How it was tested:** Ran `python3 data_generator.py` inside `.venv` against live Postgres container with 4-table schema. Generated 5 rows per table (20 rows total).
**Result:** 20 rows generated across 4 tables in correct dependency order. All emails unique. All SKUs unique. Prices within `numeric(10,2)`. Timestamps ISO-formatted within 2-year range. FK columns correctly deferred. 0 unsupported type flags.
**Open issues:** none