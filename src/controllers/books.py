from typing import Union
from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel
from src.services.books_service import BookNotFoundError, BooksService

router = APIRouter()


class Book(BaseModel):
    author: str
    title: str
    isbn: str
    id: Union[None, int]


@router.get("/search")
def search(request: Request):
    query_params = request.query_params
    try:
        search_results = BooksService().search(query_params)
    except Exception:
        raise HTTPException(
            status_code=503, detail="API Error. Try again at a later date."
        )

    return search_results


@router.get("/{isbn}", response_model=Book)
def get_by_isbn(isbn: str):
    try:
        book = BooksService().get(isbn)
    except BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict()


@router.post("/{isbn}", status_code=201, response_model=Book)
def save_by_isbn(isbn: str):
    try:
        book = BooksService().save(isbn)
    except BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
