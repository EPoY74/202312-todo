def fa():
    print('Функция 1 fa')

def fb():
    print('Функция 2 fb')

def fc():
    print('Фунукция 3 fc')


func_dict ={
    'a': fa,
    'b': fb,
    'c': fc
}

if __name__ =="__main__":
    my_case = ' '
    
    while my_acase:
        try:
            my_case = str(input("Введите a, b или c: "))
            my_func = func_dict[my_case]
            my_func()
        except:
            print("Вы ввели некорректный вариант. Попробуйте еще раз")
