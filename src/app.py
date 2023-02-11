from fastapi import FastAPI, Response
from .services.books_service import BookNotFoundError, BooksService


app = FastAPI()


@app.get("/books/{isbn}")
def get_by_isbn(isbn: str, response: Response):
    try:
        book = BooksService().get(isbn)
    except BookNotFoundError:
        response.status_code = 404
        return {"status": "Book with isbn {isbn} not found."}
    return {
        "result": {
            "isbn": book.isbn,
            "author": book.author,
            "id": book.id,
            "title": book.title,
        }
    }
