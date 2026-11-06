
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "faqs.json"


def load_faqs():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"FAQ file not found: {DATA_FILE}"
        )

if __name__ == "__main__":
    faqs = load_faqs()

    print("FAQ loaded successfully")
    print("Total FAQs:", len(faqs))
    print("First FAQ:", faqs[0])