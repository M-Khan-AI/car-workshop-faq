from src.answer_engine import get_answer
from src.config import FALLBACK_MESSAGE
from src.guardrails import is_guess

def test_known_question_hours():
    assert "8" in get_answer("What time do you open?")

def test_known_question_warranty():
    assert "warranty" in get_answer("Do you guarantee your repairs?").lower()

def test_unknown_question_returns_fallback():
    assert get_answer("What is the capital of France?") == FALLBACK_MESSAGE

def test_unknown_car_topic_returns_fallback():
    assert get_answer("Do you sell Tesla Model 3 cars?") == FALLBACK_MESSAGE

def test_empty_question():
    assert get_answer("   ") == FALLBACK_MESSAGE

def test_guardrail_detects_hedging():
    assert is_guess("I think it costs around 50 dollars") is True

def test_guardrail_detects_token():
    assert is_guess("NOT_IN_FAQ") is True