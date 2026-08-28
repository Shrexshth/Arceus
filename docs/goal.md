# Project Goals & Architecture: Arceus

**Structure Change Log:**
- *2026-08-28:* Initialized Arceus architecture (Next.js + TrueForge).

## Onboarding Stub
Welcome to Arceus. We are building an agentic tool for developers that reads a database schema via MCP, writes a Python script in a secure sandbox to generate realistic mock data, and waits for a human to click "Approve" before injecting it into the database. It exists to solve the pain of manually writing fake data for UI testing.

## End-to-End Structure & Data Flow
1. **Frontend:** Next.js (TailwindCSS) dashboard.
2. **Backend/Harness:** TrueForge running locally.
3. **Tools (MCP):** Database Connector (Reads schema, executes inserts).
4. **Sandbox:** TrueForge Python Sandbox (runs data generation script).
5. **Flow:** User Prompt -> TrueForge queries schema via MCP -> TrueForge writes generation script -> Sandbox executes script -> JSON preview sent to Frontend -> Human Approves -> TrueForge executes SQL injection via MCP.

## Tech Stack & Versions
- Next.js (App Router, Latest)
- TrueForge (Latest CLI/Docker)
- PostgreSQL or SQLite (for dummy target database)
- Qodo (GitHub Integration)

## Metrics/KPIs (Definition of Success)
- 1 successful end-to-end execution of schema reading -> sandbox generation -> human approval -> DB injection.
- 1 clean PR reviewed by Qodo documented in README.
- 1 demo video (<3 mins) showing the "Approve" button.

## Rough Roadmap
- **Built:** Docs.
- **Next:** TrueForge setup, Qodo integration, basic Next.js UI.
- **Out of Scope:** Complex authentication, multi-database support (sticking to one DB type for the demo).