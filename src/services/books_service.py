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
            return {"status": "not found"}
        return response.json()

    def save(self, isbn):
        book_data = self.get(isbn)
        book = Book(title=book_data["title"], author=book_data["author"], isbn=isbn)
        self.repository.add(book)
        return book
