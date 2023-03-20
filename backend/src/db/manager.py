import sqlite3
from logging import getLogger

import ulid
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session as BaseSession

import config
from model.tables import BackendResult
from util.log import error_trace

LOGGER = getLogger(__name__)
global Session
Session: BaseSession = None

global engine


def get_session():
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def setup():
    Base = declarative_base()
    global engine
    engine = create_engine("sqlite:///main_db.sqlite3", echo=True)
    Base.metadata.create_all(bind=engine, tables=[BackendResult.__table__])


class BackendResultManager:
    def __init__(self) -> None:
        self.id = ulid.new().str
        self.session = get_session()
        self.seq = 0

    def add(self, result):
        try:
            br = BackendResult()
            br.id = self.id
            br.seq = self.seq
            br.result = result
            self.session.add(br)
        except Exception as e:
            pass
        finally:
            self.seq += 1

    def commit(self):
        self.session.commit()


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
