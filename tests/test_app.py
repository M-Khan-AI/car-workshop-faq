import os

# Dummy key so importing the app works without a real .env file.
os.environ.setdefault("OPENAI_API_KEY", "test-key")

import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Car Workshop Assistant" in response.data


def test_ask_returns_answer(client, monkeypatch):
    monkeypatch.setattr(app_module, "get_answer", lambda q: "We open at 8 AM.")
    response = client.post("/ask", json={"question": "When do you open?"})
    assert response.status_code == 200
    assert response.get_json()["answer"] == "We open at 8 AM."


def test_ask_empty_question_returns_400(client):
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_ask_missing_body_returns_400(client):
    response = client.post("/ask", data="not json")
    assert response.status_code == 400


def test_ask_too_long_question_returns_400(client):
    response = client.post("/ask", json={"question": "a" * 301})
    assert response.status_code == 400