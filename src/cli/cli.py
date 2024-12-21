"""
Реализация CLI интерфейса для todo листа

Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""
# import sys
import os
import argparse as ap
import dotenv

from src.cfg.cfg_working import search_config_and_db
from src.db_access.db_working import (delete_task,
                        get_db_name,
                        list_of_tasks,
                        set_tasks_deadline,
                        task_done,
                        make_db,
                        make_task)
from src.cfg.logger_config import logger


def main_body(db_name_main_def: str):
    """
    Автор: Евгений Б. Петров, Челябинск, p174@mail.ru
    Выполняет основную логику консольного приложения: считывает параметры из командной строки
    и вызывает соответствующую процедуру.
    Ничего не возвращает.
    """
    parser = ap.ArgumentParser()
    parser.description = "Програма создает ToDo список дел в текстовом консольном режиме."
    parser.add_argument("--create_db",
                        help = "Создаем базу данных для списка задач",
                        action="store_true")
    parser.add_argument("--task_add",
                        type = str,
                        help = '''Описание задачи, которую заводим: --task_add \"Это запись\" ''')
    parser.add_argument("--task_deadline",
                        type = int, help = """Устанавлявает дату, до которой надо выполнить задание:
                        --task_deadline номер_записи""")
    parser.add_argument("--task_list",
                        help = "Выводит список задач",
                        action="store_true")  # И где написано про action интересно?
    parser.add_argument("--task_done_date",
                        type = int,
                        help = """Помечает задание с номером № завершенным:
                        --set_done_date номер_записи""")
    parser.add_argument("--task_del_id",
                        type = int,
                        help = """Удаляет запись с номером: --task_del_id номер_записи""" )

    args = parser.parse_args()

    if args.create_db:
        make_db("test.db")
    elif args.task_add:
        make_task(db_name_main_def, args.task_add)
    elif args.task_deadline:
        set_tasks_deadline(db_name_main_def, args.task_deadline)
    elif args.task_list:
        list_of_tasks(db_name_main_def, "all")
    elif args.task_done_date:
        task_done(db_name_main_def, args.task_done_date)
    elif args.task_del_id:
        delete_task(db_name_main_def, args.task_del_id)


def printing_help():
    """_summary_ Выводит доступные команды на экран, так как мне надо, а не так как придетс я
    """
    print("Основные команды консольного ToDo приложения:")
    print("--create_db: Создаем базу данных для списка задач")
    print("--task_add: Описание задачи, которую заводим: --task_add \"Это запись\" ")
    print("""--task_deadline: Устанавлявает дату, до которой
    надо выполнить задание: --task_deadline номер_записи""")
    print("--task_list: Выводит список задач")
    print("""--task_done_date: Помечает задание с номером № завершенным:
    --task_done_date номер_записи""")
    print("--task_del_id: Удаляет запись с номером: --task_del_id номер_записи\n" )

def main():
    """
    Для запуска через имя модуля
    """
     #Загружаю переменные окружения из локального окружение текущего проекта
    dotenv.load_dotenv()

    logger.info("Запуск приложения.")
    print("""\nКонсольное приложение для ведения задач.
          \nАвтор: Евгений Б. Петров, p174@mail.ru\n""")
    #  Принимаю объект с файлом конфигурации, что бы избавится от глобальной переменной
    todo_config_obj =  search_config_and_db()

    db_name_main_read: str = get_db_name(todo_config_obj)
    # inner_for_search_db_file_name = str(prog_name + ".db")
    file_directory:str = os.path.dirname(__file__)
    db_file_name_path:str = os.path.join(
        file_directory,
        '..', '..',
        'src', 'data', db_name_main_read
    )
    print("cli: ", db_file_name_path)


    logger.info("Старт консольного ToDo приложения.")
    printing_help()
    main_body(db_file_name_path)

    # FULL_PROG_NAME = str(sys.argv[0])  # pylint: disable=invalid-name
    # PROG_NAME = FULL_PROG_NAME[0:FULL_PROG_NAME.find(".")]  # pylint: disable=invalid-name
    logger.info("Конец выполнения консольного ToDo приложения.")


if __name__ == "__main__":
    main()
