"""Load the car workshop FAQ data and print one random entry."""

import json
import random
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "faqs.json"


def load_faqs(path: Path = DATA_FILE) -> list[dict]:
    """Read the FAQ JSON file and return a list of Q&A dictionaries."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"Error: data file not found at {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Error: invalid JSON in {path}: {e}")


def main() -> None:
    faqs = load_faqs()
    entry = random.choice(faqs)
    print(f"[{entry['category'].upper()}]")
    print(f"Q: {entry['question']}")
    print(f"A: {entry['answer']}")


if __name__ == "__main__":
    main()