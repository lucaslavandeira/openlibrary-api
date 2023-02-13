import os
import pytest


pytestmark = pytest.mark.skipif(os.getenv("INTEGRATION_TEST") is None, reason="INTEGRATION_TEST environment variable not set")


def test_get_book(test_client, isbn):
    response = test_client.get(f"/books/{isbn}")
    assert response.status_code == 200


def test_get_book_invalid(test_client):
    invalid_isbn = 123123
    response = test_client.get(f"/books/{invalid_isbn}")
    assert response.status_code == 404


def test_post_book(test_client, book_repository, isbn):
    response = test_client.post(f"/books/{isbn}")
    assert response.status_code == 201
    body = response.json()
    book_from_database = book_repository.get(book_id=body["id"])
    assert book_from_database.isbn == body["isbn"]


def test_search(test_client, isbn):
    # API reference: https://openlibrary.org/dev/docs/api/books
    response = test_client.get(f"/books/search?bibkeys=ISBN:{isbn}")
    assert response.status_code == 200
    body = response.json()
    assert body["result"]
