--
-- File generated with SQLiteStudio v3.4.18 on Пн дек 8 10:21:28 2025
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: my_todo_list
CREATE TABLE IF NOT EXISTS my_todo_list (
    id               INTEGER PRIMARY KEY,
    data_of_creation,
    date_max         TEXT,
    todo_text        TEXT,
    is_gone          INTEGER,
    date_of_gone     TEXT
);

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             1,
                             '11.12.2023 02:57',
                             '12.12.2023 13:45',
                             'Записать задание',
                             1,
                             '25.01.2024 23:01'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             3,
                             '11.12.2023 03:08',
                             '12.12.2023 12:23',
                             'Записать еще одно задание задание',
                             1,
                             '25.01.2024 23:04'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             4,
                             '11.12.2023 03:14',
                             '12.12.2023 12:00',
                             'Проверить, сработает ли команда add',
                             1,
                             '25.01.2024 23:14'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             5,
                             '11.12.2023 03:36',
                             NULL,
                             'Проверяю, сработает ли импорт только одного класса',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             7,
                             '11.12.2023 17:03',
                             NULL,
                             'Проверяю, почему не работает',
                             1,
                             '03.10.2024 21:58'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             8,
                             '11.12.2023 17:57',
                             NULL,
                             'Проверяю, запишется ли БД',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             10,
                             '11.12.2023 18:01',
                             NULL,
                             'Проверяю, запишется ли БД еще раз',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             12,
                             '12.12.2023 08:26',
                             NULL,
                             'Проверяю запись в файл снова',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             13,
                             '12.12.2023 08:27',
                             NULL,
                             'Проверяю запись в файл снова после того, как поправил',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             14,
                             '18.12.2023 11:36',
                             NULL,
                             'Делаю добавление и проверю за одно вывод красивой таблицы для одной строки',
                             1,
                             '18.12.2023 23:53'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             15,
                             '18.12.2023 11:50',
                             NULL,
                             'Делаю добавление и проверю за одно вывод красивой таблицы для одной строки и заодно проверяю ограничение по ширине 150 символов',
                             1,
                             '19.12.2023 00:09'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             16,
                             '18.12.2023 12:03',
                             NULL,
                             'Делаю добавление и проверю за одно вывод красивой таблицы для одной строки и заодно проверяю ограничение по ширине 150 символов и еще раз пробую, при этом буду писать достаточно длинный текст и посмотрим, как это будет выводиться',
                             1,
                             '25.01.2024 23:17'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             17,
                             '18.12.2023 13:28',
                             NULL,
                             'Добавляю 11 запись',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             18,
                             '18.12.2023 13:29',
                             NULL,
                             'Добавляю 12 запись',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             19,
                             '18.12.2023 13:45',
                             NULL,
                             'Запись 13 111 222 333',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             20,
                             '18.12.2023 13:46',
                             NULL,
                             'Запись 14 тоже проверил',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             21,
                             '18.12.2023 14:16',
                             '26.01.2023 12:30',
                             'Запись 15 тоже добавлена',
                             1,
                             '18.12.2023 21:59'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             22,
                             '18.12.2023 14:16',
                             '22.12.2023 13:00',
                             'Запись 15 тоже добавлена',
                             1,
                             '18.12.2023 22:31'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             23,
                             '19.12.2023 00:11',
                             '25.12.2023 14:30',
                             'Начать добавлять задания в данную таблицу, что бы тут их можно было тоже фиксировать',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             24,
                             '19.12.2023 00:12',
                             NULL,
                             'TODO',
                             1,
                             '19.12.2023 00:14'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             25,
                             '19.12.2023 00:12',
                             NULL,
                             'TODO: разобраться до конца с файлом конфигурации и начать спрашивать название БД и делать ini если его нет',
                             1,
                             '27.01.2024 21:49'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             26,
                             '19.12.2023 00:12',
                             NULL,
                             'TODO: использовать ORM взаимодействия с базой, например http://docs.peewee-orm.com/en/latest/',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             27,
                             '19.12.2023 11:09',
                             NULL,
                             'Проверяю создание записи в БД, позже так же помечу эту запись завершенной',
                             1,
                             '19.12.2023 11:14'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             29,
                             '23.01.2024 22:06',
                             NULL,
                             'Проверяю, что возвращает метод .execute',
                             1,
                             '27.01.2024 20:54'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             30,
                             '23.01.2024 22:10',
                             NULL,
                             'Проверяю, что возвращает метод .execute еще раз',
                             1,
                             '27.01.2024 20:28'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             31,
                             '21.12.2024 19:39',
                             '23.12.2024 12:00',
                             'Записываю задание, запуская модуль, как скрипт',
                             1,
                             '21.12.2024 19:48'
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             32,
                             '03.11.2025 10:06',
                             NULL,
                             'ПРОВЕСТИ ТО СЕРВЕРА 1',
                             0,
                             NULL
                         );

INSERT INTO my_todo_list (
                             id,
                             data_of_creation,
                             date_max,
                             todo_text,
                             is_gone,
                             date_of_gone
                         )
                         VALUES (
                             33,
                             '06.12.2025 10:33',
                             NULL,
                             'Проверяю запись в БД после Ruff формата SQL запроса',
                             0,
                             NULL
                         );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
