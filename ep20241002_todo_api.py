"""
Цель проекта: API оболочка для todo приложения.
Использованые библиотеки: FastApi
Автор: Евгений Петров
Почта: epoy@gmail.com
Дата начала: 02.10.2024
"""

from fastapi import FastAPI

import db_working_api

from logging_cfg import logger

app_todo = FastAPI()

print("""\nAPI: Консольное приложение для ведения задач.
        \nАвтор: Евгений Б. Петров, p174@mail.ru\n""")


# Использую имя БД явно для тестирования.
# Позже надо будет прикрутить файл конфигурации для API тоже
db_name: str = "ep20231204_todo_cli.db"

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
