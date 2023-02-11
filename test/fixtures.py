from pytest import fixture
from fastapi.testclient import TestClient

from src.app import app
from src.repositories.books import BookRepository
from src.repositories.comments import CommentRepository
from src.repositories.database import SessionFactory


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
