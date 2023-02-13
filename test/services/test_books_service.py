from pytest import fixture
from unittest import mock
from src.errors import BookNotFoundError
from src.repositories.books import Book
from src.services.books_service import BooksService


def test_get_ok(books_service: BooksService, isbn, mock_provider):
    mock_provider.get_book_by_isbn.return_value = Book(
        isbn=isbn, title="Test title", author="Test author"
    )
    response = books_service.get(isbn)

    assert response.author


def test_404(books_service, mock_provider):
    mock_provider.get_book_by_isbn.side_effect = BookNotFoundError
    invalid_isbn = 123213
    exception_thrown = False
    try:
        books_service.get(invalid_isbn)
    except BookNotFoundError:
        exception_thrown = True

    assert exception_thrown


def test_persist(books_service: BooksService, isbn, book_repository, mock_provider):
    mock_provider.get_book_by_isbn.return_value = Book(
        isbn=isbn, title="Test title", author="Test author"
    )
    book = books_service.save(isbn)

    book_from_database = book_repository.get(book_id=book["id"])

    assert book["isbn"] == book_from_database.isbn


def test_search_returns_the_api_response_directly(books_service, isbn, mock_provider):
    mock_provider.search_books.return_value = {}

    search_result = books_service.search({"isbn": isbn})
    assert search_result["result"] == {}
