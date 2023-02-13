from datetime import datetime
from pytest import fixture

from src.repositories.books import Book, BookRepository
from src.repositories.comments import Comment


@fixture
def other_book(isbn, book_repository: BookRepository):
    book = Book(author="Test author 2", title="Test title 2", isbn=isbn)
    book_repository.add(book)
    yield book


def test_create_comment(book, comment_repository):
    comment = Comment(book=book.id, content="This is my test comment")
    comment_repository.add(comment)

    assert comment_repository.get_all_for_book(book)[0].id == comment.id


def test_create_many_comments(book, comment_repository):
    comments_amount = 3
    for x in range(comments_amount):
        comment = Comment(book=book.id, content=f"This is my test comment number {x}")
        comment_repository.add(comment)

    assert len(comment_repository.get_all_for_book(book)) == comments_amount


def test_create_comments_for_multiple_books(book, other_book, comment_repository):
    comment = Comment(book=book.id, content="This is my test comment")
    other_comment = Comment(book=other_book.id, content="This is my test comment")
    comment_repository.add(comment)
    comment_repository.add(other_comment)

    assert len(comment_repository.get_all_for_book(book)) == 1
    assert len(comment_repository.get_all_for_book(other_book)) == 1


def test_update_comment(book, comment_repository):
    comment = Comment(book=book.id, content="This is my test comment")
    comment_repository.add(comment)

    comment_repository.update_content(comment.id, "Updated content")

    comment = comment_repository.get(comment.id)
    assert comment.content == "Updated content"


def test_delete_comment(book, comment_repository):
    comment = Comment(book=book.id, content="This is my test comment")
    comment_repository.add(comment)
    assert len(comment_repository.get_all_for_book(book)) == 1

    count = comment_repository.delete(comment)
    assert count == 1
    assert len(comment_repository.get_all_for_book(book)) == 0


def test_attempt_delete_of_non_existing_comment_returns_0(comment_repository):
    comment = Comment(id=0)
    count = comment_repository.delete(comment)
    assert count == 0


def test_list_for_book(book, comment_repository):
    comment = Comment(book=book.id, content="This is my test comment")
    comment_repository.add(comment)
    comment_2 = Comment(book=book.id, content="This is second comment")
    comment_repository.add(comment_2)

    comments = comment_repository.list_for_book(book)
    assert len(comments) == 2
    assert comments[0].content == comment.content
    assert comments[1].content == comment_2.content


def test_list_for_book_returns_results_by_created_date(book, comment_repository):
    comment = Comment(
        book=book.id,
        content="This is my test comment",
        created_at=datetime(2020, 1, 2, 0, 0, 0),
    )
    comment_repository.add(comment)
    comment_2 = Comment(
        book=book.id,
        content="This is second comment",
        created_at=datetime(2020, 1, 1, 0, 0, 0),
    )
    comment_repository.add(comment_2)

    comments = comment_repository.list_for_book(book)
    assert comments[0].content == comment_2.content
    assert comments[1].content == comment.content
