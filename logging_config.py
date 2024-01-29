import logging

# Конфигурирование логгера
FORMAT = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('todologger')