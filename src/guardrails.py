from src.config import FALLBACK_MESSAGE, NOT_FOUND_TOKEN

HEDGES = ["i think", "probably", "i'm not sure", "as an ai", "i guess"]

def is_guess(reply: str) -> bool:
    text = reply.strip().lower()
    if not text or NOT_FOUND_TOKEN.lower() in text:
        return True
    return any(h in text for h in HEDGES)

def apply_guardrail(reply: str) -> str:
    return FALLBACK_MESSAGE if is_guess(reply) else reply.strip()