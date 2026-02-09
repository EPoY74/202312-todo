[Русский](README.md) | [English](README.en.md)  
![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)

# 202312-todo — Python ToDo / To-Do / TODO app (task manager / task tracker) — CLI + REST API + SQLite (CRUD)

**202312-todo** is an open-source **ToDo app / To-Do list / task manager** written in **Python**. It ships with a productivity-friendly **CLI** (command line interface) and an experimental **HTTP REST API** for integrations (web UI, bots, automation, other services).  
The project focuses on core **CRUD** operations (Create / Read / Update / Delete) and persists tasks in a local **SQLite** database.

## Features

- ✅ **ToDo / Task management**: add, list, update, delete tasks; mark tasks as completed.
- ✅ **CLI (Command Line)**: manage your todo list from the terminal.
- 🧪 **REST API (optional, in progress)**: read tasks over HTTP.
- ✅ **SQLite storage**: simple local persistence for tasks.
- ✅ **Logging**: CLI logs are written to a file.

## Tech stack / Keywords

- **Python**, **SQLite**, **CLI**, **REST API**, **HTTP API**, **CRUD**
- Dependency & environment management via **uv** (`pyproject.toml` + `uv.lock`)

**GitHub topics (SEO):** `python`, `todo`, `to-do`, `todo-app`, `todolist`, `task-manager`, `task-tracker`, `cli`, `command-line`, `rest-api`, `http-api`, `sqlite`, `crud`, `open-source`

## Supported environments

Developed and tested on:

- Windows 10 / Windows 11
- Windows 10/11 with WSL (Windows Subsystem for Linux)
- Ubuntu Linux

## Quick start

> Run all commands from the repository root (where `README.en.md`, `pyproject.toml`, and `uv.lock` are located).

### 1) Prerequisites

- **Git**
- **uv** — Python project manager that creates a virtual environment and installs dependencies from `pyproject.toml` and `uv.lock`

Check `uv`:

```bash
uv --version
```

If the command is not found, install `uv` from the official Astral documentation.

### 2) Clone the repository

```bash
git clone https://github.com/EPoY74/202312-todo.git
cd 202312-todo
```

### 3) Install dependencies (uv)

```bash
uv sync
```

This will:

- create a virtual environment (typically `.venv`) if needed
- install dependencies from `pyproject.toml`
- sync exact locked versions from `uv.lock` (reproducible installs)

## Run the project

### 4) Initialize the SQLite database

Before first use, create the SQLite database file and tables:

```bash
uv run python -m src.cli --create_db
```

The database file will be created (default location: `src/data/`).

#### Load test data (optional)

`src/data/init_db.py` loads the `sqlite-example-data-db-utf-8.sql` dump into the `todo_main.db` database.  
If `todo_main.db` does not exist, it will be created automatically.

```bash
uv run python src/data/init_db.py
```

### 5) Run the CLI (console app)

Show CLI help:

```bash
uv run python -m src.cli
```

Typical commands:

```bash
# Show task list
uv run python -m src.cli --tasks_list
```

```bash
# Add a new task
uv run python -m src.cli --task_add "Buy milk"
```

```bash
# Mark task as completed (by ID)
uv run python -m src.cli --completed_at 1
```

```bash
# Delete task (by ID)
uv run python -m src.cli --task_del_id 1
```

### 6) Run the REST API (optional, experimental)

Start the API server:

```bash
uv run python -m src.api
```

After startup, the terminal will show the server address (typically `http://127.0.0.1:8000`).

Example endpoints:

- `GET /` — project info / health check
- `GET /all` — list all tasks
- `GET /last` — most recently added task
- `GET /task/{id}` — get a task by id

> If OpenAPI/Swagger is enabled in your API module, use it as the source of truth for request/response formats.

### 7) Data and logs

- **Database (SQLite):** `src/data/`
- **Logs:** `src/log/` (`todo_cli.log` is created automatically on first run)

### 8) Stop the application

- CLI commands exit automatically after completion.
- Stop the API server with `Ctrl + C` in the terminal where it is running.

## License

Apache-2.0 — see [LICENSE-en](./LICENSE-en)
