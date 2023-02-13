from pytest import fixture
from unittest import mock
from src.errors import BookNotFoundError
from src.services.books_service import BooksService


@fixture
def books_service():
    yield BooksService()


def test_get_ok(books_service: BooksService, isbn):
    response = books_service.get(isbn)

    assert response.author


def test_404(books_service):
    invalid_isbn = 123213
    exception_thrown = False
    try:
        books_service.get(invalid_isbn)
    except BookNotFoundError:
        exception_thrown = True

    assert exception_thrown


def test_persist(books_service: BooksService, isbn, book_repository):
    book = books_service.save(isbn)

    book_from_database = book_repository.get(book_id=book["id"])

    assert book["isbn"] == book_from_database.isbn


def test_search_returns_the_api_response_directly(books_service, isbn):
    with mock.patch("src.providers.openlibrary_provider.requests.get") as patched_get:
        mock_response = mock.MagicMock(status_code=200)
        patched_get.return_value = mock_response
        search_result = books_service.search({"isbn": isbn})
        assert search_result["result"] == mock_response.json()


def test_search_passes_on_the_params_as_request_query_params_and_json_format(
    books_service, isbn
):
    with mock.patch("src.providers.openlibrary_provider.requests.get") as patched_get:
        mock_response = mock.MagicMock(status_code=200)
        patched_get.return_value = mock_response
        books_service.search({"isbn": isbn})
        patched_get.assert_called_once_with(
            mock.ANY, params={"isbn": isbn, "format": "json"}
        )


def test_search_unavailable(books_service, isbn):
    exception_thrown = False
    with mock.patch("src.providers.openlibrary_provider.requests.get") as patched_get:
        mock_response = mock.MagicMock(ok=False)
        patched_get.return_value = mock_response
        try:
            books_service.search({"isbn": isbn})
        except Exception:
            exception_thrown = True

    assert exception_thrown
