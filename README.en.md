[Русский](README.md)|[English](README.en.md)
<br>
![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
<br>

# Project 202312-todo: task list management system



A program for creating ToDo tasks. 202312-todo is a multifunctional task management application written in Python.

It provides two convenient interfaces: a console application for working from the command line and a REST API (partially implemented, currently under development) for integration with web applications and other systems.

With todoapp, users can easily add, view, update, and delete tasks, while keeping all changes in a shared database. It is a flexible solution for efficient time and task management.

The application was developed and tested in the following environments:
- Windows 10 and Windows 11
- Windows 10/11 with WSL (Windows Subsystem for Linux)
- Ubuntu Linux

---

## Preparing to run

### 1. Prerequisites

To run the project, you will need:

* Git installed;
* `uv` installed — a Python project manager that automatically creates a virtual environment and installs dependencies based on `pyproject.toml` and `uv.lock`.

Check that `uv` is available:

```
uv --version
```

If the command is not found, install `uv` following the instructions on the developer’s (Astral) website for your operating system.

---

### 2. Cloning the repository

Clone the repository to the desired location and go to the project folder:

```
git clone https://github.com/EPoY74/202312-todo.git
cd 202312-todo
```

All subsequent commands are executed from the project root (where `README.md`, `pyproject.toml`, and `uv.lock` are located).

---

### 3. Installing dependencies with uv

Install the project dependencies:

```
uv sync
```

This command:

* creates a virtual environment in `.venv` (if it does not already exist);
* installs the dependencies listed in `pyproject.toml`;
* brings the environment to the exact state recorded in `uv.lock` (reproducible and predictable set of versions).

The Python interpreter will be selected automatically by `uv`; if a suitable version is not available, `uv` will suggest installing it.

---

## Running the project

### 4. Database initialization

Before first use, you need to create the SQLite database file and the tables. To do this, run:

```
uv run python -m src.cli --create_db
```

After successful execution, this command will create the database file (by default it is located in the `src/data` directory).

---

### 5. Running the CLI version (console application)

To view a short help for the CLI:

```
uv run python -m src.cli
```

Typical usage examples:

```
# Show the task list
uv run python -m src.cli --tasks_list
```

```
# Add a new task
uv run python -m src.cli --task_add "Buy milk"
```

```
# Mark a task as completed (by ID)
uv run python -m src.cli --completed_at 1
```

```
# Delete a task (by ID)
uv run python -m src.cli --task_del_id 1
```

The up-to-date list of options and flags can be obtained via:

```
uv run python -m src.cli
```

or in the section describing CLI commands further down in the README.

---

### 6. Running the API version (optional)

The project also includes an API interface for working with tasks over HTTP.

To start it:

```
uv run python -m src.api
```

After startup, the terminal will show the address and port of the server (typically something like `http://127.0.0.1:8000`).

Main endpoints:

* `GET /` — project information / service health;
* `GET /all` — list of all tasks;
* `GET /last` — the most recently added task;
* `GET /task/{id}` — get a task by its identifier.

The exact list and the request/response formats are available in the API description (OpenAPI/Swagger) and in the corresponding API section of the README.

---

### 7. Where data and logs are stored

* Database: directory `src/data/` (main SQLite file with tasks).
* Application logs: directory `src/log/`, the `todo_cli.log` file is created automatically on first run.

---

### 8. Stopping the application

CLI commands exit automatically after they finish their work.

The API server is stopped with `Ctrl + C` in the terminal where it was started:

```
Ctrl + C
```


## License
License: Apache-2.0 – see [License: Apache-2.0](./LICENSE-en)
