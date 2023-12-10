import argparse as ap
import sqlite3 as sql3
import os
import datetime


def get_db_name():
    """
    Получает имя базы из переменной окружения TODO_DB_NAME.
    Если такой переменной нет, то имя базы будет eo20231206sql.db.
    """
    dbname = os.getenv("TODO_DB_NAME")
    if dbname is not None:
        print(f"Используем имя базы из переменной TODO_DB_NAME - {dbname}")
    return dbname if dbname is not None else "eo20231206sql.db"

DB_NAME = get_db_name()
# is_ok_flag: bool = True

parser = ap.ArgumentParser()
parser.description = """\nПрограма создает ToDo список дел в текстовом консольном режиме.
\nПоддерживает команды:
\ncreatedb - создать базу данных
\nmaketask или add - создать задание
\nlist - список сохраненных заданий\n """
parser.add_argument("command",
                     type = str,
                       help = "Команда, что необходимо сделать: ")
#createdb
#list, maketask or add
parser.add_argument("--text", type = str,  help = "Описание задачи, которую заводим")

args = parser.parse_args()

# TODO: использовать ORM взаимодействия с базой, например http://docs.peewee-orm.com/en/latest/#

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
    date_time_now_obj = datetime.datetime.now()  # Получаем объект дата время 
    date_time_now = date_time_now_obj.strftime('%d.%m.%Y %H:%M')  # Преобразовываем его как нам надо
    print("Добавляю задачу в БД...")
    try:
        with sql3.connect(DB_NAME) as db_connection:
            db_cursor = db_connection.cursor()
            db_sql_query = '''INSERT INTO my_todo_list (data_of_creation, todo_text, is_gone) VALUES (?, ?, ?)'''
            adding_datas = [date_time_now, text_of_task, 0]
            db_cursor.execute(db_sql_query, adding_datas)
            db_connection.commit()
        print("Задача в БД добавлена:")
        list_of_tasks("last") # Выводим на экран последнюю созданную запись
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")
    
def list_of_tasks(all_or_last: str = "all"):
    """
    Выводим список дел из таблицы на экран.
    Если задан параметр all - выводим все записи по 10 шт.
    ЕСли задан параметр last - то только последнюю запись  
    """#выводим списк дел
    if all_or_last == "last": db_sql_query = '''SELECT * FROM  my_todo_list ORDER BY id DESC LIMIT 1'''
    elif all_or_last == "all": db_sql_query = '''SELECT * FROM  my_todo_list'''

    try:
        with sql3.connect(DB_NAME) as db_connection :  # Здесь надо указать именно соединение, а не курсор
            db_cursor = db_connection.cursor()
            data_of_todo = db_cursor.execute(db_sql_query)
            names_of_columns = [description[0] for description in db_cursor.description]
            print(names_of_columns)
            counter = 0
            for row in data_of_todo:
                print(row)
                #print(row[0])
                if counter == 10:
                    input("\nДля продолжения нажмите Enter: ")
                    print("\n",names_of_columns,"\n")
                    counter = 0 
                counter += 1
    except sql3.Error as err: print(f"Ошибка: \n{str(err)}")

if __name__ == "__main__":
    print("Привет! Я - консольное todo приложение\n")


if __name__ == "__main__":
    if args.command == "createdb":
        make_db()
    elif args.command == "maketask":
        make_task(args.text)
    elif args.command == "list":
        lisf_of_tasks()