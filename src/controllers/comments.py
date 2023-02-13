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
def get_comments(book_id, response: Response, offset: int = 0, limit: int = 10):
    try:
        return CommentsService().list_for_book(book_id, offset, limit)
    except BookNotFoundError:
        response.status_code = 404
        return {"error": "Book not found"}


@router.get("/{comment_id}")
def get(book_id: int, comment_id: int, response: Response):
    comment = CommentsService().get(book_id, comment_id)
    if comment is None:
        response.status_code = 404
        return {"error": "Comment not found"}

    return comment


@router.patch("/{comment_id}")
def edit_comment(book_id: int, comment_id: int, comment: Comment, response: Response):
    try:
        return CommentsService().update(book_id, comment_id, comment.content)
    except BookNotFoundError:
        response.status_code = 404
        return {"error": "Book not found"}
