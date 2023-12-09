import argparse as ap
import sqlite3 as sql3
import os
import datetime


DB_NAME  = "eo20231206sql.db"
is_ok_flag: bool = True

parser = ap.ArgumentParser()
parser.description = """\nПрограма создает ToDo список дел в текстовом консольном режиме.
\nПоддерживает команды:
\ncreatedb - создать базу данных
\nmaketask - создать задание
\nlist - список сохраненных заданий\n """
parser.add_argument("command",
                     type = str,
                       help = "Команда, что необходимо сделать: ")
#createdb
#list, maketask
parser.add_argument("--text", type = str,  help = "Описание задачи, которую заводим")

args = parser.parse_args()

def make_db():
    global is_ok_flag

    #создаем БД
    print("Создаю базу данных")
    db_connection = sql3.connect(DB_NAME)
    db_connection.close()
    
    
    # ЗАписываем таблицу, если не создана
    try:
        db_connection = sql3.connect(DB_NAME)
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
        db_connection.close()
    except sql3.Error as error:
        is_ok_flag = False
        print("Ошибка: ", error.message)  # не уверен, что отработает
    if is_ok_flag:
        print("Таблица создана успешно")

def make_task(text_of_task:str):
    global is_ok_flag
   
    #ввести новую задачу
    date_time_now_obj = datetime.datetime.now()  # Получаем объект дата время 
    date_time_now = date_time_now_obj.strftime('%d.%m.%Y %H:%M')  # Преобразовываем его как нам надо
    print("Add task in list")
    # print(type(date_time_now))
    #Подключаюсь кБД
    try:
        db_connection = sql3.connect(DB_NAME)
        db_cursor = db_connection.cursor()
        db_sql_query = '''INSERT INTO my_todo_list (data_of_creation, todo_text, is_gone) VALUES (?, ?, ?)'''
        adding_datas = [date_time_now, text_of_task, 0]
        
        db_cursor.execute(db_sql_query, adding_datas)
        db_connection.commit()
    except sql3.Error as error:
        
        is_ok_flag = False
        print("Ошибка: ", error.message)
    
    if is_ok_flag:
        print(f"Данные \"{text_of_task}\" записаны успешно")  # вспоминаю как пользоваться f строками 

    #print(sql3.Error.message)

    db_connection.close()


def lisf_of_tasks():
    #выводим списк дел
    print("Print list of tasks\n\n")
    db_connection = sql3.connect(DB_NAME)
    db_cursor = db_connection.cursor()
    db_sql_query = '''SELECT * FROM  my_todo_list'''
    
    
    with db_connection:  # Здесь надо указать именно соединение, а не курсор
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
            counter +=  1
 
    # Выводит, но некрасиво 
    # print()
    # db_cursor.execute(db_sql_query)
    # tables = db_cursor.fetchall()
    # for table in tables:
    #     print(table)
    #     print(table[1])

    db_connection.close()


if __name__ == "__main__":
    print("Привет! Я - консольное todo приложение\n")


if __name__ == "__main__":
    if args.command == "createdb":
        make_db()
    elif args.command == "maketask":
        make_task(args.text)
    elif args.command == "list":
        lisf_of_tasks()