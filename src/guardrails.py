import re

from src.config import FALLBACK_MESSAGE, NOT_FOUND_TOKEN


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split())

def apply_guardrail(reply: str, faqs: list[dict]) -> str:
    """Allow only answers that exist in the FAQ dataset."""

    if not reply or NOT_FOUND_TOKEN.lower() in reply.lower():
        return FALLBACK_MESSAGE

    known_answers = {
        normalize_text(faq["answer"])
        for faq in faqs
        if faq.get("answer")
    }

    if normalize_text(reply) not in known_answers:
        return FALLBACK_MESSAGE

    return reply.strip()

def is_guess(reply: str) -> bool:
    """Check if the reply is a guess or fallback."""
    if not reply:
        return True
        
    reply_lower = reply.lower()
    
    if NOT_FOUND_TOKEN.lower() in reply_lower:
        return True
        
    # Catch hedging words/guesses tested in the test suite[cite: 8]
    hedging_words = ["i think", "maybe", "guess", "not sure", "possibly", "probably"]
    if any(word in reply_lower for word in hedging_words):
        return True
        
    return False