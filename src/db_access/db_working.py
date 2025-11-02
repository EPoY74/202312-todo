"""
Модуль для работы с  базой данный SQLite.
Вынесены все функции, которые обеспечивают
работу todo приложения.
Автор: Евгений Петров
Почта: p174@mail.ru
"""

from datetime import datetime
import os
import sqlite3
from typing import List
from typing import Optional
from configparser import ConfigParser

from prettytable import PrettyTable

from src.db_access.table_working import table_header
from src.cfg.logger_config import logger


def get_db_name(cli_config_obj: ConfigParser):
    """
    Получает имя базы из переменной окружения TODO_DB_NAME.
    Если такой переменной нет, то имя базы будет todo_main.db.
    """
    logger.info("Запуск get_db_name()")
    dbname: Optional[str] = None
    # TODO Проверить, так ли я понял документацию.
    # Понял, что todo_config - должен содержать содержимое файла конфигурации
    dbname = os.getenv("TODO_DB_NAME")
    if dbname is not None:
        logger.info(f"Используем имя базы из переменной TODO_DB_NAME - {dbname}")
    return dbname if dbname is not None else str(cli_config_obj["db_cfg"]["db_name"])


def make_db(db_name_new: str):
    """
    Создаем основную базу данных для работы приложения.
    Создаем основную таблицу для работы приложения
    """
    # создаем БД
    logger.info("Запуск  make_db()")
    if not db_name_new:
        logger.error("Ошибка в make_db(): Надо передать db_new_new")
        raise ValueError("make_db(): Надо передать db_new_new")

    try:
        print("\n\nСоздаю базу данных...")
        with sqlite3.connect(db_name_new) as db_connection:
            print("База данных создана\n")
            logger.info("make_db(): База данных %s создана", db_name_new)
    except sqlite3.Error as err:
        logger.info("Ошибка в make_db(): %s", str(err))
        print(f"Ошибка в make_db():\n {str(err)}")
        raise

    # Записываем таблицу, если не создана
    try:
        with sqlite3.connect(db_name_new) as db_connection:
            print("Создаю таблицу для ToDo заданий в Базе Данных")
            logger.info("make_db(): Создаю таблицу в БД")
            db_cursor = db_connection.cursor()
            db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_todo_list(
            id INTEGER PRIMARY KEY,
            data_of_creation,
            date_max TEXT,
            todo_text TEXT,
            is_gone integer,
            date_of_gone TEXT
            )
            """)
        print("Таблица в базе данных создана успешно\n")
        print("База данных создана и подготовлена к работа.")
        logger.info("make_db(): БД создана")
    except sqlite3.Error as error:
        logger.error("make_db(): Ошибка %s", str(error))
        print(f"make_db(): Ошибка:\n  {str(error)}")
        raise


def make_task(db_name: str, text_of_task: str):  # Создаю таск в БД
    """
    Создаем новую задачу в таблице my_todo_list в БД
    выводим последнюю созданную запись на экран
    """
    logger.info("make_task(): Запуск")
    logger.info("make_task(): DB name is: %s", db_name)
    logger.info("make_task(): Task for execute is:  %s", text_of_task)
    # Открываем БД на Read-Write. Создавать - не будем.
    db_name_rw: str = "file:" + db_name + "?mode=rw"
    logger.info("make_task():DB name for writeng is: %s", db_name_rw)

    # Получаем объект дата время
    date_time_now_obj = datetime.now()

    # Преобразовываем его как нам надо
    date_time_now = date_time_now_obj.strftime("%d.%m.%Y %H:%M")
    print("Добавляю задачу в БД...\n")
    logger.info("make_task(): add task to BD")
    try:
        with sqlite3.connect(db_name_rw, uri=True) as db_connection:
            db_cursor = db_connection.cursor()
            db_sql_query = """INSERT INTO my_todo_list (data_of_creation, todo_text, is_gone)
                              VALUES (?, ?, ?)"""
            adding_datas = [date_time_now, text_of_task, 0]
            test = db_cursor.execute(db_sql_query, adding_datas)
            print(test)
            db_connection.commit()
        print("Задача в БД добавлена:\n")
        list_of_tasks(db_name, "last")  # Выводим на экран последнюю созданную запись
    except sqlite3.Error as err:
        print(f"Ошибка: \n{str(err)}")


def set_tasks_deadline(db_name: str, task_deadline_id: int):
    # TODO Сделать проверку установлена ли
    # крайняя дата выполнения и если установлена уточнить, меняем или нет
    # TODO Сделать проверку, больше ли вводимая дата текущего числа
    # TODO Думаю, надо стукнуть на почту, если кто-то попытается
    # поменяять дату исполнения на прошедшую (а надо щи стучать?)
    # TODO Сделать проверку на наличие записи вообще
    # TODO Проверить на завешенность - если завершено, то любые изменения запрещены
    """
    Автор: Евгений Б. Петров, Челябинск, p174@mail.ru
    Процедура устанавливает сроки исполнения задания с конкретным номером
    DB_NAME - имя БД, с которой работаем
    task_deadline_id - номер записи, которую мы изменяем
    """
    print("\nУстанавливаем крайнюю дату исполнения  задания")
    logger.info("set_tasks_deadline(): запуск")

    # Делаем инфрмирование до запроса даты, что бы проверить наличие записи в БД
    # что бы пользователь не вводил дишние данные.
    list_of_tasks(db_name, "one", task_deadline_id)
    print(
        f"Устанавливаем для записи номер {task_deadline_id} дату и время исполнения: "
    )

    while True:
        date_time_deadline = input("""\nВведите дату и время завершения задания
                                   в формате ДД.ММ.ГГГГ ЧЧ:ММ: """)
        try:
            datetime.strptime(date_time_deadline, "%d.%m.%Y %H:%M")
            logger.debug("set_tasks_deadline(): Позьзователь ввел корректное значение")
            break
        except ValueError:
            print("""Введенно значение некорректно,
                  введите значение в формате ДД.ММ.ГГГГ ЧЧ:ММ""")
            logger.error("""set_tasks_deadline():
                          Пользователь ввел некорректное знначение даты и времени""")
            continue

    select_id_sql_deadline = (
        """UPDATE my_todo_list
                               SET date_max=\""""
        + str(date_time_deadline)
        + """\"
                               WHERE id="""
        + str(task_deadline_id)
    )

    if confirm_action("установка срока исполнения задания", str(task_deadline_id)):
        logger.debug(
            "set_tasks_deadline(): Запись значения в БД, Пользователь подтвердил"
        )
        work_with_slq(db_name, "write", "many", select_id_sql_deadline)
        print(
            f"\n\nЗапись номер {task_deadline_id} изменена. Срок исполнения установлен"
        )
        list_of_tasks(db_name, "one", task_deadline_id)
    else:
        print("Отменияем изменение записи")
        logger.debug(
            "set_tasks_deadline(): Не изменяем запись, пользлватель не подтвердил "
        )
        exit(1)


def list_of_tasks(db_name: str, all_or_last: str = "all", id_row: int = 0):
    """
    Выводим список дел из таблицы на экран.
    Если задан параметр all - выводим все записи по 10 шт, указана по умолчанию.
    ЕСли задан параметр last - то только последнюю запись
    Если задан переметр one  - выводим одну запись, номер задаем третьим пареметром
    """

    # выводим списк дел.
    logger.info("list_of_tasks(): Запуск")

    # Такой синтаксис для открытия БД - что бы открыть её только на чтение/запись, без создания
    # говорит, что не используется db_name_rw = "file:" + db_name + "?mode=rw"
    row = None
    row_insert = None

    # Формирую заголовой таблицы. Таблица - с красивым выводом
    # global todo_table
    todo_table = PrettyTable()
    table_header(todo_table)

    # Формируем SQL запрос на одну запись, на последнюю или на все.
    # На различный функцилнал требуются различные выводы таблицы

    # check all_or_last for valid value
    if all_or_last != "all" and all_or_last != "last" and all_or_last != "one":
        logger.error("list_of_tasks(): Передан некорректный параметр all_or_last")
        print("Передан некорректный параметр all_or_last")
        exit(1)

    data_of_todo: List[sqlite3.Row] = []

    try:
        logger.debug("list_of_tasks(): Подключение к БД через work_with_slq")
        logger.debug("list_of_tasks(): Выполнение SQL-запроса через work_with_slq()")

        if all_or_last == "last":
            data_of_todo = get_last_record(db_name)

        elif all_or_last == "all":
            data_of_todo = get_all_records(db_name)

        elif all_or_last == "one":
            data_of_todo = get_record_by_id(db_name, id_row)

        ####================
        # COMMENT: можно использовать enumerate и вести отдельный счетчик самостоятельно
        # Преобразую значение в таблице в удобоваримый вид для КЛ
        for counter, row in enumerate(data_of_todo):
            # COMMENT: лучше не модифицировать кортеж in-place, такой код сложно читать.
            # COMMENT: и лучше не использовать индексы, а обращаться к полям по имени.
            # Для этого устанавливаем row_factory = sql3.Row (см. выше)
            # COMMENT: лучше так
            # Создать кортеж из строки, полученной из БД, и добавить его в таблицу
            row_insert = (
                row["id"],
                row["data_of_creation"],
                row["date_max"] or "Отсутсвует",
                row["todo_text"],
                "Исполнено" if row["is_gone"] else "Нет",
                row["date_of_gone"] or "Не установлено",
            )
            todo_table.add_row(row_insert)
            if counter > 0 and counter % 10 == 0:
                print(todo_table)  #  тут выводим, если блок из 10 штук
                todo_table.clear_rows()
                input("\nДля продолжения нажмите Enter: ")
                # counter = 1  # больше не нужен, т.к. используем enumerate
                table_header(todo_table)
            # counter += 1  # больше не нужен, т.к. используем enumerate
        print(todo_table)  # а тут выводим, если меньше 10
    ####==========================

    except sqlite3.Error as err:
        logger.error("Ой!", exc_info=err)
        print(f"Ошибка: \n{str(err)}")


def get_last_record(db_name):
    """
    Автор: Евгений Петров, Челябинск,
    Возвращает последнюю запись из БД
    """
    db_sql_query = """SELECT *
                      FROM  my_todo_list
                      ORDER BY id 
                      DESC LIMIT 1
                    """
    data_of_todo = work_with_slq(db_name, "read", "many", db_sql_query)  # Новая функция
    return data_of_todo


def get_all_records(db_name):
    """
    Автор: Евгений Петров, Челябинск,
    Возвращает все записи из БД
    """
    db_sql_query = "SELECT * FROM  my_todo_list"
    data_from_bd = work_with_slq(db_name, "read", "many", db_sql_query)
    return data_from_bd


def get_record_by_id(db_name, id_row):
    """
    Автор: Евгений Петров, Челябинск,
    Возвращает запись с номером id_row из БД
    """
    db_sql_query = "SELECT * FROM  my_todo_list WHERE id=" + str(id_row)
    data_of_todo = work_with_slq(db_name, "read", "many", db_sql_query)
    return data_of_todo


def delete_task(db_name_for_delete_task: str, deleting_task: int):
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Удаляем одно задание, номер которого получаем в параметре
    DB_NAME - имя БД, с которой работаем
    deleting_task - id удаляемой записи
    """

    logger.info("delete_task(): Запуск процедуры")
    # DB_NAME_RW = "file:" + db_name_for_delete_task + "?mode=rw"
    select_id_sql_for_delete_task: str = """DELETE FROM  my_todo_list
                                            WHERE id=""" + str(deleting_task)

    list_of_tasks(db_name_for_delete_task, "one", deleting_task)
    print("Вы хотите удалить данную запись.\n")

    if confirm_action(" удаление записи #", str(deleting_task)):
        logger.debug("""delete_task():
                      Пользователь подтвердил удаление записи #{deleting_task}""")
        work_with_slq(
            db_name_for_delete_task, "write", "one", select_id_sql_for_delete_task
        )
    else:
        logger.debug("""delete_task():
                      Пользователь не подтвердил удаление записи #{deleting_task}""")
        exit(1)


def task_done(db_name: str, complited_id: int) -> None:
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Помечаем задание с номером ask_done_id помеченным и исполненным.
    Пометка осуществляется текущим временем
    DB_NAME - имя БД, с которой работаем
    task_gone_id - id записи, с которой работаем
    """

    logger.info("task_done(): запуск")

    date_time_now_obj = datetime.now()  # Получаем объект дата время
    date_time_now = date_time_now_obj.strftime(
        "%d.%m.%Y %H:%M"
    )  # Преобразовываем его как нам надо

    # Формирую sql запрос на пометку задания исполненным
    select_id_sql_gone = """UPDATE my_todo_list
                            SET is_gone = 1 
                            WHERE id=""" + str(complited_id)

    # Формирую SQL запрос на установку даты исполнения
    select_id_sql_date_gone = (
        """UPDATE my_todo_list
    SET date_of_gone=\""""
        + str(date_time_now)
        + """\" WHERE id="""
        + str(complited_id)
    )

    id_and_date = "# " + str(complited_id) + ", дата выполнения " + date_time_now
    list_of_tasks(db_name, "one", complited_id)  # Показываеи запись до их изменения

    if confirm_action("пометить исполненным задание ", id_and_date):
        logger.debug("task_gone(): Записываем пометку исполнения задания в БД")
        work_with_slq(
            db_name, "write", "one", select_id_sql_gone
        )  # Помечаем запись выполненой

        logger.debug("task_gone(): Записываем дату исполнения задания в БД")
        work_with_slq(db_name, "write", "one", select_id_sql_date_gone)
        list_of_tasks(db_name, "one", complited_id)  # Показываем запись с изменениями
        print(f'\n\nЗапись номер {complited_id} изменена на "Исполенно"')
    else:
        print(
            f'\n\nОтменяем изменение статуса задания № {complited_id}  на "Исполенно"'
        )
        logger.debug(
            "task_gone(): Пользователь не подтвердил изменение записи на исполнено"
        )
        exit(1)


def work_with_slq(
    db_name_def_worrk_with_sql: str,
    type_of_sql: str,
    is_one: str,
    db_sql_query: str,
    db_sql_data: tuple = (),
) -> List[sqlite3.Row]:  # isDone Далаем запись в БД
    """
    Выполняе запрос в базу данных. Если указаана только БД
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

    logger.info("work_with_slq(): Запуск")

    db_return: List = []
    # data: List =[]

    db_name_rw = "file:" + db_name_def_worrk_with_sql + "?mode=rw"

    logger.debug("work_with_slq(): Имя БД: %s", db_name_rw)
    logger.debug("work_with_slq(): SQL запрос: %s", db_sql_query)
    logger.debug("work_with_slq(): SQL данные: %s", db_sql_data)

    try:
        with sqlite3.connect(db_name_rw, uri=True) as db_connection:
            db_connection.row_factory = sqlite3.Row
            db_cursor = db_connection.cursor()

            logger.debug("""work_with_slq(): Подключился к БД,
                          Получил курсор, Выполняю SQL запрос""")
            db_return_temp = db_cursor.execute(db_sql_query, db_sql_data)

            if is_one == "one":
                db_return = db_return_temp.fetchone()

            if is_one == "many":
                db_return = db_return_temp.fetchall()

            if type_of_sql == "read" and len(db_return) == 0:
                print("Запись с таким номером в БД отсутсвует.")
                logger.error(
                    "work_with_slq(): Запись с таким номером в БД отсутствует."
                )
                return []

            if type_of_sql == "write":
                db_connection.commit()
    # else:
    except sqlite3.Error as err:
        print(f"Ошибка: {err}")
        logger.error("work_with_slq(): Упс!!!", exc_info=err)
    return db_return


def confirm_action(confirm_text: str = "---Текст---", other_text: str = ""):
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Функция выполняет запрос подтверждения какой-либо операции у пользователя.
    Возвращает True если подтвердил, False, если не подтвердил
    confirm_text  - Описание операции, которую надо подьвердить
    other_text  - возможность добавить какой-то текст, проме описания
    операции(например номер позиции)
    """

    logger.info("confirm_action(): Запуск")

    # TODO Прикрутить везде работу с БД через функцию и прикрутить подтверждение операции
    logger.debug("""confirm_action(): Запрос подтверждение операции:
                  {confirm_text} у пользователя""")

    while True:
        is_confirm = input(f"Выполнить операцию: {confirm_text} {other_text}? y/n ")
        if is_confirm.upper() == "Y":
            print(f"Выполняю операцию: {confirm_text}")
            return_value = True
            logger.debug(
                "confirm_action(): ПОДТВЕРЖДЕНИЕ Пользователь подтвердил операцию"
            )
            break
        elif is_confirm.upper() == "N":
            print(f"Отменяю выполнение операции: {confirm_text}!")
            return_value = False
            logger.debug(
                "confirm_action(): ОТМЕНА Пользователь не подтвердил операцию."
            )
            break
        else:
            print('Вы ввели не корректное значение. Введите "y" или "n"!')
            logger.error("""confirm_action():
                          Пользователь ввел некорректное значение. Можно только Y,y или N,n """)
    return return_value
