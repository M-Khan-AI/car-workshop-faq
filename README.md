# Car Workshop FAQ Assistant

Car Workshop FAQ Assistant is a Python web app that answers customer questions using only a verified JSON knowledge base of 20 workshop FAQs covering prices, hours, and repairs. It sends the FAQ and the question to an AI model, returns grounded answers, and uses guardrails to give a safe fallback when the answer is not in the data.

**Live demo:** https://car-workshop-faq-production.up.railway.app/

> The demo runs on a free host that sleeps after 15 minutes without visitors. The first visit can take about a minute to wake up.

## What It Does

- Customers type a question on a clean page that works on phones and computers.
- The app answers **only** from `data/faqs.json`, so it never invents prices or policies.
- If the answer is not in the FAQ, it replies with a polite fallback asking the customer to call the workshop.
- Guardrails detect guessing (a `NOT_IN_FAQ` token and hedging phrases like "I think" or "probably").

## How It Works

```
Browser -> /ask (Flask) -> get_answer() -> AI model -> guardrails -> answer -> Browser
```

1. `data_loader.py` reads the 20 FAQs from `data/faqs.json`.
2. `prompt_builder.py` puts the FAQ data into a system prompt that restricts the AI to that data.
3. `answer_engine.py` sends the prompt and question to the AI model (temperature 0 for consistent answers).
4. `guardrails.py` checks the reply and swaps in the fallback message if it looks like a guess.
5. `app.py` serves the page and the `/ask` route, and `script.js` shows the answer without reloading.

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
├── Procfile 
├── requirements.txt
├── .env.example
├── .gitignore
├── HANDOVER.md
└── README.md
```

## Technologies

| Technology | Purpose |
|---|---|
| Python 3.9+ | Main language |
| JSON | FAQ knowledge base (single source of truth) |
| GROQ API | AI model that generates answers |
| Flask | Web server and `/ask` route |
| HTML, CSS, JavaScript | Responsive user interface |
| python-dotenv | Loads the API key from `.env` |
| Pytest | Automated tests |
| Gunicorn | Production server used when deployed |
| Railway | Free hosting |
| Git / GitHub | Version control |

## Setup (Run Locally)

```bash
git clone https://github.com/<M-Khan-AI>/car-workshop-faq.git
cd car-workshop-faq
python -m venv venv
venv\Scripts\Activate.ps1      # Windows (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

Create a `.env` file in the project root (copy `.env.example`) and add your key:

```
GROQ_API_KEY=your_key_here
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

## Testing

**Automated tests:**

```bash
pytest -v
```

`test_app.py` mocks the AI and runs offline. `test_answer_engine.py` calls the real AI, so it needs a valid API key and internet.

| # | Question | Type | Expected result |
|---|---|---|---|
| 1 | What are your opening hours? | Known | Gives the opening times |
| 2 | How much does an oil change cost? | Known | Gives the price range from the FAQ |
| 3 | Do you offer a warranty on repairs? | Known | Gives the warranty terms |
| 4 | What is the capital of France? | Unknown | Fallback message |
| 5 | Do you sell Tesla Model 3 cars? | Unknown | Fallback message |

## Deployment (Render)

1. Push the code to GitHub (the `main` branch).
2. On [railway.com](https://railway.com), choose **New > Web Service** and connect the repository.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app` (the same command is in `Procfile`).
5. Choose the **Free** instance type.
6. Under **Environment**, add `GROQ_API_KEY` with your key.
7. Click **Create Web Service** and open the generated link.

## Updating the FAQ

Edit `data/faqs.json` and keep each entry in this format, then redeploy:

```json
{
  "id": 1,
  "category": "hours",
  "question": "What are your opening hours?",
  "answer": "We are open Monday to Friday from 8:00 AM to 6:00 PM..."
}
```
MIT License

Copyright (c) 2026 Muhammad Khan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
