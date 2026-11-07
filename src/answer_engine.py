from google import genai

from src.config import API_KEY, MODEL, FALLBACK_MESSAGE
from src.data_loader import load_faqs
from src.prompt_builder import build_system_prompt
from src.guardrails import apply_guardrail


client = genai.Client(api_key=API_KEY)

FAQS = load_faqs()
SYSTEM_PROMPT = build_system_prompt(FAQS)


def get_answer(question: str) -> str:

    if not question or not question.strip():
        return FALLBACK_MESSAGE

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=question,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0,
            },
        )

        if not response.text:
            return FALLBACK_MESSAGE

        return apply_guardrail(response.text, FAQS)

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return FALLBACK_MESSAGE