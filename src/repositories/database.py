from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class SessionFactory:
    def __init__(self) -> None:
        self.engine = create_engine("postgresql://postgres:postgres@localhost/postgres")
        Base.metadata.create_all(self.engine)
        self.sessionmaker = sessionmaker(bind=self.engine)

    def get(self):
        return self.sessionmaker()
