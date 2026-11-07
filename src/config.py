import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GENAI_API_KEY")

MODEL = "gemini-3.8-flash"

FALLBACK_MESSAGE = (
    "Sorry, I don't have that information. "
    "Please call the workshop and our team will help you."
)

NOT_FOUND_TOKEN = "NOT_IN_FAQ"