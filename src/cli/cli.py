# SPDX-License-Identifier: Apache-2.0
"""
Реализация CLI интерфейса для todo листа

Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""

import argparse as ap
import os

from src.cfg.cfg_working import search_config_and_db
from src.cfg.logger_config import logger
from src.db_access.db_working import (
    delete_task,
    get_db_name,
    list_of_tasks,
    make_db,
    make_task,
    set_tasks_deadline,
    task_completed,
)


def main_body(db_full_path: str) -> None:
    """
    Автор: Евгений Б. Петров, Челябинск, p174@mail.ru
    Выполняет основную логику консольного приложения:
      считывает параметры из командной строки
    и вызывает соответствующую процедуру.
    Ничего не возвращает.
    """
    logger.info("CLI main_body(): Запуск")
    parser = ap.ArgumentParser()
    parser.description = (
        "Програма создает ToDo список дел в текстовом консольном режиме."
    )
    parser.add_argument(
        "--create_db",
        help="Создаем базу данных для списка задач",
        action="store_true",
    )
    parser.add_argument(
        "--task_add",
        type=str,
        help="""Описание задачи, которую заводим: --task_add \"Это запись\" """,  # noqa
    )
    parser.add_argument(
        "--deadline_at",
        type=int,
        help="""Устанавлявает дату, до которой надо выполнить задание:
                        --deadline_at номер_записи""",
    )
    parser.add_argument(
        "--tasks_list", help="Выводит список задач", action="store_true"
    )  # И где написано про action интересно?
    parser.add_argument(
        "--completed_at",
        type=int,
        help="""Помечает задание с номером № завершенным. Дата и время завершения - текущие:
                        --completed_at номер_записи""",  # noqa
    )
    parser.add_argument(
        "--task_del_id",
        type=int,
        help="""Удаляет запись с номером: --task_del_id номер_записи""",
    )

    args = parser.parse_args()

    if args.create_db:
        logger.warning("CLI main_body: Пользователь запросил создание БД")
        make_db(db_full_path)
    elif args.task_add:
        make_task(db_full_path, args.task_add)
    elif args.deadline_at:
        set_tasks_deadline(db_full_path, args.deadline_at)
    elif args.tasks_list:
        list_of_tasks(db_full_path, "all")
    elif args.completed_at:
        task_completed(db_full_path, args.completed_at)
    elif args.task_del_id:
        delete_task(db_full_path, args.task_del_id)
    else:
        printing_help()
        logger.warning(
            "CLI main_body: Пользователь не указал ни одной команды."
        )
        exit(0)


def printing_help():
    # _summary_ Выводит доступные команды на экран,
    #  так как мне надо, а не так как придется
    logger.info("CLI printing_help(): Запуск. Вывод помощи на экран")
    print("Основные команды консольного ToDo приложения:")  # noqa
    print("--create_db:\n" + "\t Создаем базу данных для списка задач")  # noqa
    print("--tasks_list:\n" + "\tВыводит список задач")  # noqa
    print(  # noqa
        "--task_add: \n"
        + "\tОписание задачи, которую заводим:\n"
        + '\t --task_add "Это запись" '
    )
    print(  # noqa
        "--deadline_at: \n"
        + "\tУстанавлявает дату, до которой надо выполнить задание:\n"
        + "\t--deadline_at номер_записи"
    )
    print("--tasks_list:\n" + "\tВыводит список задач")  # noqa
    print(  # noqa
        "--completed_at:\n"
        + "\tпечает задание с номером № завершенным. "
        + "Дата и время завершения - текущие:\n"
        + "\t--completed_at номер_записи"
        ""
    )
    print(  # noqa
        "--task_del_id:\n"
        + "\tУдаляет запись с номером:\n"
        + "\t --task_del_id номер_записи\n"
    )


def main() -> None:
    """
    Для запуска через имя модуля
    """

    logger.info("CLI main(): Запуск src.cli приложения.")
    print("""\nКонсольное приложение для ведения задач.
          \nАвтор: Евгений Б. Петров, p174@mail.ru\n""")  # noqa
    #  Принимаю объект с файлом конфигурации,
    # что бы избавится от глобальной переменной
    todo_config_obj = search_config_and_db()

    db_name_from_config: str = get_db_name(todo_config_obj)
    logger.info(
        "CLI main(): DB name from config in variable db_name_main_read: %s ",
        db_name_from_config,
    )
    file_directory: str = os.path.dirname(__file__)
    db_full_path: str = os.path.join(
        file_directory, "..", "..", "src", "data", db_name_from_config
    )
    logger.info(
        "CLI main(): DB name for working  "
        + "  cli app in variable db_file_name_path: %s ",
        db_full_path,
    )
    logger.debug("cli: %s", db_full_path)

    main_body(db_full_path)


if __name__ == "__main__":
    main()
    logger.info("Конец выполнения консольного ToDo приложения.")
