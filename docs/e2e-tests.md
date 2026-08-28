# TC-ARC-001 - Arceus Agentic Data Generator End-to-End Suite

## Test Suite Metadata

| Field | Value |
|---|---|
| Suite ID | `TC-ARC-001` |
| Functional area | Arceus Data Generation & Human Approval |
| Source backlog | `/docs/goal.md`, `/docs/progress.md` |
| Covered components | Next.js Frontend, TrueForge Harness, Python Sandbox, PostgreSQL MCP |
| Initial execution status | `NOT_RUN` |
| Test type | Functional, Integration, UI, Agentic Execution |

## Result Statuses & Priorities
- `NOT_RUN`: Execution has not started.
- `PASSED`: Observed behavior matches expected result.
- `FAILED`: Observed behavior differs; requires API or Agent prompt debugging.
- `P0`: Release blocker (e.g., Sandbox escape, DB corruption, Hackathon disqualification).
- `P1`: Primary business workflow (UI generation, DB injection).
- `P2`: Secondary behavior (UI styling, loading states).

## Environment Prerequisites
1. PostgreSQL container is running via `docker-compose up -d` on port `5432`.
2. TrueForge harness is running locally via `npx @truefoundry/trueforge`.
3. Next.js dashboard is running via `npm run dev` and accessible at `http://localhost:3000`.
4. `mcp_server.py` is active and connected to the TrueForge instance.
5. A synthetic `users` table exists in the PostgreSQL database with columns: `id`, `name`, `email`, `created_at`.

## A. Infrastructure, Connection, & MCP Registration

| ID | Pri | Scenario and action | Expected result | Result |
|---|---|---|---|---|
| `ARC-INF-001` | P0 | Verify TrueForge HTTP API is reachable from the Next.js backend. | A basic ping to the TrueForge localhost endpoint returns HTTP 200. | PASSED |
| `ARC-INF-002` | P0 | Verify MCP Server Registration in TrueForge. | TrueForge logs confirm the PostgreSQL schema reader tool is registered and active. | PASSED |
| `ARC-INF-003` | P0 | Test MCP Tool execution independently. | Triggering the MCP tool directly returns the accurate schema definition for the `users` table. | PASSED |
| `ARC-INF-004` | P1 | Load Arceus Next.js Dashboard. | Dashboard renders immediately with Table Name input, Row Count input, and disabled "Approve" button. | PASSED |

## B. Agentic Generation & Python Sandbox

| ID | Pri | Scenario and action | Expected result | Result |
|---|---|---|---|---|
| `ARC-GEN-001` | P0 | Submit `users` table and `5` rows via the Next.js UI. | Next.js API route successfully POSTs the prompt to TrueForge. UI enters a loading state. | PASSED |
| `ARC-GEN-002` | P0 | TrueForge Agent Schema Retrieval. | Agent successfully calls the MCP tool, reads the `users` schema, and understands required fields. | FAILED |
| `ARC-GEN-003` | P0 | Sandbox Script Execution. | Agent writes a standard Python script (using `random`, `json`, `datetime`), executes it securely in the Sandbox, and returns a JSON array of 5 valid user records. | FAILED |
| `ARC-GEN-004` | P0 | Invalid Table Name submitted. | Agent recognizes table does not exist via MCP, returns a clean error to the UI without executing sandbox code. | PASSED |

## C. Human Approval Gate (UI Validation)

| ID | Pri | Scenario and action | Expected result | Result |
|---|---|---|---|---|
| `ARC-APP-001` | P0 | Next.js receives generated JSON from TrueForge. | UI placeholder table populates with the 5 generated rows. The JSON is held in browser memory; no DB injection has occurred yet. | PASSED |
| `ARC-APP-002` | P0 | "Approve Injection" Button State. | Button transitions from Disabled to Active green state only after data successfully renders in the UI. | PASSED |
| `ARC-APP-003` | P1 | Click "Cancel/Clear" (Rejection). | Table clears, button disables, memory is flushed. No data touches the database. | PASSED |
| `ARC-APP-004` | P2 | Malformed JSON returned from agent. | UI gracefully catches the parsing error, displays an error banner, and keeps the Approve button disabled. | FAILED |

## D. Database Injection & Final Execution

| ID | Pri | Scenario and action | Expected result | Result |
|---|---|---|---|---|
| `ARC-INJ-001` | P0 | User clicks "Approve Injection". | Next.js sends the JSON array back to TrueForge/MCP with authorization to execute `INSERT` SQL. | PASSED |
| `ARC-INJ-002` | P0 | SQL Execution verification. | The 5 rows are successfully written to the PostgreSQL `users` table. | FAILED |
| `ARC-INJ-003` | P1 | Post-Injection UI State. | UI displays a green success banner, clears the data table, and disables the Approve button to prevent duplicate submissions. | PASSED |
| `ARC-INJ-004` | P0 | Verify actual DB state. | Manually query the PostgreSQL container (`SELECT count(*) FROM users;`). Count has increased by exactly 5. | FAILED |

## E. Hackathon Compliance & Code Quality

| ID | Pri | Scenario and action | Expected result | Result |
|---|---|---|---|---|
| `ARC-HAC-001` | P0 | Qodo Code Review Verification. | The GitHub Pull Request containing the API logic is reviewed by the Qodo bot with no unresolved High-severity issues. | PASSED |
| `ARC-HAC-002` | P0 | README Review Evidence. | `README.md` explicitly links to the Qodo-reviewed PR under the required section header. | PASSED |
| `ARC-HAC-003` | P0 | Code Repository Sanitation. | No `.env` files, database credentials, or `.venv` folders are present in the remote repository. | PASSED |