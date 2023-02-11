def test_get_book(test_client, isbn):
    response = test_client.get(f"/books/{isbn}")
    assert response.status_code == 200


def test_get_book_invalid(test_client):
    invalid_isbn = 123123
    response = test_client.get(f"/books/{invalid_isbn}")
    assert response.status_code == 404
