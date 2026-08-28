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
Bring up the local PostgreSQL database using Docker Compose.
```bash
docker-compose up -d
```

### 2. Start the TrueForge Agent
Run the TrueForge agent harness via `npx`. This orchestrates the data generation and handles MCP execution.
```bash
npx @truefoundry/trueforge
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
