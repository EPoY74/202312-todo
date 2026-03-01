[Русская версия](./RELEASE_NOTES.md) | [English version](./RELEASE_NOTES.en.md)

Related documents: [README.md](./README.md) | [README.en.md](./README.en.md) | [CHANGELOG.md](./CHANGELOG.md) | [CHANGELOG.en.md](./CHANGELOG.en.md) | [RELEASE_PAGE.md](./RELEASE_PAGE.md) | [RELEASE_PAGE.en.md](./RELEASE_PAGE.en.md)

# RELEASE NOTES

## Version 0.1.0

Release date: `2026-02-28`

## What is included

Version `0.1.0` captures the first coherent baseline of `202312-todo`: a local Python-based todo manager with SQLite storage, a working CLI, and a minimal FastAPI REST API.

This release includes:

- a CLI for core task operations;
- a local SQLite database without requiring a separate DB server;
- create, list, complete, and delete task flows;
- deadline support;
- a minimal HTTP API for reading tasks;
- `.ini`-based configuration;
- CLI logging;
- tests and sample data for local verification.

## Why it matters

The value of this release is not breadth. Its value is that the project already solves a practical problem without extra infrastructure. For local task tracking, it is enough to have:

- one repository;
- one SQLite file;
- a standard Python environment;
- a simple CLI.

That makes it a useful base for personal use, FastAPI experiments, and future evolution into a more formal task manager.

## Practical value

This release is useful in several real scenarios:

- keeping a local task list without a web UI or cloud dependency;
- validating Python + SQLite CRUD behavior quickly;
- using the project as a base for a lightweight REST API;
- evolving it into a personal productivity CLI tool.

## Technical highlights

- The main usable workflow currently goes through the CLI.
- The API is already usable for HTTP reads.
- The data model is intentionally simple: one task table with creation date, deadline, completion flag, and completion timestamp.
- The project remains compact and easy to debug locally.

## Release limitations

Release `0.1.0` should not be described as production-ready.

Current limits:

- the API is limited and should not be treated as a stabilized contract;
- dates are string-based and primarily shaped for CLI usage;
- some CLI operations are interactive and require confirmation;
- the architecture is closer to a practical MVP than to a fully formalized application;
- part of test reproducibility depends on the local environment, especially `uv`.

## What should come next

The most logical next steps are:

1. Stabilize the API and add write operations.
2. Make CLI automation easier by reducing interactive requirements.
3. Improve data-model formalization and date handling.
4. Expand the test setup so it depends less on the environment.
5. Add a web UI or external client if the project scope grows.

## License

The project is distributed under the `Apache License 2.0`.

In practical terms:

- the code may be used and modified;
- license and copyright notices must be preserved when redistributing;
- the software is provided without warranties.

Full license texts: [LICENSE](./LICENSE), [LICENSE-ru](./LICENSE-ru), [LICENSE-en](./LICENSE-en)
