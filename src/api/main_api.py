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

import uvicorn

# from src.cfg.cfg_working import search_config_and_db
from src.cfg import cfg_working

# from src.db_access import db_working_api
import src.db_access.db_working_api as db_working_api

from src.cfg.logger_config import logger
# import src.cfg.logger_config

colorama.init()
app_todo = FastAPI()

# # Получаем объект дата время
# date_time_now_obj = datetime.now()

# # Преобразовываем его как нам надо
# date_time_now = date_time_now_obj.strftime('%d.%m.%Y %H:%M')

# Оказывается можно и так, что бы не плодить переменные
date_time_now_new = datetime.now().strftime('%d.%m.%Y %H:%M')

print(colorama.Fore.YELLOW + "\nЗапущено в " + date_time_now_new)
print("API: Консольное приложение для ведения задач.")
print("Запуск необходим через команду: uvicorn main_api:app_todo --reload")
print("Автор: Евгений Б. Петров, p174@mail.ru\n")


# Получаю имя базы данных из файла с конфигурацией
db_name: str = db_working_api.get_db_name(cfg_working.search_config_and_db())

logger.info("API: Старт консольного ToDo приложения.")

@app_todo.get('/')
async def root_async():
    """Слушает эндпоит "/" и выдает общюю информацию об API
    Returns:
        Возвращает общую информацию о данном API
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
async def show_one_task_async(task_id: str):
    """Выводит запись в БД c номером task_id
    """
    logger.info("API: Обращение с API по роуту '/task/{task_id}', где task_id = %s", task_id)

    return db_working_api.list_of_tasks_json(db_name, all_or_last="one", id_row = int(task_id))


# def start_todo_api_app():
#     """Запуск API для проложения todo
#     """
#     # uvicorn.run("main:app_todo", host="127.0.0.1", port=8000, reload=True)
#     # uvicorn.run(app_todo, reload=True)

# if __name__ == "__main__":
#     start_todo_api_app()
