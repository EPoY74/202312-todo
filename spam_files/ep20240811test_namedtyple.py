"""
Программа изучает использование namedtyple, и отвязывании
данных от поведения.
Источник: Закрытая группа тестирования учебника Python, Григорий Петров
Автор: Евгений Петров
Почта: p174@mail.ru
ДАта: 20240811
"""
import collections

Teacher = collections.namedtuple('Teacher',
                                 ['name', 'subject'])
Student = collections.namedtuple('Student', ['name'])
type  SchoolPerson = Teacher | Student


def get_name(obj_name: SchoolPerson) -> str:
    """
    Выводит только имя из передаваемого объекта
    """
    return obj_name.name


def get_subject(obj_sub: SchoolPerson):
    """
    Выводит только преподаваемый предмет
    """
    try:
        return obj_sub.subject
    except AttributeError as err:
        if err:
            pass
        return None


teacher = Teacher("Eugenii Petrov", "Programming")
student = Student("Elina Shefer")

print(student.name)
print(teacher.name)

print(get_name(student))
print(get_subject(student))
print(20 * "-")
print(get_name(teacher))
print(get_subject(teacher))
