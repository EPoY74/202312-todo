"""
Цель проекта: API оболочка для todo приложения.
Использованые библиотеки: FastApi
Автор: Евгений Петров
Почта: epoy@gmail.com
Дата начала: 02.10.2024
"""

from fastapi import FastAPI

app_todo = FastAPI()

@app_todo.get('/')
async def root_async():
    """_summary_ Слушает эндпоит "/" и выдает общею информацию об API

    Returns:
        _type_: _description_
    """
    
    return {"mеssage" : "This is API for EPoY's todo app. Since 2023."}

def main_execute():
    """_summary_ Основное тело программы
    """


# if __name__ == "__main__":
#     main_execute()
