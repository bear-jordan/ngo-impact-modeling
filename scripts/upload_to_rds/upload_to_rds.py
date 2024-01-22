from pathlib import Path
import os

from dotenv import load_dotenv
from icecream import ic
import pandas as pd
from sqlalchemy import create_engine


VOTER_HIST_PATH = Path(__file__).parent.parent.parent / "data" / "ncvhis60.txt"
VOTER_PATH = Path(__file__).parent.parent.parent / "data" / "ncvoter60.txt"


def get_engine():
    load_dotenv()
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    return create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )


def upload_data(file_path, engine, table_name):
    data = pd.read_table(file_path, encoding="ISO-8859-1")
    data.to_sql(table_name, con=engine, index=False, if_exists="append")


def main():
    engine = ic(get_engine())
    ic("Uploading voter_history")
    upload_data(VOTER_HIST_PATH, engine, "voter_history")

    ic("Uploading nc_voter")
    upload_data(VOTER_PATH, engine, "nc_voter")
    ic("Upload complete")


if __name__ == "__main__":
    main()
