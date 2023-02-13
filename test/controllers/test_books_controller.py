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
