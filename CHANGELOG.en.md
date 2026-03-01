[Русская версия](./CHANGELOG.md) | [English version](./CHANGELOG.en.md)

Related documents: [README.md](./README.md) | [README.en.md](./README.en.md) | [RELEASE_NOTES.md](./RELEASE_NOTES.md) | [RELEASE_NOTES.en.md](./RELEASE_NOTES.en.md) | [RELEASE_PAGE.md](./RELEASE_PAGE.md) | [RELEASE_PAGE.en.md](./RELEASE_PAGE.en.md)

# CHANGELOG

All notable changes to the `202312-todo` project are documented in this file.

The format is close to Keep a Changelog. At the current stage, versioning is effectively based on the value defined in `pyproject.toml`.

## [0.1.0] - 2026-02-28

### Added

- A basic CLI for task management through command-line arguments.
- Local SQLite storage for the `my_todo_list` table.
- Operations for creating, listing, updating task state, and deleting tasks.
- Deadline support for tasks.
- A FastAPI application with `/`, `/all`, `/last`, and `/task/{id}` routes.
- Configuration through `src/cfg/todo_config.ini`.
- CLI file logging.
- A sample SQL dump and a database initialization script.
- Tests for the DB layer, CLI, and API.
- A bilingual set of project and release documentation.

### Changed

- The README was rewritten to describe the project honestly as an `MVP`.
- The documentation now clearly separates the working CLI path from the experimental API layer.
- License sections and cross-links across documents were unified into a consistent style.

### Fixed

- No separate completed bug-fix items were confirmed as release-level work for this version.

### Notes

- Version `0.1.0` represents an early but already usable working baseline.
- At the time the release documents were prepared, part of test reproducibility depended on the local environment, especially `uv` cache state and cache-directory write permissions.
