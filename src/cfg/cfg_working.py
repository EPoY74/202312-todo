"""
Функции для работы с конфигуратором
"""

import configparser as cfg_par
import os
import typing

from src.cfg.logger_config import logger
from src.db_access.db_working import make_db


def search_config_and_db(name_exicting_db: str = "") -> cfg_par.ConfigParser:
    """
    Функция ищет файл конфигурации и файл БД,
     если отсутствует(первый запуск,допустим),
    то создает их.
    Возвращает объект с  содержимым файла конфигурации cfg_par.ConfigParser
    """

    # Использую переменнут чтобы линтер не ругался.
    # Не учел, что можно использовать БД с другим именем
    logger.debug(name_exicting_db)

    prog_name: str = "todo_main"

    # Формирую имя файла конфигурации
    ini_config_name = "todo_config.ini"
    file_directory: str = os.path.dirname(__file__)
    config_file_path: str = os.path.join(
        file_directory, "..", "..", "src", "cfg", ini_config_name
    )
    logger.debug("cfg_working: %s", config_file_path)

    # Формирую имя БД
    db_name = str(prog_name + ".db")
    db_path: str = os.path.join(
        file_directory, "..", "..", "src", "data", db_name
    )
    logger.debug("cfg_working: %s", db_path)

    config_obj = cfg_par.ConfigParser()

    # задаю объект парсера конфигурации
    # Читаю конфигурацию
    todo_config = config_obj.read(config_file_path)

    if len(todo_config) == 0:
        if not os.path.isfile(db_path):
            logger.error("БД не создана")
        is_confirm = input(f"Создать базу данных {db_name}? y/n ")
        if is_confirm.upper() == "Y":
            make_db(db_path)

        elif is_confirm.upper() == "N":
            logger.warning("Отменяю создание базы данных")
            exit(1)
        else:
            logger.warning(
                'Вы ввели не корректное значение. Введите "y" или "n"!'
            )
            exit(1)

        logger.error(f"\nфайл конфигурации {ini_config_name} не найден")
        is_confirm = input(f"Создать файл конфигурации {ini_config_name}? y/n ")
        if is_confirm.upper() == "y" or is_confirm == "Y":
            create_config_file(config_file_path, db_name)
        elif is_confirm.upper() == "n":
            logger.error("Отменяю создание файла конфигурации")
            exit(1)
        else:
            logger.warning(
                'Вы ввели не корректное значение. Введите "y" или "n"!'
            )
            exit(1)
    return config_obj


def create_config_file(
    ini_file_name: str, db_name: str
) -> typing.NoReturn:  # Создаю файл конфигурации
    """Создает файл конфигурации

    Args:
        ini_file_name (str): Имя файла конфигурации??? Сам забыл уже
        db_name (str): Имя базы данных
    """

    logger.info("\n\nСоздаю файл конфигурации...")
    todo_config = cfg_par.ConfigParser()
    todo_config.add_section("db_cfg")
    todo_config.set("db_cfg", "db_name", db_name)

    with open(ini_file_name, "w", encoding="utf-8") as cfg_file:
        todo_config.write(cfg_file)
    logger.info("Файл конфигурации создан успешно!")
    exit(0)
