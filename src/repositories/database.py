from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Session:
    singleton = None

    @classmethod
    def get(cls):
        if cls.singleton is None:
            cls.init()
        return cls.singleton

    @classmethod
    def init(cls):
        engine = create_engine("postgresql://postgres:postgres@localhost/postgres")
        Base.metadata.create_all(engine)

        # Start a session to interact with the database
        Session = sessionmaker(bind=engine)
        cls.singleton = Session()

    @classmethod
    def close(cls):
        cls.singleton.close()
