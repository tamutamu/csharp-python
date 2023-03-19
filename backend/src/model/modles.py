from datetime import datetime

from sqlalchemy import DATETIME, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BackendResult(Base):
    __tablename__ = "backend_result"

    thread_id: int | None = Column(Integer, primary_key=True)
    seq: int = Column(Integer, autoincrement=True)
    result: str = Column(String)

    created: datetime = Column("created", DATETIME, default=datetime.now, nullable=False)
    modified: datetime = Column("modified", DATETIME, default=datetime.now, nullable=False)