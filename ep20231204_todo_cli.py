import argparse as ap
import sqlite3 as sql3
import os
from datetime import datetime
import configparser as cfg_par

# TODO  Убрать чтобы БД не плодились, если вдруг ошибка и именовании базы

def get_db_name():
    """
    Получает имя базы из переменной окружения TODO_DB_NAME.
    Если такой переменной нет, то имя базы будет eo20231206sql.db.
    """
    global todo_config
    dbname = os.getenv("TODO_DB_NAME")
    if dbname is not None:
        print(f"Используем имя базы из переменной TODO_DB_NAME - {dbname}")
    return dbname if dbname is not None else str(todo_config["db_cfg"]["db_name"])

def make_db():
    """
    Создаем основную базу данных для работы приложения.
    Создаем основную таблицу для работы приложения
    """
    #создаем БД
    try:
        with sql3.connect(DB_NAME) as db_connection:
            print("База данных создана\n\n")
        # db_connection.close()
    except sql3.Error as err: print(f"Ошибка:\n {str(err)}")
    
    # ЗАписываем таблицу, если не создана
    try:
        with sql3.connect(DB_NAME) as db_connection:
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
    except sql3.Error as error: print(f"Ошибка:\n  {str(error)}")
   
def make_task(text_of_task:str):
    """
    Создаем новую задачу в таблице my_todo_list в БД
    выводим последнюю созданную запись на экран
    """
    DB_NAME_RW = "file:"+DB_NAME + "?mode=rw" # Открываем БД на Read-Write. Создавать - не будем.
    print(DB_NAME_RW)
    date_time_now_obj = datetime.now()  # Получаем объект дата время 
    date_time_now = date_time_now_obj.strftime('%d.%m.%Y %H:%M')  # Преобразовываем его как нам надо
    print("Добавляю задачу в БД...")
    try:
        with sql3.connect(DB_NAME_RW, uri=True) as db_connection:
            db_cursor = db_connection.cursor()
            db_sql_query = '''INSERT INTO my_todo_list (data_of_creation, todo_text, is_gone) VALUES (?, ?, ?)'''
            adding_datas = [date_time_now, text_of_task, 0]
            db_cursor.execute(db_sql_query, adding_datas)
            db_connection.commit()
        print("Задача в БД добавлена:")
        list_of_tasks(DB_NAME, "last") # Выводим на экран последнюю созданную запись
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")
    
def list_of_tasks(DB_NAME: str, all_or_last: str = "all"):
    # TODO: добавать краcивый вывод таблиц 
    """
    Выводим список дел из таблицы на экран.
    Если задан параметр all - выводим все записи по 10 шт.
    ЕСли задан параметр last - то только последнюю запись  
    """#выводим списк дел
    DB_NAME_RW = "file:" + DB_NAME + "?mode=rw"
    print(type(DB_NAME_RW))
    print(DB_NAME_RW)
    print(str(DB_NAME_RW))
    if all_or_last == "last": db_sql_query = '''SELECT * FROM  my_todo_list ORDER BY id DESC LIMIT 1'''
    elif all_or_last == "all": db_sql_query = '''SELECT * FROM  my_todo_list'''

    try:
        # b_connection = sql3.connect(DB_NAME)
        with sql3.connect(DB_NAME_RW, uri=True) as db_connection:  # Здесь надо указать именно соединение, а не курсор
            db_cursor = db_connection.cursor()
            data_of_todo = db_cursor.execute(db_sql_query)
            names_of_columns = [description[0] for description in db_cursor.description]
            print(names_of_columns)
            counter = 1
            for row in data_of_todo:
                print(row)
                #print(row[0])
                if counter == 10:
                    input("\nДля продолжения нажмите Enter: ")
                    print("\n",names_of_columns,"\n")
                    counter = 1 
                counter += 1
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")

def delete_task(DB_NAME: str, deleting_task: int):
    """
    Удалаем одно задание, номер которого получаем в параметре
    """
    DB_NAME_RW = "file:" + DB_NAME + "?mode=rw"
    select_id_sql = '''DELETE FROM  my_todo_list WHERE id=''' + str(deleting_task)
    print(select_id_sql)
    try:
        with sql3.connect(DB_NAME_RW, uri=True) as db_connection:
            print(f"Удаляем запись номер  {deleting_task}")
            list_of_tasks(DB_NAME,"one",deleting_task)
            try:
                is_confirm = input("\nВы подтверждаете удаление записи? y/n: ")
                if is_confirm == "y" or is_confirm == "Y":
                      db_cursor = db_connection.cursor()
                      db_cursor.execute(select_id_sql)
                      db_connection.commit()  # Так как делаем изменения, необходимо закомитить
                      print(f"Запись номер {deleting_task} удалена")
                elif is_confirm == "n" or is_confirm == "N":
                    print("Отменияем удаление записи")
            except:
                print('Вы ввели не корректное значение. Введите "y" или "n"!')
           
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")



if __name__ == "__main__":
    # TODO: разобраться до конца с файлом конфигурации и начать спрашивать название БД и делать ini если его нет 
    todo_config = cfg_par.ConfigParser()  # Создаю объект парсера конфигурации
    todo_config.read("ep20231204_todo_cli.ini")  # Читаю конфигурацию
    # print(todo_config["db_cfg"]["db_name"])
    DB_NAME = get_db_name()
    # print(DB_NAME)
    parser = ap.ArgumentParser()
    parser.description = """\nПрограма создает ToDo список дел в текстовом консольном режиме.
    \nПоддерживает команды:
    \ncreatedb - создать базу данных
    \nmaketask или add - создать задание
    \nlist - список сохраненных заданий\n
    \ndelete - Удаляет запись """
    parser.add_argument("command",
                        type = str,
                        help = """Команда, что необходимо сделать: delete \ncreatedb  """)
    #createdb
    #list, maketask or add
    parser.add_argument("--text", type = str,  help = "Описание задачи, которую заводим")
    parser.add_argument("--id_row", type = int, help = "id записи, с которой работаем" )
    args = parser.parse_args()

    # TODO: использовать ORM взаимодействия с базой, например http://docs.peewee-orm.com/en/latest/#

    print("Привет! Я - консольное todo приложение\n")
    if args.command == "createdb":
        make_db()
    elif args.command == "maketask" or args.command == "add":
        make_task(args.text)
    elif args.command == "list":
        list_of_tasks(DB_NAME, "all")
    elif args.command == "delete":
        delete_task(DB_NAME, args.id_row)
