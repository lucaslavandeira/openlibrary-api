import pytest
import sqlalchemy as db
from src.repositories.database import SessionFactory
from src.repositories.books import Book


@pytest.fixture(scope="function", autouse=True)
def db_session(request):
    session = SessionFactory().get()
    transaction = session.begin()

    def teardown():
        transaction.rollback()

    request.addfinalizer(teardown)

    return session


def test_example(book_repository):
    book = Book(isbn=123)
    book_repository.add(book)

    result = book_repository.get(book_id=book.id)
    assert result.isbn == book.isbn


def test_database_is_empty(book_repository):
    result = book_repository.get_all()
    assert result
