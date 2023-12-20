# 202311-ToDo: список задач
 Программа для создания ToDo заданий.
 
 Работает в консольном режиме - позволяет добавлять задания(таски) из командной строки.

 
 
Умеет добавлять зпапись, удалять запись, выводить список записей и помечать запись сделанной так же устанавливать срок исполнения.



2023.12.20


Поддерживаемые  аргументы:

Новая:

--task_deadline, Устанавлявает дату, до которой надо выполнить задание: --task_deadline номер_записи

Ранее поддерживаемые:

--create_db, Создаем базу данных для списка задач

--task_add, Описание задачи, которую заводим: --task_add "Это запись"

--task_list, Выводит список задач

--task_gone_date, Помечает задание с номером № завершенным: --set_gone_date №

--task_del_id, Удаляет запись с номером: --task_del_id №


Базовый комплект:

ep20231204_todo_cli.py - приложение ToDo в командной строке

При первом запуске самостоятельно в диалоговом режиме подготовит файл когфигурации и создаст базу данны. Имя конфигурации и имя БД формируются автоматически. 

В дальнейших планах изменять, развивать и добавлять.

--- Ранее ---

2023.12.19
Поддерживаемые  аргументы:

--create_db, Создаем базу данных для списка задач
--task_add, Описание задачи, которую заводим: --task_add "Это запись"
--task_list, Выводит список задач
--task_deadline, Устанавлявает дату, до которой надо выполнить задание: --task_deadline номер_записи
--task_gone_date, Помечает задание с номером № завершенным: --set_gone_date №
--task_del_id, Удаляет запись с номером: --task_del_id №
    

