from unittest import mock
from pytest import fixture
from src.errors import BookNotFoundError

from src.providers.openlibrary_provider import OpenLibraryProvider
from src.repositories.books import Book


@fixture()
def mock_provider():
    with mock.patch(
        "src.services.books_service.OpenLibraryProvider",
        return_value=mock.MagicMock(OpenLibraryProvider),
    ) as m:
        yield m()


def test_get_book(test_client, isbn, mock_provider):
    mock_provider.get_book_by_isbn.return_value = Book(
        isbn=isbn, title="Test title", author="Test author"
    )
    response = test_client.get(f"/books/{isbn}")
    assert response.status_code == 200


def test_get_book_invalid(test_client, mock_provider):
    invalid_isbn = 123123
    mock_provider.get_book_by_isbn.side_effect = BookNotFoundError

    response = test_client.get(f"/books/{invalid_isbn}")
    assert response.status_code == 404


def test_post_book(test_client, book_repository, isbn, mock_provider):
    mock_provider.get_book_by_isbn.return_value = Book(
        isbn=isbn, title="Test title", author="Test author"
    )
    response = test_client.post(f"/books/{isbn}")
    assert response.status_code == 201
    body = response.json()
    book_from_database = book_repository.get(book_id=body["id"])
    assert book_from_database.isbn == body["isbn"]
