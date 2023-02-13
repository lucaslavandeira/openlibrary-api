from src.repositories.books import Book


def test_example(book_repository):
    book = Book(isbn=123)
    book_repository.add(book)

    result = book_repository.get(book_id=book.id)
    assert result.isbn == book.isbn


def test_database_is_empty(book_repository):
    result = book_repository.get_all()
    assert result
