from sqlalchemy import Column, String, create_engine, declarative_base

engine = create_engine("sqlite:///main_db.sqlite3", echo=True)
Base = declarative_base()


class Account(Base):
    __tablename__ = "account"

    email = Column(String, primary_key=True)
    password = Column(String)


Base.metadata.create_all(bind=engine)
