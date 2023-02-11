from fastapi import FastAPI
from .services.books_service import BooksService
from .repositories.database import Session


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books/{isbn}")
def get_by_isbn(isbn):
    book = BooksService().get(isbn)
    return {"result": book}


@app.on_event("shutdown")
def shutdown_event():
    Session.close()


@app.on_event("startup")
def startup_event():
    Session.init()
