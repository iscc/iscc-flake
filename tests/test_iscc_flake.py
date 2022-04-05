from iscc_flake import __version__
from fastapi.testclient import TestClient
from iscc_flake.main import app

client = TestClient(app)


def test_version():
    assert __version__ == "0.2.0"


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flake-ID Generator" in response.content


def test_post_root():
    response = client.post("/")
    assert response.status_code == 201
    assert "iscc" in response.json()


def test_get_flake():
    response = client.get("/flake")
    assert response.status_code == 200
    assert "iscc" in response.json()


def test_get_try_it():
    response = client.get("/try-it")
    assert response.status_code == 200
    assert b"Flake-ID Generator" in response.content
