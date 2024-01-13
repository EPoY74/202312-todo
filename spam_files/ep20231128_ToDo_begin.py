import sqlite3
import os

list_of_db_fields: list = ["data_of_creation", #дата создвния 
                          "date_max", #  дата максимального исполнения задания
                          "todo_text", # текст задания
                          "is_gone",  # выполнено ли задание
                          "date_of_gone", # дата исполнения
                          ]

if __name__ == "__main__":

    list_of_datas = ['' for n in range(9)]

    # Создаю подключение к безе данных, если её нет, то БД создается
    db_connection = sqlite3.connect('ep20231129ToDo.db')  #  ep20231129ToDo.db имя базы
    # закрываю подключение к базе данных
    db_connection.close()

    # Устанавливаю соединение с БД
    db_connection = sqlite3.connect('ep20231129ToDo.db')
    db_cursor = db_connection.cursor()  # Формирую курсор для БД, что бы получать и писать данные

    # создаем таблицу, если создана, то не создаем
    db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_todo_list(
    id INTEGER PRIMARY KEY,
    data_of_creation TEXT NOT NULL,
    date_max TEXT NOT NULL,
    todo_text TEXT NOT NULL,
    is_gone integer,
    date_of_gone TEXT NOT NULL
    )
    ''')

    db_connection.commit()  # Записал в БД
    db_connection.close()  # Закрыл соединение с БД


    print("Yello")
    
    # db_connection = sqlite3.connect('ep20231119begin.db')
    # db_cursor = db_connection.cursor()  # формирую курсор, что писать и получать данные с БД

    # db_insert_and_params = '''INSERT INTO Zayavki(data_zyavki,
    #      nomer_obekta,
    #       adres_obekta,
    #        otvetstvennoe_litso,
    #         neispravnost,
    #          tehnik,
    #          vremya_na_obekte,
    #           rezultat,
    #            sotrudnik)
    #             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'''

    # for path in paths:
    #     my_doc = Document(path)

    #     # выделяю только имя файла, так как в нем дата заявок

    #     # разделяю на имя файла(file_name_full) и путь (path_to_file)
    #     path_to_file, file_name_full = os.path.split(path)

    #     # print(path_to_file, file_name_full)

    #     # выделяю имя файла без расширения
    #     file_name_only = os.path.splitext(file_name_full)
    #     print(file_name_only[0])

    #     # выводил текст в файле, но его там мало - так что отключил пока что
    #     # for take_paragraph in my_doc.paragraphs:
    #     #     print(take_paragraph.text)

    #     for table in my_doc.tables:
    #         for row in table.rows:
    #             position_in_string = 0  # когда начинается новая строка - чищу переменную
    #             list_of_datas[0] = str(file_name_only[0])
    #             position_in_string += 1
    #             for cell in row.cells:

    #                 # удаляю перенос строки, если он присутствует
    #                 if '\n' in cell.text:
    #                     only_printable_string = ''.join(char for char in cell.text if char not in "\n")

    #                     # Проверю, записывается ли старое значение, из прошлой строки
    #                     # или просто тянутся хвостом повторы.
    #                     # Старое значение остаётся. Ячейка специально не чистится,
    #                     # будем чистить вручную
    #                     cell.text = ''
    #                 else:
    #                     only_printable_string = cell.text

    #                     # Проверю, записывается ли старое значение, из прошлой строки
    #                     # или просто тянутся хвостом повторы.
    #                     # Старое значение остаётся. Ячейка специально не чистится,
    #                     # будем чистить вручную
    #                     cell.text = ''

    #                 # print(only_printable_string)
    #                 list_of_datas[position_in_string] = only_printable_string  # записываю ячейку в список
    #                 position_in_string += 1

    #             print(list_of_datas)
    #             db_cursor.execute(db_insert_and_params, list_of_datas)
    #             db_connection.commit()

    # db_connection.close()
