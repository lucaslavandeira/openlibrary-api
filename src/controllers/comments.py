from fastapi import APIRouter, Response, Request
from src.services.comments_service import (
    BookNotFoundError,
    CommentsService,
    CommentNotFoundError,
)


from pydantic import BaseModel

router = APIRouter()


class Comment(BaseModel):
    content: str


@router.post("/")
def add_comment(book_id: int, comment: Comment, response: Response):
    if not comment:
        response.status_code = 400
        return {"error": "Content not supplied"}
    response.status_code = 201
    return CommentsService().add(book_id, comment.content)


@router.get("/")
def get_comments(book_id):
    return CommentsService().list_for_book(book_id)


@router.get("/{comment_id}")
def get(book_id: int, comment_id: int):
    return CommentsService().get(book_id, comment_id)
