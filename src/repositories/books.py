from sqlalchemy import Column, Integer, String, select

from src.repositories.database import Base


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
    def __init__(self, session):
        self.session = session

    def add(self, book):
        self.session.add(book)
        self.session.commit()
        return book.id

    def get(self, book_id):
        return self.session.get(Book, book_id)

    def update(self, book):
        self.session.commit()

    def delete(self, book):
        self.session.delete(book)
        self.session.commit()

    def get_all(self):
        return self.session.execute(select(Book)).all()
