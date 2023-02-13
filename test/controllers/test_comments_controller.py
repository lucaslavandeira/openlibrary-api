from test.fixtures import TestClient


def test_post_comment(test_client: TestClient, book):
    response = test_client.post(
        f"/books/{book.id}/comments", json={"content": "Test content"}
    )
    assert response.status_code == 201
    body = response.json()
    comments = test_client.get(f"/books/{book.id}/comments")
    assert comments.json()[0] == body


def test_get_comment(test_client, book, comment_id):
    response = test_client.get(f"/books/{book.id}/comments/{comment_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == comment_id


def test_get_non_existing_comment(test_client, book):
    invalid_comment_id = 0
    response = test_client.get(f"/books/{book.id}/comments/{invalid_comment_id}")
    assert response.status_code == 404


def test_list_comments_limit(test_client, book):
    first_comment = test_client.post(
        f"/books/{book.id}/comments", json={"content": "Test content 1"}
    ).json()
    test_client.post(
        f"/books/{book.id}/comments", json={"content": "Test content 2"}
    )

    comments = test_client.get(f"/books/{book.id}/comments?limit=1").json()
    assert len(comments) == 1
    assert comments[0] == first_comment


def test_list_comments_offset(test_client, book):
    test_client.post(
        f"/books/{book.id}/comments", json={"content": "Test content 1"}
    )
    second_comment = test_client.post(
        f"/books/{book.id}/comments", json={"content": "Test content 2"}
    ).json()

    comments = test_client.get(f"/books/{book.id}/comments?offset=1").json()
    assert len(comments) == 1
    assert comments[0] == second_comment


def test_list_comments_for_non_existing_book(test_client):
    invalid_book_id = 0
    comments = test_client.get(f"/books/{invalid_book_id}/comments")
    assert comments.status_code == 404


def test_list_comments_of_book_with_no_comments(test_client, book):
    comments = test_client.get(f"/books/{book.id}/comments?offset=1").json()
    assert len(comments) == 0
