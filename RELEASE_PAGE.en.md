[Русская версия](./RELEASE_PAGE.md) | [English version](./RELEASE_PAGE.en.md)

Related documents: [README.md](./README.md) | [README.en.md](./README.en.md) | [CHANGELOG.md](./CHANGELOG.md) | [CHANGELOG.en.md](./CHANGELOG.en.md) | [RELEASE_NOTES.md](./RELEASE_NOTES.md) | [RELEASE_NOTES.en.md](./RELEASE_NOTES.en.md)

# 202312-todo 0.1.0

`202312-todo` is a local Python todo manager with a CLI, SQLite storage, and a minimal FastAPI API. Release `0.1.0` captures a working MVP: core CRUD task operations are available through the console interface, and the API already exposes task reads over HTTP.

## Included in this release

- a CLI for creating, listing, completing, and deleting tasks;
- SQLite storage without a separate DB server;
- deadline support;
- minimal API routes at `/`, `/all`, `/last`, and `/task/{id}`;
- `.ini`-based configuration;
- logging and a basic test setup;
- sample data for local verification.

## Practical value

This release is useful as a compact `python todo app` and `CLI task manager` for local use, and also as a starting point for a future REST API or web UI.

## Limitations

- project status: `MVP`;
- the API is still experimental;
- part of the CLI workflow is interactive;
- reproducibility of some tests depends on the local environment.

## Documentation

- [README.md](./README.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [RELEASE_NOTES.md](./RELEASE_NOTES.md)
- [README.en.md](./README.en.md)
- [CHANGELOG.en.md](./CHANGELOG.en.md)
- [RELEASE_NOTES.en.md](./RELEASE_NOTES.en.md)

## License

`Apache License 2.0`. Full texts: [LICENSE](./LICENSE), [LICENSE-ru](./LICENSE-ru), [LICENSE-en](./LICENSE-en)
