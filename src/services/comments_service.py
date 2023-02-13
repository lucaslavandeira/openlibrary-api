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

    def update(self, comment_id, new_content):
        count = self.comment_repository.update_content(comment_id, new_content)
        if not count:
            raise CommentNotFoundError

    def delete(self, comment_id):
        comment = Comment(id=comment_id)
        if not self.comment_repository.delete(comment):
            raise CommentNotFoundError


class CommentNotFoundError(ValueError):
    pass
