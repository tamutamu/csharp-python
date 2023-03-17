import sqlite3

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

import config
from util.log import error_trace


def setup():
    engine = create_engine("sqlite:///main_db.sqlite3", echo=True)
    Base = declarative_base()

    class Account(Base):
        __tablename__ = "account"

        email = Column(String, primary_key=True)
        password = Column(String)

    Base.metadata.create_all(bind=engine)


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
