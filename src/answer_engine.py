
from groq import Groq

from src.config import API_KEY, MODEL, FALLBACK_MESSAGE, NOT_FOUND_TOKEN
from src.data_loader import load_faqs
from src.prompt_builder import build_system_prompt


FAQS = load_faqs()
SYSTEM_PROMPT = build_system_prompt(FAQS)

client = None


def get_client():
    global client

    if client is None:
        client = Groq(api_key=API_KEY)

    return client


def get_answer(question: str) -> str:

    if not question or not question.strip():
        return FALLBACK_MESSAGE

    try:
        groq_client = get_client()

        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0,
            max_tokens=512,
        )

        selection = response.choices[0].message.content
        if not selection or selection.strip() == NOT_FOUND_TOKEN:
            return FALLBACK_MESSAGE

        try:
            selected_id = int(selection.strip())
        except ValueError:
            return FALLBACK_MESSAGE

        selected_faq = next(
            (faq for faq in FAQS if faq.get("id") == selected_id),
            None,
        )
        if selected_faq is None:
            return FALLBACK_MESSAGE

        return selected_faq["answer"]

    except Exception as e:
        print(f"Groq API Error: {e}")
        return FALLBACK_MESSAGE
