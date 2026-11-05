from types import SimpleNamespace

import pytest

from src import answer_engine
from src.config import FALLBACK_MESSAGE
from src.guardrails import is_guess, apply_guardrail


def fake_response(text):
    """Create a simulated Gemini response."""
    return SimpleNamespace(text=text)


def test_known_question_hours(monkeypatch):
    expected_answer = answer_engine.FAQS[0]["answer"]

    def mock_generate_content(**kwargs):
        return fake_response(expected_answer)

    monkeypatch.setattr(
        answer_engine.client.models,
        "generate_content",
        mock_generate_content,
    )

    result = answer_engine.get_answer("What time do you open?")

    assert result == expected_answer


def test_unknown_question_returns_fallback(monkeypatch):

    def mock_generate_content(**kwargs):
        return fake_response("NOT_IN_FAQ")

    monkeypatch.setattr(
        answer_engine.client.models,
        "generate_content",
        mock_generate_content,
    )

    result = answer_engine.get_answer("What is the capital of France?")

    assert result == FALLBACK_MESSAGE


def test_unsupported_answer_returns_fallback(monkeypatch):

    def mock_generate_content(**kwargs):
        return fake_response("We provide free Ferrari repairs.")

    monkeypatch.setattr(
        answer_engine.client.models,
        "generate_content",
        mock_generate_content,
    )

    result = answer_engine.get_answer("Do you repair Ferrari cars?")

    assert result == FALLBACK_MESSAGE


def test_empty_question():
    assert answer_engine.get_answer("   ") == FALLBACK_MESSAGE


def test_api_timeout_returns_fallback(monkeypatch):

    def mock_generate_content(**kwargs):
        raise TimeoutError("Gemini API request timed out")

    monkeypatch.setattr(
        answer_engine.client.models,
        "generate_content",
        mock_generate_content,
    )

    result = answer_engine.get_answer("What are your opening hours?")

    assert result == FALLBACK_MESSAGE


def test_guardrail_detects_hedging():
    assert is_guess("I think it costs around 50 dollars") is True


def test_guardrail_detects_token():
    assert is_guess("NOT_IN_FAQ") is True


def test_guardrail_rejects_unknown_answer():
    result = apply_guardrail(
        "We provide free Ferrari repairs.",
        answer_engine.FAQS,
    )

    assert result == FALLBACK_MESSAGE