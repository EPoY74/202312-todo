import os
import sys

import argparse as ap
import sqlite3 as sql3
import time
from datetime import datetime
import configparser as cfg_par

from prettytable import PrettyTable

import logging

# Конфигурирование логгера
FORMAT = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('todologger')

def search_config_and_db(): # Ищем конфигурацию и БД,если нет - создаем
    """
    Функция ищет файл конфигурации и файл БД, если отсутствует(первый запуск,допустим),
    то создает их.
    Возвращает объект с  файлом конфигурации
    #TODO А правильно написал? Спросить у Славы
    """
    full_prog_name = str(sys.argv[0])  # Читаю полное имя файла
    prog_name = full_prog_name[0:full_prog_name.find(".")]  # Получаю имя скрипта без точки
    ini_file_name = str(prog_name + ".ini")  # Формирую имя файла конфигурации
    db_file_name = str(prog_name + ".db")  # Формирую имя БД
    
    todo_config_obj = cfg_par.ConfigParser()  # Создаю объект парсера конфигурации
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
    
def table_header():  # шапка таблицы, что бы не окарать, когда меняешь пареметры 
    global todo_table
    '''
    Функция выводит шапку таблицы с заранее заданными переметрами
    '''
    todo_table.field_names = ["Номер", "Дата создания", "Исполнение до", "Задание", "Исполнено", "Дата исполнения"]
    todo_table._max_width = {"Задание" : 60}
    todo_table._min_width = {"Задание" : 60, "Исполнение до" : 16, "Исполнено" : 16, "Дата исполнения" : 16}
    todo_table.align["Задание"] = "l"

def create_config_file(ini_file_name: str, DB_NAME : str):  # Создаю файл конфигурации

    print("\n\nСоздаю файл конфигурации...")
    todo_config = cfg_par.ConfigParser()
    todo_config.add_section("db_cfg")
    cfg_record = str("db_name = " + DB_NAME)
    todo_config.set("db_cfg", "db_name", DB_NAME)

    with open(ini_file_name, "w") as cfg_file:
        todo_config.write(cfg_file)
    print("Файл конфигурации создан успешно!")
    exit(0)

def get_db_name(todo_config_obj):  # Беру имя БД из переменной окружения TODO_DB_NAME, если она есть    
    """
    Получает имя базы из переменной окружения TODO_DB_NAME.
    Если такой переменной нет, то имя базы будет eo20231206sql.db.
    """
    #TODO Проверить, так ли я понял документацию. понял, что todo_config - должен содержать содержимое файла конфигурации
    dbname = os.getenv("TODO_DB_NAME")
    if dbname is not None:
        print(f"Используем имя базы из переменной TODO_DB_NAME - {dbname}")
    return dbname if dbname is not None else str(todo_config_obj["db_cfg"]["db_name"])

def make_db(db_name_new: str):  # Создаю БД, если её нет
    """
    Создаем основную базу данных для работы приложения.
    Создаем основную таблицу для работы приложения
    """
    #создаем БД
    if not db_name_new:
        raise ValueError("Надо передать db_new_new")

    try:
        print("\n\nСоздаю базу данных...")
        with sql3.connect(db_name_new) as db_connection:
            print("База данных создана\n")
        # db_connection.close()
    except sql3.Error as err: print(f"Ошибка:\n {str(err)}")
    
    # ЗАписываем таблицу, если не создана
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
    except sql3.Error as error: print(f"Ошибка:\n  {str(error)}")
   
def make_task(DB_NAME: str, text_of_task : str):  # Создаю таск в БД 

    """
    Создаем новую задачу в таблице my_todo_list в БД
    выводим последнюю созданную запись на экран
    """
    DB_NAME_RW = "file:"+DB_NAME + "?mode=rw" # Открываем БД на Read-Write. Создавать - не будем.
    date_time_now_obj = datetime.now()  # Получаем объект дата время 
    date_time_now = date_time_now_obj.strftime('%d.%m.%Y %H:%M')  # Преобразовываем его как нам надо
    print("Добавляю задачу в БД...\n")
    try:
        with sql3.connect(DB_NAME_RW, uri=True) as db_connection:
            db_cursor = db_connection.cursor()
            # db_sql_query = f'INSERT INTO my_todo_list (data_of_creation, todo_text, is_gone) VALUES (?, {text_of_task}, ?)'
            db_sql_query = '''INSERT INTO my_todo_list (data_of_creation, todo_text, is_gone) VALUES (?, ?, ?)'''
            adding_datas = [date_time_now, text_of_task, 0]
            test = db_cursor.execute(db_sql_query, adding_datas)
            print(test)
            db_connection.commit()
        print("Задача в БД добавлена:\n")
        list_of_tasks(DB_NAME, "last") # Выводим на экран последнюю созданную запись
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")

def set_tasks_deadline(DB_NAME : str, task_deadline_id : int):  # Устанавливаем дату исполнения
    """
    Устанавливает сроки исполнения задания
    """
    print("\n\nУстанавливаем крайнюю дату выполнения")
    while True:
        date_time_deadline = input("/nВведите дату и время завершения задания в формате ДД.ММ.ГГГГ ЧЧ:ММ: ")
        try:
            datetime.strptime(date_time_deadline, '%d.%m.%Y %H:%M')
            break
        except ValueError:
            print("Введенно значение некорректно, введите значение в формате ДД.ММ.ГГГГ ЧЧ:ММ")
            continue

    DB_NAME_RW = "file:" + DB_NAME + "?mode=rw"  # будем открывать файл только на запись
    # select_id_sql_deadline = '''UPDATE my_todo_list SET is_gone = 1 WHERE id='''+str(task_gone_id)
    select_id_sql_deadline ='''UPDATE my_todo_list SET date_max=\"''' + str(date_time_deadline) + '''\" WHERE id=''' + str(task_deadline_id)

    # print(date_time_now)
    # print(select_id_sql_date_gone)
    
    try:
        with sql3.connect(DB_NAME_RW, uri=True) as db_connection:
            print(f"Устанавливаем для записи номер {task_deadline_id} дату и время исполнения: ")
            list_of_tasks(DB_NAME,"one",task_deadline_id)
            while True:
                is_confirm = ""
                is_confirm = input("\nВы подтверждаете установку срока исполнения? y/n: ")
                if is_confirm == "y" or is_confirm == "Y":
                        db_cursor = db_connection.cursor()
                        db_cursor.execute(select_id_sql_deadline)
                        # db_connection.commit()  # Так как делаем изменения, необходимо закомитить
                        # db_cursor.execute(select_id_sql_date_dead)
                        db_connection.commit()  # Так как делаем изменения, необходимо закомитить
                        print(f"\n\nЗапись номер {task_deadline_id} изменена. Срок исполнения установлен")
                        list_of_tasks(DB_NAME,"one",task_deadline_id)
                        break
                elif is_confirm == "n" or is_confirm == "N":
                    print("Отменияем изменение записи")
                    exit(1)
                else:
                    print('Вы ввели не корректное значение. Введите "y" или "n"!')
                    continue
                    exit(1)
    
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")

def list_of_tasks(DB_NAME: str, all_or_last: str = "all", id_row : int = None):  # Вывод списка тасков
    """
    Выводим список дел из таблицы на экран.
    Если задан параметр all - выводим все записи по 10 шт, указана по умолчанию.
    ЕСли задан параметр last - то только последнюю запись  
    Если задан переметр one  - выводим одну запись, номер задаем третьим пареметром
    """
    #выводим списк дел.

    logging.info("выводим списк дел")

    # Такой синтаксис для открытия БД - что бы открыть её только на чтение/запись, без создания
    DB_NAME_RW = "file:" + DB_NAME + "?mode=rw"
    
    # Формирую заголовой таблицы. Таблица - с красивым выводом
    global todo_table
    todo_table = PrettyTable()
    table_header()
        
    # Формируем SQL запрос на одну запись, на последнюю или на все.
    # На различный функцилнал требуются различные выводы таблицы
    if all_or_last == "last":
        db_sql_query = '''SELECT * FROM  my_todo_list ORDER BY id DESC LIMIT 1'''
    
    elif all_or_last == "all":
        db_sql_query = '''SELECT * FROM  my_todo_list'''
    
    elif all_or_last == "one":
        db_sql_query = '''SELECT * FROM  my_todo_list WHERE id=''' + str(id_row)
    
    try:
        logging.debug("Подключение к базе.Новая функция")
        # with sql3.connect(DB_NAME_RW, uri=True) as db_connection:  # Здесь надо указать именно соединение, а не курсор
        # db_cursor = db_connection.cursor()
        logging.debug("Выполнение SQL-запроса через новую функцию ")
        data_of_todo = work_with_slq(DB_NAME, db_sql_query)  # Новая функция
        # data_of_todo = db_cursor.execute(db_sql_query)
        print(data_of_todo)
        counter = 1
        for row in data_of_todo:  # Преобразую значение в таблице в удобоваримый вид для КЛ
            row_insert = [row_ins for row_ins in row]
            if not row_insert[2]:
                row_insert[2]   = "Отсутсвует"
            if row_insert[5] == 0:
                row_insert[5]  = "Не выполнено"
            if row_insert[4]:
                row_insert[4] = "Исполнено"
            elif not row_insert[4]:
                row_insert[4] = "Нет"
            else:
                row_insert[4] = "Странно..."
            todo_table.add_row(row_insert)
            if counter == 10:
                print(todo_table)  #  тут выводим, если блок из 10 штук
                todo_table.clear_rows()
                input("\nДля продолжения нажмите Enter: ")
                counter = 1 
                table_header()
            counter += 1
        print(todo_table)  # а тут выводим, если меньше 10
    except sql3.Error as err:
        logging.error("Ой!", exc_info=err)
        print(f"Ошибка: \n{str(err)}")

def delete_task(DB_NAME: str, deleting_task: int):  # Удаляем таск (только один)
    """
    Удаляем одно задание, номер которого получаем в параметре
    """
    DB_NAME_RW = "file:" + DB_NAME + "?mode=rw"
    select_id_sql = '''DELETE FROM  my_todo_list WHERE id=''' + str(deleting_task)
    # print(select_id_sql)
    try:
        with sql3.connect(DB_NAME_RW, uri=True) as db_connection:
            print(f"Удаляем запись номер  {deleting_task}")
            list_of_tasks(DB_NAME,"one",deleting_task)
            is_confirm = input("\nВы подтверждаете удаление записи? y/n: ")
            if is_confirm == "y" or is_confirm == "Y":
                    db_cursor = db_connection.cursor()
                    db_cursor.execute(select_id_sql)
                    db_connection.commit()  # Так как делаем изменения, необходимо закомитить
                    print(f"Запись номер {deleting_task} удалена")
            elif is_confirm == "n" or is_confirm == "N":
                print("Отменияем удаление записи")
                exit(1)
            else:
                print('Вы ввели не корректное значение. Введите "y" или "n"!')
                exit(1)
           
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")

def task_gone(DB_NAME: str, task_gone_id: int):  # Помечаем таск исполненым
    """
    Помечаем задание с номером ask_gone_id помеченным и исполненным.
    Пометка осуществляется текущим временем
    """
    date_time_now_obj = datetime.now()  # Получаем объект дата время 
    date_time_now = date_time_now_obj.strftime('%d.%m.%Y %H:%M')  # Преобразовываем его как нам надо
    
    DB_NAME_RW = "file:" + DB_NAME + "?mode=rw"  # будем открывать файл только на запись
    select_id_sql_gone = '''UPDATE my_todo_list SET is_gone = 1 WHERE id='''+str(task_gone_id)
    select_id_sql_date_gone = '''UPDATE my_todo_list SET date_of_gone=\"''' + str(date_time_now) + '''\" WHERE id='''+str(task_gone_id)
    # print(date_time_now)
    # print(select_id_sql_date_gone)
    
    try:
        with sql3.connect(DB_NAME_RW, uri=True) as db_connection:
            print(f"Помечаем запись номер {task_gone_id} завершенной (исполненной): ")
            list_of_tasks(DB_NAME,"one",task_gone_id)
            is_confirm = ""
            is_confirm = input("\nВы подтверждаете изменение задания на \"Исполненно\"? y/n: ")
            if is_confirm == "y" or is_confirm == "Y":
                    db_cursor = db_connection.cursor()
                    db_cursor.execute(select_id_sql_gone)
                # db_connection.commit()  # Так как делаем изменения, необходимо закомитить
                    db_cursor.execute(select_id_sql_date_gone)
                    db_connection.commit()  # Так как делаем изменения, необходимо закомитить
                    print(f"\n\nЗапись номер {task_gone_id} изменена на \"Исполенно\"")
                    list_of_tasks(DB_NAME,"one",task_gone_id)
            elif is_confirm == "n" or is_confirm == "N":
                print("Отменияем изменение записи")
                exit(1)
            else:
                print('Вы ввели не корректное значение. Введите "y" или "n"!')
                exit(1)
    
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")

def work_with_slq(DB_NAME: str, db_sql_query: str, db_sql_data: tuple = () ):  # Далаем запись в БД
    """
    Пишет запрос в базуданных. Если указаана только БД и запрос - то выполняем только его
    Если укзазан БД, запрос и данные - то выполняем и данные и запрос.
    DB_NAME - Имя базы данных
    db_sql_query - SQL запоос к базе данных
    db_slq_data - передаваемые параметры в SQL запрос (необязательный)
    
    Возвращает результат запроса
    """

    DB_NAME_RW = "file:" + DB_NAME + "?mode = rw"
    try:
        # if db_sql_data == None:
        #     print("пишем один параметр")
        # elif db_sql_data != None:
        #     print("Пишем оба параметра")
        # else:
        #     print("Происходит что-то странное, не те параметры для записи в БД")
        logging.debug("Подключаюсь к БД (функция)")
        with sql3.connect(DB_NAME_RW, uri = True) as db_connection:
            db_connection.row_factory = sql3.Row
            logging.debug("Getting cursor (function)")
            db_cursor = db_connection.cursor()
            logging.debug("Executing SQL query (function)")
            db_return = db_cursor.execute(db_sql_query, db_sql_data)
            db_connection.commit()


    except sql3.Error as err:
        print(f"Ошибка: {err}")
        logging.error("Omg!!!", exc_info=err)

    return db_return

def confirm_action(confirm_text : str = "---Текст---", other_text : str = None):
    """
    Автор: Евгений Петров, Челябинск
    Функция выполняет запрос подтверждения какой-либо операции у пользователя.
    Возвращает True если подтвердил, False, если не подтвердил  
    """
    #TODO Прикрутить везде работу с БД через функцию и прикрутить подтверждение операции 
    logging.debug(f"ФУНКЦИЯ: Подтверждение операции: {confirm_text}")
    while True:
        is_confirm = input(f"Выполнить операцию: {confirm_text} {other_text}? y/n ")
        if is_confirm.upper() == "Y":
            print(f"Выполняю операцию {confirm_text}")
            return_value = True
            break               
        elif is_confirm.upper() == "N":
            print(f"Отменяю выполнение операции {confirm_text}!")
            return_value = False
            break
        else:
            print('Вы ввели не корректное значение. Введите "y" или "n"!')
    return return_value


if __name__ == "__main__":
    
    print("""\n\nКонсольное приложение для ведения задач. \n
          Автор: Евгений Б. Петров, p174@mail.ru""")
    
    #  Принимаю объект с файлом конфигурации, что бы избавится от глобальной переменной
    todo_config_obj =  search_config_and_db()  
    
    DB_NAME = get_db_name(todo_config_obj)

    logger.debug("Старт")
    
    parser = ap.ArgumentParser()
    parser.description = "Програма создает ToDo список дел в текстовом консольном режиме."
    parser.add_argument("--create_db", help = "Создаем базу данных для списка задач", action="store_true")
    parser.add_argument("--task_add", type = str,  help = """Описание задачи, которую заводим: --task_add \"Это запись\" """)
    parser.add_argument("--task_deadline", type = int, help = "Устанавлявает дату, до которой надо выполнить задание: --task_deadline номер_записи")
    parser.add_argument("--task_list", help = "Выводит список задач", action="store_true")  # И где написано про action интересно?
    parser.add_argument("--task_gone_date", type = int, help = "Помечает задание с номером № завершенным: --set_gone_date номер_записи")
    parser.add_argument("--task_del_id", type = int, help = "Удаляет запись с номером: --task_del_id номер_записи" )

    args = parser.parse_args()

    # TODO: использовать ORM взаимодействия с базой, например http://docs.peewee-orm.com/en/latest/#

    
    # print(sys.argv[0])
    full_prog_name = str(sys.argv[0])
    prog_name = full_prog_name[0:full_prog_name.find(".")]
    # print(prog_name)

    if args.create_db:
        make_db("test.db")
    elif args.task_add:
        make_task(DB_NAME, args.task_add)
    elif args.task_deadline:
        set_tasks_deadline(DB_NAME, args.task_deadline)
    elif args.task_list:  
        list_of_tasks(DB_NAME, "all")
    elif args.task_gone_date:
        task_gone(DB_NAME, args.task_gone_date)
    elif args.task_del_id:
        delete_task(DB_NAME, args.task_del_id)
    # else:
    #     print(f'Неизвестная команда "{args.command}"')

    # while True:
    #     # TODO: проверки задача в базе и рассылка почты
    #     logging.debug("Проверка базы")
    #     time.sleep(1)
