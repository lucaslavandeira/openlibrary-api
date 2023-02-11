from fastapi import FastAPI
from .services.books_service import BooksService


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books/{isbn}")
def get_by_isbn(isbn):
    book = BooksService().get(isbn)
    return {"result": book}
