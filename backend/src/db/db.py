import sqlite3

import config
from util.log import error_trace


def get_conn():
    dbname = config.DB_NAME
    return sqlite3.connect(dbname)


def exec_sql(sql_list):
    conn = get_conn()
    try:
        cur = conn.cursor
        for sql in sql_list:
            cur.execute(sql)

    except Exception as e:
        error_trace(e)
    finally:
        conn.close()
