# Car Workshop FAQ Assistant

Car Workshop FAQ Assistant is a Python project that answers customer questions using only a verified JSON knowledge base of 20 workshop FAQs covering prices, hours, and repairs. It sends the FAQ and question to an AI model, returns grounded answers, and uses guardrails to give a safe fallback when unsure. A responsive web page lets customers ask questions.

## What Has Been Done

- **Task 1 – FAQ data and setup:** Created 20 realistic car workshop question-and-answer pairs in `data/faqs.json` (prices, hours, repairs, booking, policies) and set up the Python project on GitHub.
- **Task 2 – AI answer engine:** Built `get_answer()` in `src/answer_engine.py`. The prompt includes the FAQ data and restricts the AI to it, guardrails detect guessing and return a fallback message, and Pytest tests cover known and unknown questions.
- **Task 3 – Web page:** Built a clean, mobile-friendly page with Flask, HTML, CSS, and JavaScript where a user types a question and sees the answer from `get_answer()`. Route tests are in `tests/test_app.py`.

## Technologies

Python, Flask, HTML, CSS, JavaScript, python-dotenv, Pytest

## Dependencies
google-genai
python-dotenv
pytest
flask

## Project Structure

```
car-workshop-faq/
├── data/faqs.json
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── prompt_builder.py
│   ├── guardrails.py
│   └── answer_engine.py
├── templates/index.html
├── static/
│   ├── style.css
│   └── script.js
├── tests/
│   ├── __init__.py
│   ├── test_answer_engine.py
│   └── test_app.py
├── app.py
├── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/<your-username>/car-workshop-faq.git
cd car-workshop-faq
python -m venv venv
venv\Scripts\Activate.ps1      # Windows (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

Create a `.env` file in the project root (copy `.env.example`) and add your key:

```
GEMINI_API_KEY=your_key_here
```

Never commit `.env`.

## Run

Web app:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Command-line chat:

```bash
python main.py
```

## Test

```bash
pytest -v
```