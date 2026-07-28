import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_PATH

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)

def execute_query(sql):
    try:
        df = pd.read_sql_query(sql, engine)
        return True, df

    except Exception as e:
        return False, str(e)