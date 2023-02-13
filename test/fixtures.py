from pytest import fixture
from fastapi.testclient import TestClient

from src.app import app
from src.repositories.books import Book, BookRepository
from src.repositories.comments import CommentRepository
from src.repositories.database import SessionFactory
from src.services.comments_service import CommentsService


@fixture
def test_client():
    yield TestClient(app)


@fixture()
def book_repository():
    yield BookRepository()


@fixture()
def comment_repository():
    yield CommentRepository()


@fixture
def isbn():
    return "9780140328721"


@fixture
def book(isbn, book_repository: BookRepository):
    book = Book(author="Test author", title="Test title", isbn=isbn)
    book_repository.add(book)
    yield book


@fixture
def comments_service():
    yield CommentsService()


@fixture
def comment(book, comments_service):
    yield comments_service.add(book.id, "Test comment")


@fixture(scope="function", autouse=True)
def db_session(request):
    session = SessionFactory().get()
    transaction = session.begin()

    def teardown():
        transaction.rollback()

    request.addfinalizer(teardown)

    return session
