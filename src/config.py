
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY") 
MODEL = os.getenv("GROQ_MODEL") or os.getenv("MODEL", "openai/gpt-oss-120b")

FALLBACK_MESSAGE = (
    "Sorry, I don't have that information. "
    "Please call the workshop and our team will help you."
)

NOT_FOUND_TOKEN = "NOT_IN_FAQ"

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY environment variable is missing."
    )
