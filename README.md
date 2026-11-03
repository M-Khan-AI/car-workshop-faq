# Car Workshop FAQ Assistant

Car Workshop FAQ Assistant is a Python project that answers customer questions using only a verified JSON knowledge base of 20 workshop FAQs covering prices, hours, and repairs. It sends the FAQ and question to an AI model, returns grounded answers, and uses guardrails to give a safe fallback when unsure. Pytest verifies known and unknown questions.

## Features

- Answers customer questions using **only** the data in `data/faqs.json`
- Returns a polite fallback message when the answer is not in the FAQ
- Guardrails detect guessing (sentinel token and hedging phrases)
- Simple command-line chat interface
- Automated tests for known and unknown questions

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.9+ | Main language |
| JSON | FAQ knowledge base (single source of truth) |
| OpenAI API (or any compatible provider) | AI model that generates answers |
| python-dotenv | Loads the API key from a `.env` file |
| Pytest | Automated testing |
| Git / GitHub | Version control |

## Project Structure

```
car-workshop-faq/
├── data/
│   └── faqs.json              # 20 Q&A pairs (source of truth)
├── src/
│   ├── __init__.py
│   ├── config.py              # Model name, fallback message, API key loading
│   ├── data_loader.py         # Loads the FAQ JSON file
│   ├── prompt_builder.py      # Builds the system prompt with FAQ data
│   ├── guardrails.py          # Detects guessing and applies the fallback
│   └── answer_engine.py       # get_answer(question): calls the AI
├── tests/
│   ├── __init__.py
│   └── test_answer_engine.py  # Tests for known and unknown questions
├── .env                       # Your API key (never committed)
├── .env.example               # Template for the required variables
├── .gitignore
├── main.py                    # Command-line chat loop
├── requirements.txt
└── README.md
```

## How It Works

1. `data_loader.py` reads the 20 FAQs from `data/faqs.json`.
2. `prompt_builder.py` inserts the FAQ data into a system prompt that tells the AI to answer only from that data, and to reply `NOT_IN_FAQ` if the answer is missing.
3. `answer_engine.py` sends the prompt and the customer's question to the AI model (temperature set to 0 for consistent answers).
4. `guardrails.py` checks the reply. If it contains `NOT_IN_FAQ`, is empty, or sounds like guessing ("I think", "probably", etc.), the user receives the fallback message instead.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/car-workshop-faq.git
cd car-workshop-faq
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Copy the template and fill in your key:

```bash
copy .env.example .env      # Windows
cp .env.example .env        # macOS / Linux
```

Then edit `.env`:

```
OPENAI_API_KEY=your_key_here
```

> **Never commit `.env`.** It is already listed in `.gitignore`.

## Usage

Start the chat from the project root:

```bash
python main.py
```

Example session:

```
Car Workshop Assistant (type 'quit' to exit)
You: What time do you open?
Bot: We are open Monday to Friday from 8:00 AM to 6:00 PM, and Saturday from 9:00 AM to 2:00 PM.
You: What is the capital of France?
Bot: Sorry, I don't have that information. Please call the workshop and our team will help you.
You: quit
```

## Running Tests

```bash
pytest -v
```

The tests check that:

- Known questions (hours, warranty) return correct answers
- Unknown or off-topic questions return the fallback message
- Empty questions return the fallback message
- The guardrail detects hedging phrases and the `NOT_IN_FAQ` token

> Tests that call the AI need a valid API key and an internet connection.

## FAQ Data Format

Each entry in `data/faqs.json` has four fields:

```json
{
  "id": 1,
  "category": "hours",
  "question": "What are your opening hours?",
  "answer": "We are open Monday to Friday from 8:00 AM to 6:00 PM..."
}
```

Categories: `hours`, `booking`, `prices`, `repairs`, `policy`.

## Configuration

Settings live in `src/config.py`:

| Setting | Description |
|---|---|
| `MODEL` | AI model name (change it to match your provider) |
| `FALLBACK_MESSAGE` | Message shown when the answer is unknown |
| `NOT_FOUND_TOKEN` | Keyword the AI returns when it cannot answer |

## Future Improvements

- Web or chat user interface
- Retrieval of only the most relevant FAQs for larger datasets
- Mocked API tests that run without internet access
- Logging of unanswered questions to improve the FAQ
