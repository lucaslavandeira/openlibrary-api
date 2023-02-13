from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from src import config

Base = declarative_base()


class SessionFactory:
    def __init__(self) -> None:
        self.engine = create_engine(config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.sessionmaker = sessionmaker(bind=self.engine)

    def get(self):
        return self.sessionmaker()
