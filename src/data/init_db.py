import sqlite3
from pathlib import Path

DB_PATH = Path("todo_main.db")
DUMP_PATH = Path("sqlite-example-data-db-utf-8.sql")

def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    sql = DUMP_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(sql)

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
