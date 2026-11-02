import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"  # check the provider for a current free or cheap model
FALLBACK_MESSAGE = (
    "Sorry, I don't have that information. "
    "Please call the workshop and our team will help you."
)
NOT_FOUND_TOKEN = "NOT_IN_FAQ"