from sqlalchemy import create_engine
from config import DATABASE_PATH

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


def get_schema():

    schema = ""

    with engine.connect() as conn:

        tables = conn.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )

        for table in tables:

            table_name = table[0]

            schema += f"\nTable: {table_name}\n"

            columns = conn.exec_driver_sql(
                f"PRAGMA table_info({table_name});"
            )

            for column in columns:

                schema += f"{column[1]} {column[2]}\n"

    return schema