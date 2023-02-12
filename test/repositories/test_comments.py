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

    comment_repository.delete(comment)
    assert len(comment_repository.get_all_for_book(book)) == 0
