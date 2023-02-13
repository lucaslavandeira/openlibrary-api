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


def test_delete_comment(book, comments_service, comment_repository):
    comment_id = comments_service.add(book.id, "Test comment")
    comments_service.delete(comment_id)
    assert comment_repository.get(comment_id) is None


def test_delete_comment_that_does_not_exist_raises_error(comments_service):
    exception_thrown = False
    invalid_comment_id = 0
    try:
        comments_service.delete(invalid_comment_id)
    except CommentNotFoundError:
        exception_thrown = True
    assert exception_thrown


def test_list_for_book(book, comments_service):
    comment_id = comments_service.add(book.id, "Test comment")
    comments = comments_service.list_for_book(book.id)
    assert len(comments) == 1
    assert comments[0]["id"] == comment_id
    assert comments[0]["content"] == "Test comment"


def test_list_for_non_book_raises_error(comments_service):
    exception_thrown = False
    invalid_book_id = 0
    try:
        comments_service.list_for_book(invalid_book_id)
    except BookNotFoundError:
        exception_thrown = True
    assert exception_thrown


def test_book_offset(book, comments_service):
    comments_service.add(book.id, "Test comment")
    comment_id_2 = comments_service.add(book.id, "Test comment 2")
    comments = comments_service.list_for_book(book.id, offset=1)

    assert len(comments) == 1
    assert comments[0]["id"] == comment_id_2
    assert comments[0]["content"] == "Test comment 2"


def test_book_limit(book, comments_service):
    comment_id = comments_service.add(book.id, "Test comment")
    comments_service.add(book.id, "Test comment 2")
    comments = comments_service.list_for_book(book.id, limit=1)

    assert len(comments) == 1
    assert comments[0]["id"] == comment_id
    assert comments[0]["content"] == "Test comment"
