import asyncio
import os
import asyncpg
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Arceus Database Connector")

async def get_db_connection():
    return await asyncpg.connect(
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        database=os.getenv("POSTGRES_DB", "arceus"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

@mcp.tool()
async def read_database_schema() -> str:
    """Reads the database schema from the connected PostgreSQL instance."""
    try:
        conn = await get_db_connection()
        query = """
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """
        rows = await conn.fetch(query)
        await conn.close()
        
        if not rows:
            return "No tables found in public schema."
            
        schema_dict = {}
        for row in rows:
            table = row['table_name']
            if table not in schema_dict:
                schema_dict[table] = []
            schema_dict[table].append(f"{row['column_name']} ({row['data_type']})")
            
        schema_str = "Database Schema:\n"
        for table, cols in schema_dict.items():
            schema_str += f"Table: {table}\n"
            for col in cols:
                schema_str += f"  - {col}\n"
        return schema_str
    except Exception as e:
        return f"Error connecting to or reading from database: {e}"

if __name__ == "__main__":
    # In a real environment, you might run via FastMCP CLI or start it manually
    print("MCP Server initialized. Run via FastMCP standard procedures.")
    mcp.run(transport='stdio')
