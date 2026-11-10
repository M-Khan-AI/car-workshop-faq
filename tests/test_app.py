import pytest

import app as app_module


@pytest.fixture
def client():
	app_module.app.config["TESTING"] = True
	with app_module.app.test_client() as test_client:
		yield test_client


def test_homepage_returns_html(client):
	response = client.get("/")

	assert response.status_code == 200
	assert response.content_type.startswith("text/html")


@pytest.mark.parametrize(
	"payload",
	[
		{},
		{"question": ""},
		{"question": "   "},
	],
)
def test_ask_rejects_empty_question(client, monkeypatch, payload):
	def unexpected_answer(_question):
		pytest.fail("get_answer should not run for an empty question")

	monkeypatch.setattr(app_module, "get_answer", unexpected_answer)

	response = client.post("/ask", json=payload)

	assert response.status_code == 400
	assert response.get_json() == {"error": "Please type a question."}


def test_ask_rejects_question_over_max_length(client, monkeypatch):
	def unexpected_answer(_question):
		pytest.fail("get_answer should not run for an overlong question")

	monkeypatch.setattr(app_module, "get_answer", unexpected_answer)

	response = client.post("/ask", json={"question": "x" * 301})

	assert response.status_code == 400
	assert response.get_json() == {
		"error": "Question is too long (max 300 characters)."
	}


def test_ask_passes_trimmed_question_to_answer_engine(client, monkeypatch):
	received_questions = []

	def fake_get_answer(question):
		received_questions.append(question)
		return "We are open from 8 AM to 5 PM."

	monkeypatch.setattr(app_module, "get_answer", fake_get_answer)

	response = client.post("/ask", json={"question": "  What are your hours?  "})

	assert response.status_code == 200
	assert response.get_json() == {"answer": "We are open from 8 AM to 5 PM."}
	assert received_questions == ["What are your hours?"]


def test_ask_accepts_question_at_max_length(client, monkeypatch):
	question = "x" * 300
	monkeypatch.setattr(app_module, "get_answer", lambda received: received)

	response = client.post("/ask", json={"question": question})

	assert response.status_code == 200
	assert response.get_json() == {"answer": question}
