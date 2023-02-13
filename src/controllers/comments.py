from fastapi import APIRouter, HTTPException, Query
from src import config
from src.services.comments_service import (
    BookNotFoundError,
    CommentsService,
    CommentNotFoundError,
)


from pydantic import BaseModel

router = APIRouter()


class Comment(BaseModel):
    content: str


class CommentResponse(BaseModel):
    book: int
    id: int
    content: str
    created_at: str


@router.post("/", status_code=201, response_model=CommentResponse)
def add_comment(book_id: int, comment: Comment):
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return CommentsService().add(book_id, comment.content)


@router.get("/")
def get_comments(
    book_id, offset: int = Query(default=0, ge=0), limit: int = Query(default=config.PAGINATION_DEFAULT_LIMIT, ge=0, le=10)
):
    try:
        return CommentsService().list_for_book(book_id, offset, limit)
    except BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(book_id: int, comment_id: int):
    comment = CommentsService().get(book_id, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment.to_dict()


@router.patch("/{comment_id}")
def edit_comment(book_id: int, comment_id: int, comment: Comment):
    try:
        return CommentsService().update(book_id, comment_id, comment.content)
    except BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")


@router.delete("/{comment_id}", status_code=204)
def delete_comment(book_id: int, comment_id: int):
    try:
        return CommentsService().delete(book_id, comment_id)
    except BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")
