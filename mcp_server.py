import os
import psycopg2
from mcp.server.mcpserver import MCPServer
from psycopg2 import sql
from schema_introspector import introspect

mcp = MCPServer("Arceus Database Connector")

def get_db_connection():
    return psycopg2.connect(
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        dbname=os.getenv("POSTGRES_DB", "arceus"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

@mcp.tool()
def get_table_schema(table_name: str) -> str:
    """Queries the PostgreSQL information schema to return the column names and data types."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position;
        """
        cur.execute(query, (table_name,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if not rows:
            return f"No columns found for table '{table_name}'."
            
        schema_str = f"Schema for {table_name}:\n"
        for row in rows:
            schema_str += f"  - {row[0]} ({row[1]})\n"
        return schema_str
    except Exception as e:
        return f"Error reading schema: {e}"

@mcp.tool()
def insert_mock_data(table_name: str, rows: list) -> str:
    """Takes the approved JSON array and executes the SQL INSERT statements safely."""
    if not rows:
        return "No rows provided for insertion."
        
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # We assume all rows in the list are dicts with the same keys
        columns = list(rows[0].keys())
        
        # 1. Validate table and columns against schema
        schema = introspect()
        if table_name not in schema["tables"]:
            return f"Error: Table '{table_name}' does not exist in the schema."
            
        valid_columns = {c["column"] for c in schema["tables"][table_name]}
        for col in columns:
            if col not in valid_columns:
                return f"Error: Column '{col}' does not exist in table '{table_name}'."
        
        # 2. Build safe query using psycopg2.sql
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(sql.Placeholder() * len(columns))
        )
        
        # Prepare the list of tuples for executiom
        data_tuples = []
        for row in rows:
            # ensure order matches
            data_tuples.append(tuple(row[col] for col in columns))
            
        cur.executemany(insert_query, data_tuples)
        conn.commit()
        
        count = cur.rowcount
        cur.close()
        conn.close()
        return f"Successfully inserted {count} rows into {table_name}."
    except Exception as e:
        return f"Error inserting data: {e}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
