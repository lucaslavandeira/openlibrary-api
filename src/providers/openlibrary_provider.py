import requests

from src.errors import BookNotFoundError
from src.repositories.books import Book
from src import config


class OpenLibraryProvider:
    def __init__(self, endpoint=None) -> None:
        self.endpoint = endpoint or config.OPEN_LIBRARY_PROVIDER_ENDPOINT

    def get_book_by_isbn(self, isbn):
        url = f"{self.endpoint}/isbn/{isbn}.json"
        response = requests.get(url)
        if response.status_code == 404:
            raise BookNotFoundError
        book_data = response.json()
        authors = book_data.get("authors", [])
        if not authors:
            author = None
        else:
            author = authors[0].get("key")
        return Book(isbn=isbn, title=book_data.get("title"), author=author)

    def search_books(self, query) -> dict:
        query_params = dict(query)
        query_params["format"] = "json"
        response = requests.get(f"{self.endpoint}/api/books", params=query_params)
        if not response.ok:
            raise OpenLibraryAPIError
        return response.json()


class OpenLibraryAPIError(RuntimeError):
    pass
