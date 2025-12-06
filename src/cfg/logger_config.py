"""
Конфигурирование логгера для
проекта ep20231204_todo_cli.py
Автор: Евгений Петров
Почта: p17@mail.ru
"""

import logging
import os

LOG_FILENAME: str = "todo_cli.log"

file_directory: str = os.path.dirname(__file__)
logger_dir: str = os.path.join(file_directory, "..", "log")
logger_file_path: str = os.path.join(logger_dir, LOG_FILENAME)
print("logger_config: ", logger_file_path)
os.makedirs(logger_dir, exist_ok=True)
if not os.path.exists(logger_file_path):
    open(logger_file_path, "a").close()

# Конфигурирование логгера
FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(
    format=FORMAT,
    level=logging.DEBUG,
    filename=logger_file_path,
    filemode="a",
    encoding="utf-8",
)
logger = logging.getLogger("todologger")
logger.debug("Это тестовое сообщение для проверки логгера.")
