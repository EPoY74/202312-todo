import os
import sys
import sqlite3 as sql3
from typing import List

import configparser as cfg_par

from logging_config import logger  # переместил настройки логирования в отдельный файл


def search_config_and_db():  # Ищем конфигурацию и БД,если нет - создаем
    logger.info("search_config_and_db(): Запуск")
    """
    Функция ищет файл конфигурации и файл БД, если отсутствует(первый запуск,допустим),
    то создает их.
    Возвращает объект с  файлом конфигурации
    """
    # TODO А правильно написал? Спросить у Славы
    full_prog_name = str(sys.argv[0])  # Читаю полное имя файла
    prog_name = full_prog_name[0:full_prog_name.rfind(".")]  # Получаю имя скрипта без точки
    # prog_name = full_prog_name[0:full_prog_name.rfind(".")]  # Получаю имя скрипта без точки
    ini_file_name = str(prog_name + ".ini")  # Формирую имя файла конфигурации
    db_file_name = str(prog_name + ".db")  # Формирую имя БД

    # TODO: Done Проверить, так ли я понял документацию. понял, что todo_config_obj - должен
    #  содержать файл конфигурации

    todo_config_obj = cfg_par.ConfigParser()  # Сoздаю объект класса парсера конфигурации
    todo_config = todo_config_obj.read(ini_file_name)  # Читаю конфигурацию

    if len(todo_config) == 0:
        if not os.path.isfile(db_file_name):
            print("БД не создана")
        is_confirm = input(f"Создать базу данных {db_file_name}? y/n ")
        if is_confirm.upper() == "Y":
            make_db(db_file_name)

        elif is_confirm.upper() == "N":
            print("Отменяю создание базы данных")
            exit(1)
        else:
            print('Вы ввели не корректное значение. Введите "y" или "n"!')
            exit(1)

        print(f"\nфайл конфигурации {ini_file_name} не найден")
        is_confirm = input(f"Создать файл конфигурации {ini_file_name}? y/n ")
        if is_confirm.upper() == "y" or is_confirm == "Y":

            create_config_file(ini_file_name, db_file_name)
        elif is_confirm.upper() == "n":
            print("Отменяю создание файла конфигурации")
            exit(1)
        else:
            print('Вы ввели не корректное значение. Введите "y" или "n"!')
            exit(1)
    return todo_config_obj


def create_config_file(ini_file_name: str, db_name: str):  # Создаю файл конфигурации

    print("\n\nСоздаю файл конфигурации...")
    todo_config = cfg_par.ConfigParser()
    todo_config.add_section("db_cfg")
    # cfg_record = str("db_name = " + db_name)
    todo_config.set("db_cfg", "db_name", db_name)

    with open(ini_file_name, "w") as cfg_file:
        todo_config.write(cfg_file)
    print("Файл конфигурации создан успешно!")
    exit(0)


def make_db(db_name_new: str):  # Создаю БД, если её нет
    """
    Создаем основную базу данных для работы приложения.
    Создаем основную таблицу для работы приложения
    """
    # создаем БД
    if not db_name_new:
        raise ValueError("Надо передать db_new_new")

    try:
        print("\n\nСоздаю базу данных...")
        with sql3.connect(db_name_new) as db_connection:
            print("База данных создана\n")
        db_connection.close()
    except sql3.Error as err:
        print(f"Ошибка:\n {str(err)}")

    # Записываем таблицу, если не создана
    try:
        with sql3.connect(db_name_new) as db_connection:
            print("Создаю таблицу для ToDo заданий в Базе Даннах")
            db_cursor = db_connection.cursor()
            db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS my_todo_list(
            id INTEGER PRIMARY KEY,
            data_of_creation,
            date_max TEXT,
            todo_text TEXT,
            is_gone integer,
            date_of_gone TEXT
            )
            ''')
        print("Таблица в базе данных создана успешно\n")
        print("База данных создана и подготовлена к работа.")
    except sql3.Error as error:
        print(f"Ошибка:\n  {str(error)}")


def get_db_name(config_obj):  # Беру имя БД из переменной окружения TODO_DB_NAME, если она есть
    """
    Получает имя базы из переменной окружения TODO_DB_NAME.
    Если такой переменной нет, то имя базы будет eo20231206sql.db.
    """

    dbname = os.getenv("TODO_DB_NAME")
    if dbname is not None:
        print(f"Используем имя базы из переменной TODO_DB_NAME - {dbname}")
    return dbname if dbname is not None else str(config_obj["db_cfg"]["db_name"])


def work_with_data(type_of_sql: str, is_one: str, db_sql_query: str, db_sql_data: tuple = ()) -> List[sql3.Row]:
    # isGone Далаем запись в БД
    """
    Выполняет запрос в базу данных. Если указана только БД и запрос - то выполняем только его
    Если указан БД, запрос и данные - то выполняем и данные и запрос.
    Если записи не существует - то выводим сообщение
    DB_NAME - Имя базы данных
    db_sql_query - SQL запрос к базе данных
    db_slq_data - передаваемые параметры в SQL запрос (необязательный)
    type_of_sql - тип SQL ,запись или чтение (read, write), если нужно закомитить в БД,то выбирать write

    Возвращает результат запроса
    #TODO -done- Уточнить у Славы, кмк за такое, что разные типы возвращает, дают по рукам :))


    Возвращает результат запроса
    """
    global DB_NAME

    logger.info("work_with_slq(): Запуск")

    db_name_rw = "file:" + DB_NAME + "?mode = rw"

    logger.debug(f"work_with_slq(): Имя БД: {db_name_rw}")
    logger.debug(f"work_with_slq(): SQL запрос: {db_sql_query}")
    logger.debug(f"work_with_slq(): SQL данные: {db_sql_data}")

    try:
        with sql3.connect(db_name_rw, uri=True) as db_connection:
            db_connection.row_factory = sql3.Row
            db_cursor = db_connection.cursor()

            logger.debug("work_with_slq(): Подключился к БД, Получил курсор, Выполняю SQL запрос ")
            db_return_temp = db_cursor.execute(db_sql_query, db_sql_data)

            if is_one == "one":
                db_return = db_return_temp.fetchone()

            if is_one == "many":
                db_return = db_return_temp.fetchall()

            if type_of_sql == "read" and len(db_return) == 0:
                print("Запись с таким номером в БД отсутствует.")
                logger.error("work_with_slq(): Запись с таким номером в БД отсутствует.")
                return []

            if type_of_sql == "write":
                db_connection.commit()
        # else:
    except sql3.Error as err:
        print(f"Ошибка: {err}")
        logger.error("work_with_slq(): Упс!!!", exc_info=err)

    return db_return


def query_for_data(name_of_foo: str) -> str:
    logger.info("query_for_data(): Запуск")

    if name_of_foo == 'delete_task':
        return '''DELETE FROM  my_todo_list WHERE id='''

    elif name_of_foo == 'is_can_edit':
        return '''SELECT is_gone, date_of_gone FROM  my_todo_list WHERE id=?'''

    elif name_of_foo == 'make_task':
        # Этот вариант рабочий
        return '''INSERT INTO my_todo_list (data_of_creation, todo_text, is_gone) VALUES (?, ?, ?)'''
        # Просто я решил попробовать так - и взлетело upd: не взлетело - перезаписало всю таблицу!

    elif name_of_foo == "set_tasks_deadline":
        return '''UPDATE my_todo_list SET date_max=? WHERE id=?'''

    else:
        print("Запрос не может быть сформирован")
        exit(1)


# Это одна из немногих, переменных, которые будут глобальными. Мог бы сделать без нее, считывая
# каждый раз имя БД с конфигурации, но, что бы избежать подмены - решил сделать одну переменную глобальной
DB_NAME = get_db_name(search_config_and_db())
