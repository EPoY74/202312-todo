"""
Конфигурирование логгера для
проекта ep20231204_todo_cli.py
Автор: ЕВгений Петров
Почта: p17@mail.ru

"""

import logging
import os

file_directory:str = os.path.dirname(__file__)
logger_file_path:str = os.path.join(
    file_directory,
    '..',
    'log', 'todo_cli.log'
)
print("logger_config: ", logger_file_path)


# Конфигурирование логгера
FORMAT = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.DEBUG,
    filename=logger_file_path,
    filemode="a",
    encoding="utf-8"
    )
logger = logging.getLogger('todologger')
logger.debug("Это тестовое сообщение для проверки логгера.")
