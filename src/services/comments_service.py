from datetime import datetime
from src.repositories.books import BookRepository
from src.repositories.comments import Comment, CommentRepository
from src.services.books_service import BookNotFoundError


class CommentsService:
    def __init__(self) -> None:
        self.book_repository = BookRepository()
        self.comment_repository = CommentRepository()

    def add(self, book_id: int, content: str):
        book = self.book_repository.get(book_id)
        if book is None:
            raise BookNotFoundError
        comment = Comment(book=book.id, content=content, created_at=datetime.now())
        return self.comment_repository.add(comment)
