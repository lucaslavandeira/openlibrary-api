from test.fixtures import TestClient


def test_post_comment(test_client: TestClient, book):
    response = test_client.post(
        f"/books/{book.id}/comments", json={"content": "Test content"}
    )
    assert response.status_code == 201
    body = response.json()
    comments = test_client.get(f"/books/{book.id}/comments")
    assert comments.json()[0] == body
