# Technical Debt Log

- **DEBT-01:** *[2026-08-28]* Target Database. For speed, we will likely spin up a local SQLite database for the agent to target in the demo, rather than building a robust connector for external AWS/GCP databases. Cost to fix later: Medium (requires building OAuth/secure credential storage for user DBs).