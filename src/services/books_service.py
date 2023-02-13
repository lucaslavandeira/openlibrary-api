from src.providers.openlibrary_provider import OpenLibraryProvider

from ..repositories.books import BookRepository


class BooksService:
    endpoint = "https://openlibrary.org/"

    def __init__(self) -> None:
        self.repository = BookRepository()
        self.provider = OpenLibraryProvider(self.endpoint)

    def get(self, isbn):
        return self.provider.get_book_by_isbn(isbn)

    def save(self, isbn):
        book = self.get(isbn)
        book_response = book.to_dict()
        book_id = self.repository.add(book)
        book_response["id"] = book_id
        return book_response

    def search(self, params):
        response = self.provider.search_books(params)
        return {"result": response}
