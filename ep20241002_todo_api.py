"""
Цель проекта: API оболочка для todo приложения.
Использованые библиотеки: FastApi
Автор: Евгений Петров
Почта: epoy@gmail.com
Дата начала: 02.10.2024
"""

from datetime import datetime
from fastapi import FastAPI
import colorama 

from cfg_working import search_config_and_db
import db_working_api

from logging_cfg import logger

colorama.init()
app_todo = FastAPI()

# Получаем объект дата время
date_time_now_obj = datetime.now()

# Преобразовываем его как нам надо
date_time_now = date_time_now_obj.strftime('%d.%m.%Y %H:%M')
date_time_now_new = datetime.now().strftime('%d.%m.%Y %H:%M')

print(colorama.Fore.YELLOW + "\nЗапeщено в " + date_time_now)
print("API: Консольное приложение для ведения задач.")
print("Автор: Евгений Б. Петров, p174@mail.ru\n")


# Получаю имя базы данных из файла с конфигурацией
db_name: str = db_working_api.get_db_name(search_config_and_db())

logger.info("API: Старт консольного ToDo приложения.")

@app_todo.get('/')
async def root_async():
    """_summary_ Слушает эндпоит "/" и выдает общею информацию об API

    Returns:
        _type_: _description_
    """
    logger.info("API: Обращние с API по роуту '/'")

    return {"mеssage" : "This is API for EPoY's todo app. Since 2023."}


@app_todo.get("/all")
async def show_all_tasks_async():
    """Выводит все записи, которые есть в БД
    """
    logger.info("API: Обращение с API по роуту '/all'")

    return db_working_api.list_of_tasks_json(db_name)


@app_todo.get("/last")
async def show_last_tasks_async():
    """Выводит последнюю запись в БД
    """
    logger.info("API: Обращение с API по роуту '/last'")

    return db_working_api.list_of_tasks_json(db_name, all_or_last="last")


@app_todo.get("/task/{task_id}")
async def show_one_task_async(task_id: int):
    """Выводит запись в БД c номером task_id
    """
    logger.info("API: Обращение с API по роуту '/task/{task_id}'")

    return db_working_api.list_of_tasks_json(db_name, all_or_last="one", id_row = task_id)


def main_execute():
    """_summary_ Основное тело программы
    """


# if __name__ == "__main__":
#     main_execute()
