from pytest import fixture

from src.repositories.books import Book, BookRepository
from src.repositories.comments import Comment


@fixture
def book(isbn, book_repository: BookRepository):
    book = Book(author="Test author", title="Test title", isbn=isbn)
    book_repository.add(book)
    yield book


def test_create_comment(book, comment_repository):
    comment = Comment(book=book.id, content="This is my test comment")
    comment_repository.add(comment)

    assert comment_repository.get_all_for_book(book)[0].id == comment.id
