"""
программа изучает использование namedtyple, и отвязывании
данных от поведения.
Источник: ЗАкрытая группа тестирования УЧЕБНИКА pYTHON, ГРирорий Петров
Автор: Евгений Петров
Почта: p174@mail.ru
ДАта: 20240811
"""
import collections
import typing

Teacher = collections.namedtuple('Teacher', {'name': str , 'subject': str})
Student = collections.namedtuple('Student', {'name': str})
type = SchoolPerson = Teacher | Student


def get_name(obj: SchoolPerson) -> str:
    return obj.name


teacher = Teacher("Eugernii Petrov", "Programming")
student = Student("Elina Shefer")

print(student.name)
print(teacher.name)

print(get_name(student))
print(get_name(teacher))
