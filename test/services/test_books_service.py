from pytest import fixture

from src.services.books_service import BookNotFoundError, BooksService


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

    book_from_database = book_repository.get(book_id=book.id)

    assert book.isbn == book_from_database.isbn
