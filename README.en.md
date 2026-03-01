[Русская версия](./README.md) | [English version](./README.en.md)

Related documents: [CHANGELOG.md](./CHANGELOG.md) | [CHANGELOG.en.md](./CHANGELOG.en.md) | [RELEASE_NOTES.md](./RELEASE_NOTES.md) | [RELEASE_NOTES.en.md](./RELEASE_NOTES.en.md) | [RELEASE_PAGE.md](./RELEASE_PAGE.md) | [RELEASE_PAGE.en.md](./RELEASE_PAGE.en.md)

# 202312-todo

`202312-todo` is a local task manager written in Python with a CLI interface, SQLite storage, and an experimental FastAPI-based REST API. The project covers a small but practical CRUD workflow for personal task tracking: create a task, list tasks, mark a task as completed, and delete a record.

Project status: `MVP`.

Based on the repository structure and actual runtime checks, this is a practical engineering project rather than a demo-only sample. As of February 28, 2026, the main usable path is the CLI. The API exists and works for basic reads, but it should still be treated as an experimental access layer.

## Table of Contents

- [Purpose](#purpose)
- [Project Context](#project-context)
- [Current Status](#current-status)
- [Architecture](#architecture)
- [Core Modules](#core-modules)
- [Data Contract](#data-contract)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [How to Verify the Project Quickly](#how-to-verify-the-project-quickly)
- [CLI Scenarios](#cli-scenarios)
- [REST API](#rest-api)
- [Local Data and Logs](#local-data-and-logs)
- [Tests](#tests)
- [FAQ and Common Issues](#faq-and-common-issues)
- [MVP Limitations](#mvp-limitations)
- [Further Development](#further-development)
- [Release Documents](#release-documents)
- [License](#license)

## Purpose

The project solves a very simple local workflow: managing a task list without external infrastructure. Instead of a web application or cloud service, it uses SQLite and a terminal interface. That makes it useful for:

- local personal todo management;
- validating CRUD logic in Python;
- building a future API or UI layer on top of an existing data model;
- using it as a compact base for a lightweight task manager.

In search terms, the project naturally fits phrases such as `python todo app`, `CLI task manager`, `SQLite task tracker`, `FastAPI REST API`, and `CRUD application`.

## Project Context

The repository contains:

- a CLI for day-to-day task operations;
- a SQLite access layer;
- `.ini`-based configuration;
- file logging;
- tests for DB, CLI, and API;
- a minimal FastAPI interface for reading task data.

The code history and inline notes suggest an iterative evolution: first a local CLI app, then an API layer added on top of the same storage.

## Current Status

The following points were verified directly:

- the CLI starts and shows help output;
- SQLite is used as the main persistence layer;
- core task operations exist in the DB layer;
- the FastAPI app responds on `/`, `/all`, `/last`, and `/task/{id}`;
- tests exist, but part of test reproducibility depends on the local environment.

Important constraints:

- the API is read-focused and not yet a fully shaped public contract;
- the codebase still contains `TODO` markers around paths, config, and future logic;
- one CLI-related test can fail because of `uv` cache state rather than because of application logic.

## Architecture

The project is a small Python monolith split by responsibility:

1. `src/cli` contains the console interface.
2. `src/db_access` encapsulates SQL operations and task rendering.
3. `src/api` exposes a REST API over the same SQLite storage.
4. `src/cfg` handles config lookup and logging.
5. `src/data` contains the SQL dump and database bootstrap script.
6. `tests` covers the DB layer, CLI, and API behavior.

Simplified flow:

```text
CLI / FastAPI
    -> cfg
    -> db_access
    -> SQLite database
    -> formatted output / JSON response
```

## Core Modules

### `src/cli`

This is the main user-facing entry point. It supports:

- database creation;
- task insertion;
- task listing;
- deadline assignment;
- task completion;
- task deletion.

### `src/db_access/db_working.py`

This is the practical core of the current MVP. It implements:

- database and table creation;
- inserts;
- fetch one / last / all records;
- deadline updates;
- completion marking;
- deletion;
- interactive confirmation for sensitive actions.

### `src/db_access/db_working_api.py`

This module adapts SQLite results for API responses and returns JSON through FastAPI `Response` objects. At the current stage, it is a project-specific adapter rather than a stable reusable API layer.

### `src/api`

A minimal FastAPI application with a small set of GET endpoints. This is enough for local integrations, diagnostics, and lightweight HTTP access, but it is not yet a production-grade REST API surface.

### `src/cfg`

This package handles:

- loading `todo_config.ini`;
- resolving the database name;
- configuring logs in `src/log/todo_cli.log`.

### `src/data`

This directory contains:

- an example SQL dump;
- a database initialization script;
- the working location for SQLite files.

## Data Contract

The main domain entity is a task stored in the `my_todo_list` table.

### `my_todo_list` table

| Field | Type in current schema | Meaning |
| --- | --- | --- |
| `id` | `INTEGER PRIMARY KEY` | Unique task identifier |
| `data_of_creation` | loosely typed in SQLite | Creation date and time |
| `date_max` | `TEXT` | Deadline if set |
| `todo_text` | `TEXT` | Main task text |
| `is_gone` | `INTEGER` | Completion flag: `0` or `1` |
| `date_of_gone` | `TEXT` | Completion timestamp |

### Field semantics

- `todo_text` is the meaningful payload of the task record.
- `date_max` may be `NULL` if no deadline is set.
- `is_gone = 0` means the task is active.
- `is_gone = 1` means the task is completed.
- `date_of_gone` is populated when the task is marked as completed.

### Date format

The project currently uses a string date format: `DD.MM.YYYY HH:MM`, for example `28.02.2026 20:40`. This is simple for CLI use, but not ideal for strict machine integrations.

## Configuration

Basic configuration lives in `src/cfg/todo_config.ini`.

Current parameter:

```ini
[db_cfg]
db_name = todo_main.db
```

The database name can also be overridden with the `TODO_DB_NAME` environment variable.

Current state:

- configuration is intentionally minimal;
- part of the file lookup logic is tied to the repository structure;
- this is acceptable for an MVP, but it should be formalized later.

## Quick Start

### Requirements

- Python `3.12+`
- `uv` if you follow the repository workflow

### Install dependencies

```bash
uv sync
```

### Create the database

```bash
uv run python -m src.cli --create_db
```

### Show CLI help

```bash
python -m src.cli --help
```

### Start the API

```bash
uv run python -m src.api
```

After startup, the API is typically available at `http://127.0.0.1:8000`.

## How to Verify the Project Quickly

A minimal verification path:

1. Install dependencies with `uv sync`.
2. Create the database with `uv run python -m src.cli --create_db`.
3. Add a task: `uv run python -m src.cli --task_add "Project check"`.
4. List tasks: `uv run python -m src.cli --tasks_list`.
5. Start the API: `uv run python -m src.api`.
6. Check `GET /` and `GET /all`.

If you want sample data immediately, load the bundled SQL dump:

```bash
uv run python src/data/init_db.py
```

## CLI Scenarios

Main command examples:

```bash
python -m src.cli --create_db
python -m src.cli --task_add "Buy milk"
python -m src.cli --tasks_list
python -m src.cli --completed_at 1
python -m src.cli --task_del_id 1
```

One implementation detail matters: some operations require interactive `y/n` confirmation.

## REST API

Current endpoints:

- `GET /` returns a simple service message.
- `GET /all` returns all tasks.
- `GET /last` returns the latest task.
- `GET /task/{id}` returns a task by identifier.

This is useful for:

- lightweight external reads;
- attaching a simple frontend;
- local bot or automation integration;
- checking SQLite-backed task data over HTTP.

Current API limits:

- no full write API surface;
- the committed OpenAPI description is minimal;
- the contract should not yet be considered stable.

## Local Data and Logs

- SQLite files live in `src/data/`.
- The sample SQL dump is stored in `src/data/sqlite-example-data-db-utf-8.sql`.
- CLI logs are written to `src/log/todo_cli.log`.

The project is fully local: no separate DB server, no message broker, no cloud dependency.

## Tests

The repository includes tests for three layers:

- `tests/test_db_working.py` validates DB creation, insert, update, and delete behavior.
- `tests/test_cli.py` validates CLI startup and expected command-line options.
- `tests/test_api.py` validates basic FastAPI routes and `TestClient` behavior.

Practical test value:

- keeping the CRUD core from regressing;
- detecting CLI argument changes quickly;
- protecting the minimal API surface from accidental breakage.

Honest constraint: part of the test execution depends on the local environment, especially the state of `uv` and write access to cache directories.

## FAQ and Common Issues

### Why can the CLI work while `test_cli.py` fails?

The current test prefers `uv run` if `uv` is available in `PATH`. If the local `uv` cache is broken or inaccessible, the test can fail before the application itself starts.

### Where is the database file stored?

By default, the database is created in `src/data/` with the name `todo_main.db`.

### Can I override the database name?

Yes. Use the `TODO_DB_NAME` environment variable.

### Is this a production-ready API?

No. The current state is better described as an `MVP` with a working CLI and an experimental API.

### Is there a local simulator or dev server?

There is no separate simulator. The local development flow is based on:

- SQLite with a bundled sample SQL dump;
- a locally started FastAPI server;
- API tests that use `TestClient`.

## MVP Limitations

- no clean separation into domain model, service layer, and transport layer;
- string-based dates instead of a stricter normalized schema;
- API is mostly read-oriented;
- some CLI actions are interactive, which is inconvenient for automation;
- configuration is minimal and partly tied to the repository layout;
- full test reproducibility depends on the local environment;
- no web UI, multi-user mode, auth, or sync.

## Further Development

Logical next steps:

1. Stabilize the API contract and add write operations.
2. Replace string dates with a more explicit data model.
3. Separate business logic, persistence, and presentation concerns.
4. Add a non-interactive CLI mode suitable for CI and automation.
5. Expand the OpenAPI description and normalize API responses.
6. Improve config handling and path resolution.
7. Add a web UI if the project scope grows beyond local CLI usage.

## Release Documents

- Russian documents: [CHANGELOG.md](./CHANGELOG.md), [RELEASE_NOTES.md](./RELEASE_NOTES.md), [RELEASE_PAGE.md](./RELEASE_PAGE.md)
- English documents: [CHANGELOG.en.md](./CHANGELOG.en.md), [RELEASE_NOTES.en.md](./RELEASE_NOTES.en.md), [RELEASE_PAGE.en.md](./RELEASE_PAGE.en.md)

## License

The project is distributed under the `Apache License 2.0`.

Why this is a reasonable choice here:

- it is already used in the repository;
- it fits a practical software project that may be reused and modified later;
- it avoids custom restrictions and works well with a normal open-source workflow.

Full license texts:

- [LICENSE](./LICENSE)
- [LICENSE-ru](./LICENSE-ru)
- [LICENSE-en](./LICENSE-en)

Usage summary:

- you may use, modify, and redistribute the code;
- you must preserve the license text and copyright notices;
- the project is provided `AS IS`, without warranties.
