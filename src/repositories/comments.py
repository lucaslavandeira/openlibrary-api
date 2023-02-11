from sqlalchemy import Column, Integer, Text, ForeignKey, delete, select, update
from sqlalchemy.orm import Session

from src.repositories.database import Base, SessionFactory


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    book = Column(Integer, ForeignKey("books.id"))
    content = Column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "book": self.book,
            "content": self.content,
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
        session.execute(
            update(Comment).where(Comment.id == comment_id).values(content=new_content)
        )
        session.commit()

    def delete(self, comment):
        session = self.session_factory.get()
        session.execute(delete(Comment).where(Comment.id == comment.id))
        session.commit()

    def get_all_for_book(self, book):
        session = self.session_factory.get()
        results = session.execute(select(Comment).where(Comment.book == book.id)).all()
        return [x[0] for x in results]
