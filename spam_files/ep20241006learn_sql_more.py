"""Тыкаю палкой sqlite
"""

import sqlite3

if __name__ == "__main__":
    sql_query: str = "SELECT * FROM my_todo_list"
    db_name = "ep20231204_todo_cli.db"

    with (sqlite3.connect(db_name, uri=True)) as db_conn:
        db_cur = db_conn.cursor()
        db_cur.execute(sql_query)
        db_executed_sql = db_cur.fetchall()
        for row in db_executed_sql:
            print(row)

        print(dir(db_executed_sql))

        # db_conn.close()

# import sqlite3
#
# if __name__ == "__main__":
#     sql_query = "SELECT * FROM my_todo_list"
#     db_name = "ep20231204_todo_cli.db"
#
#     with sqlite3.connect(db_name) as db_conn:
#         db_cur = db_conn.cursor()
#         db_cur.execute(sql_query)
#         db_executed_sql = db_cur.fetchall()
#         print(db_executed_sql)
