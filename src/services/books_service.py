import requests

from ..repositories.books import BookRepository, Book
from ..repositories.database import SessionFactory


class BooksService:
    endpoint = "https://openlibrary.org/"

    def __init__(self) -> None:
        self.repository = BookRepository()

    def get(self, isbn):
        url = f"{self.endpoint}/isbn/{isbn}.json"
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

    def search(self, params):
        query_params = dict(params)
        query_params["format"] = "json"
        response = requests.get(f"{self.endpoint}/api/books", params=query_params)
        if response.status_code != 200:
            raise RuntimeError
        return {"result": response.json()}


class BookNotFoundError(ValueError):
    pass
