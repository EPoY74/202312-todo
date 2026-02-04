import os
import sqlite3

DB_NAME: str = "todo_main.db"
DUMP_NAME: str = "sqlite-example-data-db-utf-8.sql"
FOLDER_PATH: str = os.path.dirname(__file__)

DB_PATH: str = os.path.join(FOLDER_PATH, DB_NAME)
DUMP_PATH: str = os.path.join(FOLDER_PATH, DUMP_NAME)


def init_db() -> None:

    with open(DUMP_PATH, encoding="utf-8") as dump_sql_file:
        sql_dump = dump_sql_file.read()
    print("SQL dump file has been read successfully.")  #noqa T201

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(sql_dump)


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")  # noqa T201
