""" Модуль для работы с таблицей.
Вынес пока сюда, така как данная функция больше нику пока не вписывается.
Автор: Евгений Петров
Почта: p174@mail.ru
"""


from prettytable import PrettyTable


# шапка таблицы, что бы не окарать, когда меняешь пареметры
def table_header(todo_table_header):
    """
    Функция выводит шапку таблицы с заранее заданными пареметрами
    """
    # global todo_table

    todo_table_header.field_names = ["Номер",
                              "Дата создания",
                              "Исполнение до",
                              "Задание",
                              "Исполнено",
                              "Дата исполнения"]
    # todo_table._max_width = {"Задание": 60}
    todo_table_header.max_width["Задание"] = 35

    todo_table_header.min_width["Задание"] = 35
    todo_table_header.min_width["Исполнение до"]  =  16
    todo_table_header.min_width["Исполнено"] = 16
    todo_table_header.min_width["Дата исполнения"] =  16

    todo_table_header.align["Задание"] = "l"
