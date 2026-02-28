import sys
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import src.api.main_api as main_api  # noqa: E402


def test_root_returns_message():
    client = TestClient(main_api.app_todo)
    res = client.get("/")
    assert res.status_code == 200
    payload = res.json()
    assert isinstance(payload, dict)
    assert "This is API for EPoY's todo app. Since 2023." in payload.values()


def test_all_uses_list_of_tasks_json(monkeypatch):
    expected = [{"id": 1, "todo_text": "Task A"}]

    def fake_list_of_tasks_json(db_path, all_or_last="all", id_row=0):
        assert all_or_last == "all"
        assert id_row == 0
        return expected

    monkeypatch.setattr(
        main_api.db_working_api, "list_of_tasks_json", fake_list_of_tasks_json
    )

    client = TestClient(main_api.app_todo)
    res = client.get("/all")
    assert res.status_code == 200
    assert res.json() == expected


def test_last_uses_list_of_tasks_json(monkeypatch):
    expected = [{"id": 2, "todo_text": "Task B"}]

    def fake_list_of_tasks_json(db_path, all_or_last="all", id_row=0):
        assert all_or_last == "last"
        assert id_row == 0
        return expected

    monkeypatch.setattr(
        main_api.db_working_api, "list_of_tasks_json", fake_list_of_tasks_json
    )

    client = TestClient(main_api.app_todo)
    res = client.get("/last")
    assert res.status_code == 200
    assert res.json() == expected


def test_task_by_id_uses_list_of_tasks_json(monkeypatch):
    expected = [{"id": 5, "todo_text": "Task C"}]

    def fake_list_of_tasks_json(db_path, all_or_last="all", id_row=0):
        assert all_or_last == "one"
        assert id_row == 5
        return expected

    monkeypatch.setattr(
        main_api.db_working_api, "list_of_tasks_json", fake_list_of_tasks_json
    )

    client = TestClient(main_api.app_todo)
    res = client.get("/task/5")
    assert res.status_code == 200
    assert res.json() == expected
