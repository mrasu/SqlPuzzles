from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def get_session():
    engine = create_engine("mysql+pymysql://root@localhost/sql_puzzles", echo=True)

    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

session = get_session()
