import json
import psycopg2
from sqlalchemy import create_engine, URL
from sqlalchemy.sql import text
import wmill


def main(
    query: str,
    db_path_credentials: str = "u/krichkorn/json_vanilla_grist_supabase_pg_sqlite_fdw",
    drivername: str = "postgresql+psycopg2",
):
    try:
        _ = wmill.get_variable(db_path_credentials)
        creds = json.loads(_)
        url = URL.create(
            drivername=drivername,
            username=creds["username"],
            password=creds["password"],
            host=creds["host"],
            port=creds["port"],
            database=creds["database"],
        )
    except Exception as e:
        raise e

    # Create an SQLAlchemy engine instance using the URL object
    engine = create_engine(url.__to_string__(hide_password=False))

    print(query)

    with engine.connect() as connection:
        result = connection.execute(text(query))
        connection.commit()
    return result
