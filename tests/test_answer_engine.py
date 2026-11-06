
"""Tests for the Car Workshop answer engine."""

from src.answer_engine import get_answer
from src.config import FALLBACK_MESSAGE
from src.guardrails import is_guess


def test_known_question_hours():
    answer = get_answer("What time do you open?")

    assert "8" in answer


def test_known_question_warranty():
    answer = get_answer("Do you guarantee your repairs?")

    assert "warranty" in answer.lower()


def test_unknown_question_returns_fallback():
    answer = get_answer("What is the capital of France?")

    assert answer == FALLBACK_MESSAGE


def test_unknown_car_topic_returns_fallback():
    answer = get_answer("Do you sell Tesla Model 3 cars?")

    assert answer == FALLBACK_MESSAGE


def test_empty_question():
    answer = get_answer("   ")

    assert answer == FALLBACK_MESSAGE


def test_guardrail_detects_hedging():
    result = is_guess("I think it costs around 50 dollars")

    assert result is True


def test_guardrail_detects_token():
    result = is_guess("NOT_IN_FAQ")

    assert result is True
