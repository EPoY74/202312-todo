"""
Описание: Исследую ООП и работу с классами.
Дата: 13 июля 2024 года
Автор: Евгений Петров
Почта: p174@mail.ru
Сайт урока: https://www.youtube.com/watch?v=-Zdu4ntX_DU&list=PLNi5HdK6QEmX9fxp3_IBFx1O5tiTmKlYm&index=2
Объект - единица информации в памяти
Класс - инструкция по созданию объектов определенного типа
Экземпляр - конкретный объект какого-то класса
Метод - функция в классе для воздействия на объект
В параметр self передаётся имя переменной в которой запущен класс
"""


# Создаю класс Purse
class Purse:
    def __init__(self, valuta, name="Unknown"):
        """
        Это конструктор объекта
        Код внутри этого метода выполняется тогда, когда создается экземпляр класса
        Это нужно для того, что бы при создании класса сразу передать какие-либо значения, т.е. свойства
        Переменные в классе называют полями или свойствами.
        Атрибутами называют все ине=мена в классе методов и переменных
        Что бы различать, когда будет создано несколько экземпляров - обязательно писать self
        """

        # Так как есть self, то это свойство конкретного экземпляра
        if valuta not in ("EUR", "USD"):
            # Исключение, что бы ошибку можно было обработать
            raise ValueError("Не соответствие валюты. Можно только EUR или USD")

        self.__money = 0.00
        self.valuta = valuta
        self.name = name

    def top_up_balance(self, howmany):
        """

        # @param howmany:
        @return:
        """
        # Пополнение кошелька, на сколько мы его пополнили. Пополнение суммируется с доступным остатком
        self.__money = self.__money + howmany
        return howmany # возвращаю значение, что бы можно было осуществить перевод (тут до кучи)

    def top_down_balance(self, howmanydown):

        # Расходы с кошелька - сколько потратили. Уменьшает доступный остаток.
        if self.__money < howmanydown:
            print("Недостаточно средств. пополните, пожалуйста, кошелек")
            raise ValueError("Недостаточно средств")  # Исключение, что бы ошибку можно было обработать
        self.__money = self.__money - howmanydown
        return howmanydown  # возвращаю значение, что бы можно было осуществить перевод

    def info(self):
        # Возвращает количество денег в конкретном кошельке
        return f"{self.__money} {self.valuta}"

    def __del__(self):
        # Деструктор, выполняется во время удаления, всегда
        print("Кошелек удален")
        return self.__money


x = Purse("USD")
y = Purse("EUR", "Ann")
print(x.info())
x.money = 150
print(x.info())
print(y.info())
x.top_up_balance(300)
print(x.info())
x.top_down_balance(100)
print(x.info())
# x.top_down_balance(351.1)
# print(x.info())
x.__money = -300
print(x.info())
y.top_up_balance(20)
print(y.info())
x.top_up_balance(y.top_down_balance(10))
print(y.info())
print(x.info())
