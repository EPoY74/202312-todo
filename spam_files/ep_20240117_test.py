"""
Автор: Евгений Петров
Цель: Проверить работу декораторов и написать первый декоратор
Дата: 19.01.2024
"""


import requests as req

def outer(foo):
    def inner(*args, **kwargs):
        print("Start")
        foo(*args, **kwargs)
        print("end")
    return inner

@outer
def load_web_page(site_name: str):
    """
    Автор: Евгений Петров
    Дата: 17.01.2024
    Цель: Проверить скорость загрузки страницы или что-то еще
          для проверки работы работы декоратора 
    """
    
    print(req.get(site_name))




load_web_page("http://ya.ru")