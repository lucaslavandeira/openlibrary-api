from fastapi import FastAPI
from .controllers import books

app = FastAPI()
app.include_router(books.router, prefix="/books")
