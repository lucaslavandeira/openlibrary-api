from sqlalchemy import Column, Integer, Text, ForeignKey, select
from sqlalchemy.orm import Session

from src.repositories.database import Base


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    book = Column(Integer, ForeignKey("books.id"), required=True)
    content = Column(Text, required=True)

    def to_dict(self):
        return {
            "id": self.id,
            "book": self.book,
            "content": self.content,
        }


class CommentRepository:
    def __init__(self, session):
        self.session: Session = session

    def add(self, comment):
        self.session.add(comment)
        self.session.commit()
        return comment.id

    def get(self, comment_id):
        return self.session.get(Comment, comment_id)

    def update(self):
        self.session.commit()

    def delete(self, book):
        self.session.delete(book)
        self.session.commit()

    def get_all_for_book(self):
        return self.session.execute(select()).all()
