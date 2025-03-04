from typing import List


def main(grist_docs_id: str, lst_foreign_table_queries: List[str]) -> str:
    query_init_ext_server = f"""
    -- Ensure the extension is created
    CREATE EXTENSION IF NOT EXISTS sqlite_fdw;

    -- Drop the server if it already exists
    DROP SERVER IF EXISTS "{grist_docs_id}" CASCADE;

    -- Create the server
    CREATE SERVER IF NOT EXISTS "{grist_docs_id}"
        FOREIGN DATA WRAPPER sqlite_fdw
        OPTIONS (database '/opt/sqlite_database/docs/{grist_docs_id}.grist');
    -- Drop the schema if it exists
    DROP SCHEMA IF EXISTS "{grist_docs_id}" CASCADE;

    -- Create the schema
    CREATE SCHEMA IF NOT EXISTS "{grist_docs_id}";

    -- Unnest foreign table creation
    {"".join(lst_foreign_table_queries)}
    """

    return query_init_ext_server
