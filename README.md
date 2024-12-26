# 202312-todo: список задач
 Программа для создания ToDo заданий.
 
---

## Запуск проекта

Команда python -m src.cli - работает в консольном режиме - позволяет добавлять задания(таски) из командной строки.

Команда python -m src.api - работает в режиме API, возвращает json. 
 

---

## Команды для использования CLI части:

### Запуск CLI части приложения:
 
 python -n src.cli - выведет помощь по использованию приложения


## Базовые команды для использования CLI части приложения:

--create_db: Создаем базу данных для списка задач

--task_add: Описание задачи, которую заводим
    Пример использования:  python -m src.cli --task_add "Это запись" 

--task_deadline: Устанавлявает дату, до которой надо выполнить задание:
    Пример: python -m src.cli --task_deadline номер_записи

--task_list: Выводит список задач

--task_done_date: Помечает задание с номером № завершенным:
    Пример: python -m src.cli --task_done_date номер_записи

--task_del_id: Удаляет запись с указанным номером:
    Пример: python -m src.cli--task_del_id номер_записи