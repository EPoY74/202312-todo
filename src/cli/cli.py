"""
Реализация CLI интерфейса для todo листа

Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""

import os
import argparse as ap
# import dotenv

from src.cfg.cfg_working import search_config_and_db
from src.db_access.db_working import (
    delete_task,
    get_db_name,
    list_of_tasks,
    set_tasks_deadline,
    task_complited,
    make_db,
    make_task,
)
from src.cfg.logger_config import logger


def main_body(db_full_path: str):
    """
    Автор: Евгений Б. Петров, Челябинск, p174@mail.ru
    Выполняет основную логику консольного приложения: считывает параметры из командной строки
    и вызывает соответствующую процедуру.
    Ничего не возвращает.
    """
    logger.info("CLI main_body(): Запуск")
    parser = ap.ArgumentParser()
    parser.description = (
        "Програма создает ToDo список дел в текстовом консольном режиме."
    )
    parser.add_argument(
        "--create_db", help="Создаем базу данных для списка задач", action="store_true"
    )
    parser.add_argument(
        "--task_add",
        type=str,
        help="""Описание задачи, которую заводим: --task_add \"Это запись\" """,
    )
    parser.add_argument(
        "--task_deadline",
        type=int,
        help="""Устанавлявает дату, до которой надо выполнить задание:
                        --task_deadline номер_записи""",
    )
    parser.add_argument(
        "--task_list", help="Выводит список задач", action="store_true"
    )  # И где написано про action интересно?
    parser.add_argument(
        "--task_done_date",
        type=int,
        help="""Помечает задание с номером № завершенным:
                        --task_done_date номер_записи""",
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
    elif args.task_deadline:
        set_tasks_deadline(db_full_path, args.task_deadline)
    elif args.task_list:
        list_of_tasks(db_full_path, "all")
    elif args.task_done_date:
        task_complited(db_full_path, args.task_done_date)
    elif args.task_del_id:
        delete_task(db_full_path, args.task_del_id)
    else:
        printing_help()
        logger.warning("CLI main_body: Пользователь не указал ни одной команды.")
        exit(0)


def printing_help():
    """_summary_ Выводит доступные команды на экран, так как мне надо, а не так как придетс я"""
    logger.info("CLI printing_help(): Запуск. Вывод помощи на экран")
    print("Основные команды консольного ToDo приложения:")
    print("--create_db: Создаем базу данных для списка задач")
    print('--task_add: Описание задачи, которую заводим: --task_add "Это запись" ')
    print("""--task_deadline: Устанавлявает дату, до которой
    надо выполнить задание: --task_deadline номер_записи""")
    print("--task_list: Выводит список задач")
    print("""--task_done_date: Помечает задание с номером № завершенным:
    --task_done_date номер_записи""")
    print("--task_del_id: Удаляет запись с номером: --task_del_id номер_записи\n")


def main():
    """
    Для запуска через имя модуля
    """
    # Загружаю переменные окружения из локального окружение текущего проекта
    # dotenv.load_dotenv()

    logger.info("CLI main(): Запуск src.cli приложения.")
    print("""\nКонсольное приложение для ведения задач.
          \nАвтор: Евгений Б. Петров, p174@mail.ru\n""")
    #  Принимаю объект с файлом конфигурации, что бы избавится от глобальной переменной
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
        "CLI main(): DB name for working in cli app in variable db_file_name_path: %s ",
        db_full_path,
    )
    print("cli: ", db_full_path)

    main_body(db_full_path)


if __name__ == "__main__":
    main()
    logger.info("Конец выполнения консольного ToDo приложения.")
