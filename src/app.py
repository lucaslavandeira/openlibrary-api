from fastapi import FastAPI
from .controllers import books, comments

app = FastAPI()
app.include_router(books.router, prefix="/books")
app.include_router(comments.router, prefix="/books/{book_id}/comments")
