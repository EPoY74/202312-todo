[Русская версия](./RELEASE_PAGE.md) | [English version](./RELEASE_PAGE.en.md)

Связанные документы: [README.md](./README.md) | [README.en.md](./README.en.md) | [CHANGELOG.md](./CHANGELOG.md) | [CHANGELOG.en.md](./CHANGELOG.en.md) | [RELEASE_NOTES.md](./RELEASE_NOTES.md) | [RELEASE_NOTES.en.md](./RELEASE_NOTES.en.md)

# 202312-todo 0.1.0

`202312-todo` это локальный ToDo-менеджер на Python с CLI, SQLite и минимальным FastAPI API. Релиз `0.1.0` фиксирует рабочий MVP: базовые CRUD-операции с задачами доступны через консольный интерфейс, а API уже позволяет читать данные по HTTP.

## Что вошло в релиз

- CLI для создания, просмотра, завершения и удаления задач;
- SQLite-хранилище без отдельного сервера БД;
- поддержка deadline;
- минимальные API-маршруты `/`, `/all`, `/last`, `/task/{id}`;
- конфигурация через `.ini`;
- логирование и тестовый контур;
- примерные данные для локальной проверки.

## Практическая польза

Этот релиз полезен как компактный `python todo app` и `CLI task manager` для локального использования, а также как база для дальнейшего развития REST API или web UI.

## Ограничения

- статус проекта: `MVP`;
- API пока экспериментальный;
- часть сценариев CLI интерактивна;
- воспроизводимость некоторых тестов зависит от локального окружения.

## Документация

- [README.md](./README.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [RELEASE_NOTES.md](./RELEASE_NOTES.md)
- [README.en.md](./README.en.md)
- [CHANGELOG.en.md](./CHANGELOG.en.md)
- [RELEASE_NOTES.en.md](./RELEASE_NOTES.en.md)

## Лицензия

`Apache License 2.0`. Полные тексты: [LICENSE](./LICENSE), [LICENSE-ru](./LICENSE-ru), [LICENSE-en](./LICENSE-en)
