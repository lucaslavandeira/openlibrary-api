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
