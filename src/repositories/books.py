from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.repositories.database import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(Integer)


class BookRepository:
    def __init__(self, session):
        self.session = session

    def add(self, book):
        self.session.add(book)
        self.session.commit()

    def get(self, book_id):
        return self.session.query(Book).get(book_id)

    def update(self, book):
        self.session.commit()

    def delete(self, book):
        self.session.delete(book)
        self.session.commit()
