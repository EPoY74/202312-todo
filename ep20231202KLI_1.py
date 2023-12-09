import argparse
# Создаеём объект персер, который  будет отвечать за аргумент адресной строки
parser = argparse.ArgumentParser()
# Создаём два позиционных аргумента (то есть первый аргумент 
# попадёт в "a", а второй в "b")
# При создании аргументов можем указать тип данных (type),
#  который хотим принять и подсказку (help)
parser.add_argument('a', type = int, help = "Первый аргумент")
parser.add_argument('b', type = int, help = "Второй аргумент")
parser.add_argument('my_operation', type = str, help = 'Операцию, которую надо сделать: + - * /')
# Создаём объект args. Он будет содержать все принятые агрументы

args =  parser.parse_args()

def f(a = 1, b = 1, my_operation = '+'):
    if  my_operation == "+":
        print(a + b)
    elif my_operation == '-':
        print(a - b)
    elif my_operation == '*':
        print(a * b)
    elif my_operation == '/':
        if b != 0:
            print(a / b)
        else:
            print("Деление на 0 не возможно.")
    else:
        print(" Такую операцию пока не делаю")

if __name__ == "__main__":
    f(args.a, args.b, args.my_operation)