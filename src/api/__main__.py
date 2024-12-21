"""Для запуска api  приложения
"""

import uvicorn
from main_api import app_todo

def main():
    """пробую запускать api приложение
    """
    uvicorn.run(app_todo, reload=True)

if __name__ == "__main__":
    main()
