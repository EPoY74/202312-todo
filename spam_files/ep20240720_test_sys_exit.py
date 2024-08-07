"""
Цель: Проверка работы выхода из программы с помощью sys.exit()
и перехвата исключения
Автор: ЕВгений Б. Петров
email: p174@mail.ru
"""

import sys

def my_foo():
    """
    Цель: Эта функция непосредственно реализует проверку выхода из программы
    """
    try:
        print("Выполнение foo")
        sys.exit(3)
    except SystemExit as e:
        print(f"перехвачено исключение SystemExit: {e}")


if __name__ == "__main__":
    my_foo()
