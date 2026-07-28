import sqlite3
from sqlalchemy import create_engine


DATABASE_PATH = "data/database/chatbot.db"


def create_database():

    engine = create_engine(
        f"sqlite:///{DATABASE_PATH}"
    )

    return engine

def save_to_database(df, table_name):

    engine = create_database()

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

def list_tables():

    engine = create_database()

    with engine.connect() as conn:

        result = conn.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )

        return [row[0] for row in result]