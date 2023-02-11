from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import relationship

from src.repositories.database import Base, SessionFactory


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String)

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "author": self.author,
            "id": self.id,
            "title": self.title,
        }


class BookRepository:
    def __init__(self):
        self.session_factory = SessionFactory()

    def add(self, book):
        session = self.session_factory.get()
        session.add(book)
        session.commit()
        return book.id

    def get(self, book_id):
        session = self.session_factory.get()
        return session.get(Book, book_id)

    def get_all(self):
        session = self.session_factory.get()
        return session.execute(select(Book)).all()

