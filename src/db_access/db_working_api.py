"""Модуль работы с SQLite ри обрабтке запросов через API
Автор: Евгений Петров
Почта: p174@ mail.ru
Since: 05.10.2024
"""
from typing import List
import sqlite3
import json
import os

from fastapi import Response

from src.cfg.logger_config import logger


def get_db_name(todo_config_obj_def):

    # TODO РАзобраться с путями и подключением к БД в api части
    """
    Получает имя базы из переменной окружения TODO_DB_NAME.
    Если такой переменной нет, то имя базы будет eo20231206sql.db.
    """
    dbname = os.getenv("TODO_DB_NAME")
    if dbname is not None:
        print(f"Используем имя базы из переменной TODO_DB_NAME - {dbname}")
    return dbname if dbname is not None else str(todo_config_obj_def["db_cfg"]["db_name"])


def list_of_tasks_json(db_name: str,
                  all_or_last: str = "all",
                  id_row : int = 0):
    """
    Выводим список дел из SQLite в виде json.
    Если задан параметр all - выводим все записи, указана по умолчанию.
    ЕСли задан параметр last - то только последнюю запись  
    Если задан переметр one  - выводим одну запись, номер задаем третьим пареметром
    """

    # выводим списк дел.
    logger.info("API: list_of_tasks_json(): Запуск")

    # Формируем SQL запрос на одну запись, на последнюю или на все.
    # check all_or_last for valid value
    if all_or_last != "all" and all_or_last != "last" and all_or_last != "one":
        logger.error("list_of_tasks(): Передан некорректный параметр all_or_last")
        print("Передан некорректный параметр all_or_last")
        exit(1)

    data_of_todo: Response = Response(content="", media_type="application/json")

    try:
        if all_or_last == "last":
            logger.debug("API: list_of_tasks_json() Получаю последнюю запись из БД")
            data_of_todo = get_last_record_api(db_name)

        elif all_or_last == "all":
            logger.debug("API: list_of_tasks_json() Получаю все записи из БД")
            data_of_todo = get_all_records_api(db_name)

        elif all_or_last == "one":
            logger.debug("API: list_of_tasks_json() Получаю одну запись из БД # %d", id_row)
            data_of_todo = get_record_by_id_api(db_name, id_row)

        return data_of_todo #todo_table

    except sqlite3.Error as err:
        logger.error("Ой!", exc_info=err)
        print(f"Ошибка: \n{str(err)}")


def work_with_slq_api(db_name_def_worrk_with_sql: str,
                  type_of_sql: str,
                  is_one: str,
                  db_sql_query: str,
                  db_sql_data: tuple = () ) -> Response:
    """
    API: Выполняет запрос в базу данных. Если указаана только БД 
    и запрос - то выполняем только его
    Если укзазан БД, запрос и данные - то выполняем и данные и запрос.
    Если записи не существует - то выводим сообщение
    DB_NAME - Имя базы данных
    db_sql_query - SQL запоос к базе данных
    db_slq_data - передаваемые параметры в SQL запрос (необязательный)
    type_of_SQL - тип SQL ,запись или чтение (read, write),
    если нужно закомитить в БД,то выбирть write
    
    Возвращает результат запроса, если он есть
    Если запись отсутствует,то выход с кодом одит и return -1
    Возвращает результат запроса
    """

    logger.info("API: work_with_slq_api(): Запуск")

    db_return: List = []
    data: List =[]

    db_name_rw = "file:" + db_name_def_worrk_with_sql + "?mode = rw"

    logger.debug("API: work_with_slq_api(): Имя БД: %s ", db_name_rw)
    logger.debug("API: work_with_slq_api(): SQL запрос: %s", db_sql_query)
    logger.debug("API: work_with_slq_api(): SQL данные: %s", db_sql_data)

    try:
        with sqlite3.connect(db_name_rw, uri = True) as db_connection:
            db_connection.row_factory = sqlite3.Row
            db_cursor = db_connection.cursor()

            logger.debug("""API: work_with_slq(): Подключился к БД,
                          Получил курсор, Выполняю SQL запрос""")
            db_return_temp = db_cursor.execute(db_sql_query, db_sql_data)

            if is_one == "one":
                db_return = db_return_temp.fetchone()
                # Получаем название столбцов из курсора
                columns = [col[0] for col in db_cursor.description]

                # Объединяем оба массива (это zip) и создаем из него словарь (это dict),
                # чтобы получить пары ключ: значение
                data = [dict(zip(columns, row)) for row in db_return]

            if is_one == "many":
                # Получаем все данные из таблицы
                db_return = db_return_temp.fetchall()

                # Получаем название столбцов из курсора
                columns = [col[0] for col in db_cursor.description]

                # Объединяем оба массива (это zip) и создаем из него словарь (это dict),
                # чтобы получить пары ключ: значение
                data = [dict(zip(columns, row)) for row in db_return]

            if type_of_sql == "read" and len(db_return) == 0:
                print("API: Запись с таким номером в БД отсутсвует.")
                logger.error("API: work_with_slq(): Запись с таким номером в БД отсутствует.")
                data = list("None")

            if type_of_sql == "write":
                db_connection.commit()

    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
        logger.error("API: work_with_slq(): Упс!!! %s", exc_info=err)

    # Этот вариант тоже рабочий, но он выводит возвращает не отформатированный код
    # return JSONResponse(content=data)

    # Преобразовываем все дело в json.
    # Оказалось преобразоваывать в json не нужно,
    # так как fastAPI автоматически ПРЕОБРАЗОВЫВАЕТ ВОЗВРАЩАЕМОЕ ЗНАЧЕНИЕ в json
    to_json = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True, default=str)

    # Возвращает отформатированный код
    return Response(content=to_json, media_type='application/json')


def get_last_record_api(db_name):
    """
    Автор: Евгений Петров, Челябинск,
    Возвращает последнюю запись из БД
    """
    logger.info("API get_last_record_api(): Get last record from DB")
    db_sql_query = """SELECT *
                      FROM  my_todo_list
                      ORDER BY id 
                      DESC LIMIT 1
                    """
    executed_sql_query = work_with_slq_api(db_name, "read", "many", db_sql_query)  # Новая функция
    return executed_sql_query


def get_all_records_api(db_name):
    """
    Автор: Евгений Петров, Челябинск,
    Возвращает все записи из БД
    Parameters: db_name - имя базы данных, с которой работаем

    """
    logger.info("API get_all_records_api(): Get all records from DB")
    db_sql_query = "SELECT * FROM  my_todo_list"
    executed_sql_query = work_with_slq_api(db_name, "read", "many", db_sql_query)
    return executed_sql_query


def get_record_by_id_api(db_name, id_row):
    """
    Автор: Евгений Петров, Челябинск,
    Возвращает запись с номером id_row из БД
    """
    logger.info("API: get_record_by_id_api(): Get one record #%d from DB", id_row)
    db_sql_query = "SELECT * FROM  my_todo_list WHERE id=?"
    db_sql_parametr =  (id_row,)
    executed_sql_query = work_with_slq_api(db_name, "read", "many", db_sql_query, db_sql_parametr)
    return executed_sql_query
