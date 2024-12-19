"""Функции для работы с конфигуратором

Returns:
    _type_: _description_
"""


import os
import sys

import configparser as cfg_par
from db_working import make_db


def search_config_and_db(name_exicting_db: str = None ):
    """
    Функция ищет файл конфигурации и файл БД, если отсутствует(первый запуск,допустим),
    то создает их.
    Возвращает объект с  файлом конфигурации
    #TODO А правильно написал? Спросить у Славы
    """

    # Использую переменнут чтобы линтер не ругался.
    # Не учел, что можно использовать БД с другим именем
    print(name_exicting_db)
    # Читаю полное имя файла
    full_prog_name: str = str(sys.argv[0])

    # Получаю имя скрипта без точки
    prog_name: str = full_prog_name[0:full_prog_name.rfind(".")]

    # Формирую имя файла конфигурации

    # старая версия
    # inner_for_search_ini_file_name = str(prog_name + ".ini")

    #Новая версия - жесткое имя конфгурационного файла
    inner_for_search_ini_file_name = "todo_config.ini"

    # Формирую имя БД
    inner_for_search_db_file_name = str(prog_name + ".db")

    inner_for_search_todo_config_obj = cfg_par.ConfigParser()

    # задаю объект парсера конфигурации
    # Читаю конфигурацию
    todo_config = inner_for_search_todo_config_obj.read(
        inner_for_search_ini_file_name
        )

    if len(todo_config) == 0:
        if not os.path.isfile(inner_for_search_db_file_name):
            print("БД не создана")
        is_confirm = input(f"Создать базу данных {inner_for_search_db_file_name}? y/n ")
        if is_confirm.upper() == "Y":
            make_db(inner_for_search_db_file_name)

        elif is_confirm.upper() == "N":
            print("Отменяю создание базы данных")
            exit(1)
        else:
            print('Вы ввели не корректное значение. Введите "y" или "n"!')
            exit(1)

        print(f"\nфайл конфигурации {inner_for_search_ini_file_name} не найден")
        is_confirm = input(f"Создать файл конфигурации {inner_for_search_ini_file_name}? y/n ")
        if is_confirm.upper() == "y" or is_confirm == "Y":
            create_config_file(
                inner_for_search_ini_file_name,
                inner_for_search_db_file_name)
        elif is_confirm.upper() == "n":
            print("Отменяю создание файла конфигурации")
            exit(1)
        else:
            print('Вы ввели не корректное значение. Введите "y" или "n"!')
            exit(1)
    return inner_for_search_todo_config_obj



def create_config_file(ini_file_name: str,
                       db_name_for_create_config: str):  # Создаю файл конфигурации
    """Создает файл конфигурации

    Args:
        ini_file_name (str): Имя файла конфигурации??? Сам забыл уже
        db_name_for_create_config (str): Имя базы данных???? Сам забыл уже
    """

    print("\n\nСоздаю файл конфигурации...")
    todo_config = cfg_par.ConfigParser()
    todo_config.add_section("db_cfg")
    todo_config.set("db_cfg", "db_name", db_name_for_create_config)

    with open(ini_file_name, "w", encoding="utf-8") as cfg_file:
        todo_config.write(cfg_file)
    print("Файл конфигурации создан успешно!")
    exit(0)
