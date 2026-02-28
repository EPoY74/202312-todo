import shutil
import sqlite3
import sys
import uuid
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.db_access.db_working import (  # noqa: E402
    delete_task,
    get_record_by_id,
    make_db,
    make_task,
    set_tasks_deadline,
    task_completed,
    work_with_slq,
)


def _make_tmp_dir() -> Path:
    base = Path(__file__).resolve().parent / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    tmp_dir = base / uuid.uuid4().hex
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir


def _cleanup_tmp_dir(tmp_dir: Path) -> None:
    shutil.rmtree(tmp_dir, ignore_errors=True)


def _create_db(tmp_dir: Path) -> Path:
    db_path = tmp_dir / "test.db"
    make_db(str(db_path))
    return db_path


def _fetch_one(
    db_path: Path, sql: str, params: tuple = ()
) -> sqlite3.Row | None:
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()


def _fetch_all(
    db_path: Path, sql: str, params: tuple = ()
) -> list[sqlite3.Row]:
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()


def test_make_db_and_make_task():
    tmp_dir = _make_tmp_dir()
    try:
        db_path = _create_db(tmp_dir)
        make_task(str(db_path), "Task A")

        rows = _fetch_all(db_path, "SELECT * FROM my_todo_list")
        assert len(rows) == 1
        assert rows[0]["todo_text"] == "Task A"
    finally:
        _cleanup_tmp_dir(tmp_dir)


def test_get_record_by_id_returns_row():
    tmp_dir = _make_tmp_dir()
    try:
        db_path = _create_db(tmp_dir)
        make_task(str(db_path), "Task B")

        rows = get_record_by_id(str(db_path), 1)
        assert len(rows) == 1
        assert rows[0]["todo_text"] == "Task B"
    finally:
        _cleanup_tmp_dir(tmp_dir)


def test_set_tasks_deadline_updates_date_max(monkeypatch: pytest.MonkeyPatch):
    tmp_dir = _make_tmp_dir()
    try:
        db_path = _create_db(tmp_dir)
        make_task(str(db_path), "Task C")

        inputs = iter(["01.01.2030 10:00", "y"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        set_tasks_deadline(str(db_path), 1)

        row = _fetch_one(
            db_path, "SELECT date_max FROM my_todo_list WHERE id=?", (1,)
        )
        assert row is not None
        assert row["date_max"] == "01.01.2030 10:00"
    finally:
        _cleanup_tmp_dir(tmp_dir)


def test_task_completed_sets_flags(monkeypatch: pytest.MonkeyPatch):
    tmp_dir = _make_tmp_dir()
    try:
        db_path = _create_db(tmp_dir)
        make_task(str(db_path), "Task D")

        monkeypatch.setattr("builtins.input", lambda _: "y")
        task_completed(str(db_path), 1)

        row = _fetch_one(
            db_path,
            "SELECT is_gone, date_of_gone FROM my_todo_list WHERE id=?",
            (1,),
        )
        assert row is not None
        assert row["is_gone"] == 1
        assert row["date_of_gone"]
    finally:
        _cleanup_tmp_dir(tmp_dir)


def test_delete_task_removes_row(monkeypatch: pytest.MonkeyPatch):
    tmp_dir = _make_tmp_dir()
    try:
        db_path = _create_db(tmp_dir)
        make_task(str(db_path), "Task E")

        monkeypatch.setattr("builtins.input", lambda _: "y")
        delete_task(str(db_path), 1)

        rows = _fetch_all(db_path, "SELECT * FROM my_todo_list")
        assert len(rows) == 0
    finally:
        _cleanup_tmp_dir(tmp_dir)


def test_work_with_slq_write_and_read_one():
    tmp_dir = _make_tmp_dir()
    try:
        db_path = _create_db(tmp_dir)

        insert_sql = (
            "INSERT INTO my_todo_list (data_of_creation, todo_text, is_gone)"
            " VALUES (?, ?, ?)"
        )
        work_with_slq(
            str(db_path),
            "write",
            "one",
            insert_sql,
            ("01.01.2026 10:00", "Task SQL 1", 0),
        )

        rows = work_with_slq(
            str(db_path),
            "read",
            "one",
            "SELECT * FROM my_todo_list WHERE todo_text=?",
            ("Task SQL 1",),
        )
        assert len(rows) == 1
        assert rows[0]["todo_text"] == "Task SQL 1"
    finally:
        _cleanup_tmp_dir(tmp_dir)


def test_work_with_slq_read_many():
    tmp_dir = _make_tmp_dir()
    try:
        db_path = _create_db(tmp_dir)

        for idx in range(3):
            make_task(str(db_path), f"Task SQL {idx}")

        rows = work_with_slq(
            str(db_path), "read", "many", "SELECT * FROM my_todo_list"
        )
        assert len(rows) == 3
    finally:
        _cleanup_tmp_dir(tmp_dir)


def test_direct_sql_update_and_delete():
    tmp_dir = _make_tmp_dir()
    try:
        db_path = _create_db(tmp_dir)
        make_task(str(db_path), "Task Direct")

        with sqlite3.connect(str(db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE my_todo_list SET todo_text=? WHERE id=?",
                ("Task Direct Updated", 1),
            )
            conn.commit()

        row = _fetch_one(
            db_path, "SELECT todo_text FROM my_todo_list WHERE id=?", (1,)
        )
        assert row is not None
        assert row["todo_text"] == "Task Direct Updated"

        with sqlite3.connect(str(db_path)) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM my_todo_list WHERE id=?", (1,))
            conn.commit()

        rows = _fetch_all(db_path, "SELECT * FROM my_todo_list")
        assert len(rows) == 0
    finally:
        _cleanup_tmp_dir(tmp_dir)
