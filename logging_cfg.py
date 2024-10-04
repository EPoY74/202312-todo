"""
Конфигурирование логгера для
проекта ep20231204_todo_cli.py
Автор: ЕВгений Петров
Почта: p17@mail.ru

"""

import logging


# Конфигурирование логгера
FORMAT = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('todologger')
# TODO: логировать в файл, а не в консоль
