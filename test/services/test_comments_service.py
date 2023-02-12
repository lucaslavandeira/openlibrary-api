from pytest import fixture
from src.services.books_service import BookNotFoundError

from src.services.comments_service import CommentNotFoundError, CommentsService


@fixture
def comments_service():
    yield CommentsService()


@fixture
def comment_id(book, comments_service):
    yield comments_service.add(book.id, "Test comment")


def test_add_comment(book, comments_service, comment_repository):
    comments_service.add(book.id, "Test comment")

    assert len(comment_repository.get_all_for_book(book)) == 1


def test_add_comment_to_non_existing_book(book, comments_service):
    exception_thrown = False
    try:
        comments_service.add(0, "Test comment")
    except BookNotFoundError:
        exception_thrown = True

    assert exception_thrown


def test_add_multiple_comments(book, comments_service, comment_repository):
    comments_service.add(book.id, "Test comment")
    comments_service.add(book.id, "Test comment 2")
    comments_service.add(book.id, "Test comment 3")

    assert len(comment_repository.get_all_for_book(book)) == 3


def test_update_comment(comment_id, comments_service, comment_repository):
    comments_service.update(comment_id, "Updated comment")

    comment = comment_repository.get(comment_id)
    assert comment.content == "Updated comment"


def test_update_non_existing_comment(comments_service):
    exception_thrown = False
    try:
        comments_service.update(0, "Updated comment")
    except CommentNotFoundError:
        exception_thrown = True

    assert exception_thrown
