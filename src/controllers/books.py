from fastapi import APIRouter, Response, Request
from src.services.books_service import BookNotFoundError, BooksService

router = APIRouter()


@router.get("/search")
def search(request: Request, response: Response):
    query_params = request.query_params
    try:
        search_results = BooksService().search(query_params)
    except Exception:
        response.status_code = 503
        return {"status": "API Error. Try again at a later date"}

    return search_results


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
