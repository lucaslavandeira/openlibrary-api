from fastapi import APIRouter, Response
from src.services.books_service import BookNotFoundError, BooksService

router = APIRouter()


@router.get("/{isbn}")
def get_by_isbn(isbn: str, response: Response):
    try:
        book = BooksService().get(isbn)
    except BookNotFoundError:
        response.status_code = 404
        return {"status": "Book with isbn {isbn} not found."}
    return book.to_dict()


@router.post("/{isbn}", status_code=201)
def save_by_isbn(isbn: str, response: Response):
    try:
        book = BooksService().save(isbn)
    except BookNotFoundError:
        response.status_code = 404
        return {"status": "Book with isbn {isbn} not found."}
    return book
