import os
from logging import getLogger

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session as BaseSession

LOGGER = getLogger(__name__)
global Session
# mypy: ignore-errors
Session: BaseSession = None

global engine


def get_session():
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def setup():
    global engine
    engine = create_engine("sqlite:///main_db.sqlite3", echo=False)
    # Base.metadata.create_all(bind=engine, tables=[BackendResult.__table__])

    alembic_cfg = Config(os.path.join("src", "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

