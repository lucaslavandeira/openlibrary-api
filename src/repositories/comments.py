from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime,
    delete,
    select,
    update,
)
from sqlalchemy.orm import Session

from src.repositories.database import Base, SessionFactory


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    book = Column(Integer, ForeignKey("books.id"))
    content = Column(Text)
    created_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "book": self.book,
            "content": self.content,
            "created_at": self.created_at,
        }


class CommentRepository:
    def __init__(self):
        self.session_factory = SessionFactory()

    def add(self, comment):
        session = self.session_factory.get()
        session.add(comment)
        session.commit()
        return comment.id

    def get(self, comment_id):
        session = self.session_factory.get()
        return session.get(Comment, comment_id)

    def update_content(self, comment_id, new_content):
        session = self.session_factory.get()
        result = session.execute(
            update(Comment).where(Comment.id == comment_id).values(content=new_content)
        )
        session.commit()
        return result.rowcount

    def delete(self, comment):
        session = self.session_factory.get()
        result = session.execute(delete(Comment).where(Comment.id == comment.id))
        session.commit()
        return result.rowcount

    def get_all_for_book(self, book):
        session = self.session_factory.get()
        results = session.execute(select(Comment).where(Comment.book == book.id)).all()
        return [x[0] for x in results]

    def list_for_book(self, book, offset=0, limit=10):
        session = self.session_factory.get()
        results = session.execute(
            select(Comment)
            .where(Comment.book == book.id)
            .order_by(Comment.created_at)
            .limit(limit)
            .offset(offset)
        )
        return [x[0] for x in results]
