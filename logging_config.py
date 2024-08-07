import logging

# Конфигурирование логгера

FORMAT = '[%(levelname)s] %(asctime)s - %(message)s'
# logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, filename="ep20231204_todo_cli.log",format=FORMAT,)
logger = logging.getLogger('todologger')