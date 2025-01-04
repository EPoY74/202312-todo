"""Для запуска api  приложения
"""

import os
import sys
import uvicorn

#from src.api.main_api import start_todo_api_app
# from src.api.main_api import app_todo

if not __package__:
    #  Сделать CLI запускаемым из исходного дерева с помощью
    # python src/pakage
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

def main():
    """пробую запускать api приложение
    """
    uvicorn.run("src.api.main_api:app_todo", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
    # start_todo_api_app()
