from pytest import fixture
from fastapi.testclient import TestClient

from src.app import app


@fixture
def test_client():
    yield TestClient(app)
