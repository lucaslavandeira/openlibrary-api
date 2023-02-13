from datetime import datetime
from src.repositories.books import BookRepository
from src.repositories.comments import Comment, CommentRepository
from src.errors import BookNotFoundError

from src import config


class CommentsService:
    def __init__(self) -> None:
        self.book_repository = BookRepository()
        self.comment_repository = CommentRepository()

    def add(self, book_id: int, content: str):
        book = self.book_repository.get(book_id)
        if book is None:
            raise BookNotFoundError
        created_at = datetime.now()
        comment = Comment(book=book.id, content=content, created_at=created_at)
        comment_id = self.comment_repository.add(comment)
        response = comment.to_dict()
        response["id"] = comment_id
        return response

    def update(self, book_id, comment_id, new_content):
        book = self.book_repository.get(book_id)
        if book is None:
            raise BookNotFoundError

        count = self.comment_repository.update_content(comment_id, new_content)
        if not count:
            raise CommentNotFoundError

    def delete(self, book_id, comment_id):
        book = self.book_repository.get(book_id)
        if book is None:
            raise BookNotFoundError

        comment = Comment(id=comment_id)
        if not self.comment_repository.delete(comment):
            raise CommentNotFoundError

    def list_for_book(self, book_id, offset=0, limit=config.PAGINATION_DEFAULT_LIMIT):
        # Maybe these offset and limit should be validated, but pragmatically FastAPI does it for us at the controller level automatically.
        book = self.book_repository.get(book_id)
        if book is None:
            raise BookNotFoundError

        comments = self.comment_repository.list_for_book(book, offset, limit)
        return [comment.to_dict() for comment in comments]

    def get(self, book_id, comment_id):
        book = self.book_repository.get(book_id)
        if book is None:
            raise BookNotFoundError

        comment = self.comment_repository.get(comment_id)
        return comment


class CommentNotFoundError(ValueError):
    pass
