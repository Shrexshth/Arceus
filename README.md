# Arceus 🚀

Arceus is a powerful, agentic mock data generator built for modern development teams. It completely automates the tedious process of writing fake data for UI testing, staging environments, and database population.

Leveraging the TrueForge agent harness, the Arceus workflow is simple:
1. **Reads** your database schema dynamically using the Model Context Protocol (MCP).
2. **Generates** realistic, context-aware mock data in a secure, isolated sandbox using standard Python libraries.
3. **Pauses** for explicit human approval via a sleek Next.js dashboard before any data is injected into your database.

No more manual SQL inserts. Just instant, schema-aware data generation with full human oversight.

## 🛠 Getting Started

To spin up Arceus locally, you will need to start three distinct services.

### 1. Start the Database
Bring up the local PostgreSQL database using Docker Compose. Since the test schema (`init.sql`) only runs on an empty database volume, ensure any old volumes are cleared first:
```bash
docker-compose down -v
docker-compose up -d
```

### 2. Configure and Start the Python MCP Server
Arceus uses a Python-based Model Context Protocol (MCP) server to safely connect to Postgres. You must install its dependencies and run it so TrueForge can orchestrate it.

First, set up the Python environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the TrueForge Agent
Run the TrueForge agent harness via `npx` and register the local MCP server.
```bash
# Provide the execution command for the MCP server so TrueForge can launch it
npx @truefoundry/trueforge --mcp-server "python3 mcp_server.py"
```

### 3. Start the Arceus Dashboard
Navigate to the frontend directory and start the Next.js UI.
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to interact with the Arceus dashboard and approve pending injections.

## Qodo Code Review Evidence
All substantive code changes for this hackathon were routed through pull requests and reviewed by Qodo before merging. 

Review Evidence PR: https://github.com/Shrexshth/Arceus/pull/1
