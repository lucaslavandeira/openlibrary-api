def test_answer(test_client):
    response = test_client.get("/")
    assert response.status_code == 200