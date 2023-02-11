import requests

from ..repositories.books import BookRepository, Book
from ..repositories.database import SessionFactory


class BooksService:
    endpoint = "https://openlibrary.org/isbn/"

    def __init__(self, session=None) -> None:
        if session is None:
            session = SessionFactory().get()
        self.repository = BookRepository(session)

    def get(self, isbn):
        url = f"{self.endpoint}/{isbn}.json"
        response = requests.get(url)
        if response.status_code == 404:
            raise BookNotFoundError
        book_data = response.json()
        book = Book(
            isbn=isbn, title=book_data["title"], author=book_data["authors"][0]["key"]
        )
        return book

    def save(self, isbn):
        book = self.get(isbn)
        book_response = book.to_dict()
        book_id = self.repository.add(book)
        book_response["id"] = book_id
        return book_response


class BookNotFoundError(ValueError):
    pass
