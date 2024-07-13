import sys
from typing import List  # TODO: read about type hints
# import logging

import argparse as ap
import sqlite3 as sql3

from datetime import datetime
# import data_access.json as data  # TODO: finish DAL and start using it
from prettytable import PrettyTable

import work_with_sqlite as data
from logging_config import logger  # переместил настройки логирования в отдельный файл

# todo_table = None
# TODO: DONE логировать в файл, а не в консоль


def table_header():  # шапка таблицы, что бы не окарать, когда меняешь паре метры

    """
        Функция выводит шапку таблицы с заранее заданными параметрами
    """
    # global todo_table
    todo_table.field_names = ["Номер", "Дата создания", "Исполнение до", "Задание", "Исполнено", "Дата исполнения"]
    todo_table._max_width = {"Задание": 60}
    todo_table._min_width = {"Задание": 60, "Исполнение до": 16, "Исполнено": 16, "Дата исполнения": 16}
    todo_table.align["Задание"] = "l"


def make_task(text_of_task: str):  # isGONE Создаю таск в БД
    """
    Создаем новую задачу в таблице my_todo_list в БД
    выводим последнюю созданную запись на экран
    """
    logger.info("make_task(): Запуск")

    date_time_now = get_now_time()  # TODO GONE Спросить у Славы, а нужно ли плодить переменные

    print("Добавляю задачу в БД...\n")
    db_query = data.query_for_data('make_task')
    adding_datas = tuple([date_time_now, text_of_task, 0])
    data.work_with_data("write", "one", db_query, adding_datas)
    print("Задача в БД добавлена:\n")
    show_last_task()


def set_tasks_deadline(task_deadline_id: int):  # -done- Устанавливаем дату исполнения

    # TODO Сделать проверку установлена ли крайняя дата выполнения и если установлена уточнить, меняем или нет
    # TODO Сделать проверку, больше ли вводимая дата текущего числа
    # TODO Написать на почту, если кто-то попытается поменять дату исполнения на прошедшую (а надо ли?)
    # TODO -done- Сделать проверку на наличие записи вообще
    # TODO Проверить на завершенность - если завершено, то любые изменения запрещены
    """
    Автор: Евгений Б. Петров, Челябинск, p174@mail.ru
    Процедура устанавливает сроки исполнения задания с конкретным номером
    task_deadline_id - номер записи, которую мы изменяем
    """

    print("\nУстанавливаем крайнюю дату исполнения  задания")
    logger.info("set_tasks_deadline(): запуск")

    # Делаем информирование до запроса даты, что бы проверить наличие записи в БД,
    # что бы пользователь не вводил лишние данные.
    list_of_tasks("one", task_deadline_id)
    print(f"Устанавливаем для записи номер {task_deadline_id} дату и время исполнения: ")

    while True:
        date_time_deadline = input("\nВведите дату и время завершения задания в формате ДД.ММ.ГГГГ ЧЧ:ММ: ")
        try:
            datetime.strptime(date_time_deadline, '%d.%m.%Y %H:%M')
            logger.debug("set_tasks_deadline(): Пользователь ввел корректное значение")
            break

        except ValueError:
            print("Введено значение некорректно, введите значение в формате ДД.ММ.ГГГГ ЧЧ:ММ")
            logger.error("set_tasks_deadline(): Пользователь ввел некорректное значение даты и времени")
            continue

    # select_id_sql_deadline = '''UPDATE my_todo_list SET date_max=\"''' + str(
    #     date_time_deadline) + '''\" WHERE id=''' + str(task_deadline_id)
    set_deadline = data.query_for_data("set_tasks_deadline")
    adding_data = tuple([date_time_deadline, task_deadline_id])

    if confirm_action("установка срока исполнения задания", str(task_deadline_id)):
        logger.debug("set_tasks_deadline(): Запись значения в БД, Пользователь подтвердил")

        data.work_with_data("write", "many", set_deadline, adding_data)
        print(f"\n\nЗапись номер {task_deadline_id} изменена. Срок исполнения установлен")
        list_of_tasks("one", task_deadline_id)
    else:
        print("Отменяем изменение записи")
        # assert isinstance(logger, object)
        logger.debug("set_tasks_deadline(): Не изменяем запись, пользователь не подтвердил ")
        exit(1)
    return ()


def list_of_tasks(all_or_last: str = "all", id_row: int = None):  # isGone Вывод списка тасков
    """
    Выводим список дел из таблицы на экран.
    Если задан параметр all - выводим все записи по 10 шт., указана по умолчанию.
    ЕСли задан параметр last - то только последнюю запись
    Если задан периметр one - выводим одну запись, номер задаем третьим параметром
    """
    # выводим список дел.
    logger.info("list_of_tasks(): Запуск")

    # Формирую заголовок таблицы. Таблица - с красивым выводом
    # global todo_table

    global todo_table

    todo_table = PrettyTable()

    table_header()

    # Формируем SQL запрос на одну запись, на последнюю или на все.
    # На различный функционал требуются различные выводы таблицы

    # check all_or_last for valid value
    if all_or_last != "all" and all_or_last != "last" and all_or_last != "one":
        logger.error("list_of_tasks(): Передан некорректный параметр all_or_last")
        print("Передан некорректный параметр all_or_last")
        exit(1)

    data_of_todo: List[sql3.Row] = []

    try:
        logger.debug("list_of_tasks(): Подключение к БД через work_with_slq")
        logger.debug("list_of_tasks(): Выполнение SQL-запроса через work_with_slq()")

        if all_or_last == "last":
            data_of_todo = get_query_last_record()

        elif all_or_last == "all":
            data_of_todo = get_query_all_records()

        elif all_or_last == "one":
            data_of_todo = get_query_record_by_id(id_row)

        counter = 1
        for row in data_of_todo:  # Преобразую значение в таблице в удобоваримый вид для КЛ
            row_insert = [row_ins for row_ins in row]
            if not row_insert[2]:
                row_insert[2] = "Отсутствует"
            if row_insert[5] == 0:
                row_insert[5] = "Не выполнено"
            if row_insert[4]:
                row_insert[4] = "Исполнено"
            elif not row_insert[4]:
                row_insert[4] = "Нет"
            else:
                row_insert[4] = "Странно..."
            todo_table.add_row(row_insert)
            if counter == 10:
                print(todo_table)  # тут выводим, если блок из 10 штук
                todo_table.clear_rows()
                input("\nДля продолжения нажмите Enter: ")
                counter = 1
                table_header()
            counter += 1
        print(todo_table)  # а тут выводим, если меньше 10
    except sql3.Error as err:
        logger.error("Ой!", exc_info=err)
        print(f"Ошибка: \n{str(err)}")


def get_query_last_record():
    """
        Автор: Евгений Петров, Челябинск, p174@mail.ru
        Подготавливает запрос и возвращает последнюю запись из БД
    """

    db_sql_query = "SELECT * FROM  my_todo_list ORDER BY id DESC LIMIT 1"
    data_of_todo = data.work_with_data("read", "many", db_sql_query)  # Новая функция
    return data_of_todo


def get_query_all_records():
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Подготавливает запрос и возвращает все записи из БД
    """
    db_sql_query = "SELECT * FROM  my_todo_list"
    data_of_todo = data.work_with_data("read", "many", db_sql_query)  # Новая функция
    return data_of_todo


def get_query_record_by_id(id_row):
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Подготавливает запрос и возвращает запись с номером id_row из БД
    """
    db_sql_query = "SELECT * FROM  my_todo_list WHERE id=" + str(id_row)
    data_of_todo = data.work_with_data("read", "many", db_sql_query)  # Новая функция
    return data_of_todo


def delete_task(deleting_task: int):  # Удаляем таск (только один)
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Удаляем одно задание, номер которого получаем в параметре
    DB_NAME - имя БД, с которой работаем
    deleting_task - id удаляемой записи
    """

    logger.info("delete_task(): Запуск процедуры")
    data.query_for_data('delete_task')
    select_id = data.query_for_data('delete_task') + str(deleting_task)

    list_of_tasks("one", deleting_task)
    print("Вы хотите удалить данную запись.\n")

    if confirm_action(" удаление записи #", str(deleting_task)):
        logger.debug(f"delete_task(): Пользователь подтвердил удаление записи #{deleting_task}")
        data.work_with_data("write", "one", select_id)
    else:
        logger.debug(f"delete_task(): Пользователь не подтвердил удаление записи #{deleting_task}")
        exit(1)

    print(f"Запись #{deleting_task} удалена")
    print(f"Проверяю удаление записи #{deleting_task} в БД")
    list_of_tasks("one", deleting_task)


def task_done(task_done_id_int: int) -> None:  # isDone Помечаем таск исполненным
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Помечаем задание с номером ask_gone_id помеченным и исполненным.
    Пометка осуществляется текущим временем
    DB_NAME - имя БД, с которой работаем
    task_gone_id - id записи, с которой работаем
    """

    # TODO DONE Сделать вывод таблицы до и после пометки

    logger.info("task_done(): запуск")

    date_time_now = get_now_time()
    task_done_id = str(task_done_id_int)

    # Формирую sql запрос на пометку задания исполненным
    select_id_sql_done = '''UPDATE my_todo_list SET is_gone = 1 WHERE id=''' + task_done_id

    # Формирую SQL запрос на установку даты исполнения
    select_id_sql_date_done = '''UPDATE my_todo_list SET date_of_gone=\"''' + str(
        date_time_now) + '''\" WHERE id=''' + task_done_id

    id_and_date = "# " + task_done_id + ", дата выполнения " + date_time_now
    list_of_tasks("one", task_done_id_int)  # Показывает запись до их изменения

    if confirm_action("пометить исполненным задание ", id_and_date):

        logger.debug("task_gone(): Записываем пометку исполнения задания в БД")
        data.work_with_data("write", "one", select_id_sql_done)  # Помечаем запись выполненной

        logger.debug("task_gone(): Записываем дату исполнения задания в БД")
        data.work_with_data("write", "one", select_id_sql_date_done)

        list_of_tasks("one", task_done_id_int)  # Показываем запись с изменениями
        print(f"\n\nЗапись номер {task_done_id} изменена на \"Исполнено\"")
    else:
        print(f"\n\nОтменяем изменение статуса задания № {task_done_id}  на \"Исполнено\"")
        logger.debug("task_gone(): Пользователь не подтвердил изменение записи на исполнено")
        exit(1)


def confirm_action(confirm_text: str = "---Текст---", other_text: str = None):  # isGone Проверяет выполнение операции
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Функция выполняет запрос подтверждения какой-либо операции у пользователя.
    Возвращает True если подтвердил, False, если не подтвердил
    confirm_text - Описание операции, которую надо подтвердить
    other_text - возможность добавить какой-то текст, кроме описания операции(например номер позиции)
    """
    logger.info("confirm_action(): Запуск")
    # TODO Прикрутить везде работу с БД через функцию и прикрутить подтверждение операции
    logger.debug(f"confirm_action(): Запрос подтверждение операции: {confirm_text} у пользователя")
    while True:
        is_confirm = input(f"Выполнить операцию: {confirm_text} {other_text}? y/n ")
        if is_confirm.upper() == "Y":
            print(f"Выполняю операцию: {confirm_text}")
            return_value = True
            logger.debug("confirm_action(): ПОДТВЕРЖДЕНИЕ Пользователь подтвердил операцию")
            break
        elif is_confirm.upper() == "N":
            print(f"Отменяю выполнение операции: {confirm_text}!")
            return_value = False
            logger.debug("confirm_action(): ОТМЕНА Пользователь не подтвердил операцию.")
            break
        else:
            print('Вы ввели не корректное значение. Введите "y" или "n"!')
            logger.error("confirm_action(): Пользователь ввел некорректное значение. Можно только Y,y или N,n ")
    return return_value


def is_can_edit(task_id) -> bool:
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Проверяет возможность редактирования записи БД с заданным номером task_id
    Если запись не помечена завершенной, то её можно редактировать
    Возвращает:
        true - если можно редактировать
        false - если нельзя

    """
    query = data.query_for_data("is_can_edit")
    data_of_task = data.work_with_data("read", 'one', query, tuple([task_id]))

    # raise NotImplementedError()
    return True


def main_body():  # isGone Основная логика программы (выбор действия с заданиями)
    """
    Автор: Евгений Б. Петров, Челябинск, p174@mail.ru
    Выполняет основную логику консольного приложения: считывает параметры из командной строки
    и вызывает соответствующую процедуру.
    Ничего не возвращает.
    """
    parser = ap.ArgumentParser()
    parser.description = "Программа создает ToDo список дел в текстовом консольном режиме."
    parser.add_argument("--create_db", help="Создаем базу данных для списка задач", action="store_true")
    parser.add_argument("--task_add", type=str, help="""Описание задачи, которую заводим: --task_add \"Это запись\" """)
    parser.add_argument("--task_deadline", type=int,
                        help="Устанавливает дату, до которой надо выполнить задание: --task_deadline номер_записи")
    parser.add_argument("--task_list", help="Выводит список задач",
                        action="store_true")  # И где написано про action интересно?
    parser.add_argument("--task_done", type=int,
                        help="Помечает задание с номером № завершенным: --set_done_date номер_записи")
    parser.add_argument("--task_delete", type=int, help="Удаляет запись с номером: --task_del_id номер_записи")

    args = parser.parse_args()

    if args.create_db:
        data.make_db("test.db")
    elif args.task_add:
        make_task(args.task_add)
    elif args.task_deadline:
        set_tasks_deadline(args.task_deadline)
    elif args.task_list:
        list_of_tasks("all")
    elif args.task_done:
        task_done(args.task_done_date)
    elif args.task_delete:
        delete_task(args.task_delete)


def print_help_info():
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Выводит основные команды работы с консольным приложением
    Отдельная функция - так как хотел красивый вывод на экран, как мне надо,
    а не как придется
    """

    logger.info("print_help_info(): Запуск")
    print("Основные команды консольного ToDo приложения:")
    print("--create_db: Создаем базу данных для списка задач")
    print("--task_add: Описание задачи, которую заводим: --task_add \"Это запись\" ")
    print("--task_deadline: Устанавливает дату, до которой надо выполнить задание: --task_deadline номер_записи")
    print("--task_list: Выводит список задач")
    print("--task_done: Помечает задание с номером № завершенным: --set_gone_date номер_записи")
    print("--task_delete: Удаляет запись с номером: --task_del_id номер_записи\n")


def get_now_time() -> str:
    """
    Автор: Евений Петров, Челябинск, p174@mqil.ru
    Функция возвращает текущие дату и время в формате %d.%m.%Y %H:%M
    Возвращает str
    """
    date_time_now_obj = datetime.now()  # Получаем объект дата время
    date_time_now = date_time_now_obj.strftime('%d.%m.%Y %H:%M')  # Преобразовываем его как нам надо
    return str(date_time_now)


def show_last_task() -> None:
    """
    Автор: Евгений Петров, Челябинск, p174@mail.ru
    Функция выводит последнюю запись из БД
    Ничего не возвращает
    """
    list_of_tasks("last")


if __name__ == "__main__":
    print("""\nКонсольное приложение для ведения задач. \nАвтор: Евгений Б. Петров, p174@mail.ru\n""")
    logger.info("Старт консольного ToDo приложения.")

    print_help_info()
    main_body()

    # TODO: использовать ORM взаимодействия с базой, например http://docs.peewee-orm.com/en/latest/#

    full_prog_name = str(sys.argv[0])
    prog_name = full_prog_name[0:full_prog_name.find(".")]

    # while True:
    #     # TODO: проверки задача в базе и рассылка почты
    #     logging.debug("Проверка базы")
    #     time.sleep(1)

    logger.info("Конец выполнения консольного ToDo приложения.")
