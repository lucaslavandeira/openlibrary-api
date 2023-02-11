from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Session:
    singleton = None

    @classmethod
    def get(cls):
        if cls.singleton is not None:
            return cls.singleton
        engine = create_engine(
            "postgresql://postgres:postgres@localhost/openlibraryapi"
        )
        Base.metadata.create_all(engine)

        # Start a session to interact with the database
        Session = sessionmaker(bind=engine)
        cls.singleton = Session()
        return cls.singleton
