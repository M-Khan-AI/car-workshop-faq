# Handover Document: Car Workshop FAQ Assistant

## 1. Project Summary

The Car Workshop FAQ Assistant is a web app where customers type a question and get an instant answer about prices, opening hours, repairs, booking, and policies. It answers **only** from the workshop's own FAQ file, so it does not invent prices or policies. If the answer is not in the FAQ, it politely asks the customer to call the workshop.

| Item | Details |
|---|---|
| Live demo | https://car-workshop-faq-production.up.railway.app/ |
| Source code | https://github.com/M-Khan-AI/car-workshop-faq |
| Hosting | railway.com |
| AI provider | GROQ API |
| Delivered by | <Muhammad Khan> |
| Handover date | <11/11/2026> |

## 2. What Is Delivered

- A responsive web page that works on phones and computers
- An AI answer engine that uses only the FAQ data
- Guardrails that return a safe fallback message instead of guessing
- 20 workshop questions and answers in `data/faqs.json`
- Automated tests (Pytest) and a manual test report (`TESTING.md`)
- Deployment configuration (`Procfile`, `requirements.txt`)
- Documentation (`README.md` and this file)

## 3. How Customers Use It

1. Open the live link in any browser.
2. Type a question, or tap one of the suggested questions.
3. Read the answer shown in the chat area.

Questions outside the FAQ receive this reply: *"Sorry, I don't have that information. Please call the workshop and our team will help you."*

## 4. How to Update the Workshop Information

All answers come from one file: `data/faqs.json`. To change a price, opening hours, or a policy:

1. Open `data/faqs.json` on GitHub (or in your code editor).
2. Edit the `answer` text of the relevant entry. To add a new question, copy an existing entry and give it the next `id`:
   ```json
   {
     "id": 21,
     "category": "prices",
     "question": "How much does a tyre change cost?",
     "answer": "A tyre change costs 10 USD per tyre, excluding the tyre."
   }
   ```
3. Keep valid JSON: every entry needs `id`, `category`, `question`, and `answer`, and entries are separated by commas.
4. Commit the change to the `main` branch. Render redeploys automatically, usually within a few minutes.
5. Open the live link and ask the updated question to confirm.

> If the website does not need to change, only `faqs.json` needs editing. No code changes are required.

## 5. Accounts and Access

| Account | Used for | Notes |
|---|---|---|
| GitHub | Stores the code | Add the client as a repository collaborator or transfer ownership |
| Railway | Hosts the live app | Invite the client to the service, or have them create their own account and redeploy from the repository |
| GROQ | Provides the AI model | The client should create their own API key |

**API key:** the key is stored as the environment variable `OPENAI_API_KEY` in the Render dashboard (**Environment** tab). It is never stored in the code or on GitHub. To change it, update the value in Render and redeploy.

## 6. Known Limitations

- **Cold starts:** on the free hosting plan, the app sleeps after about 15 minutes without visitors, and the first visit afterwards can take around a minute. A paid plan removes this delay.
- **Free plan limits:** hosting and AI provider free tiers change over time. Check Railway and GRPQ for current limits and pricing.
- **Public link:** anyone with the link can ask questions, and each question uses the AI API quota. Set a usage limit in the AI provider's dashboard.
- **FAQ-only answers:** the assistant cannot answer anything outside the 20 FAQs, by design. Add more entries to widen its coverage.
- **No chat memory:** each question is answered on its own, so follow-up questions such as "and how long does that take?" may not work.
- **Single language:** the FAQ and answers are in English.

## 7. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Page takes about a minute to load | Free plan was asleep | Wait, then refresh |
| Every answer is the fallback message | Missing or invalid API key, or AI quota used up | Check `GROQ_API_KEY` in Railway and the AI provider's usage page |
| Site shows "Application failed" after an update | Invalid JSON in `faqs.json` or a failed build | Check the Railway logs and validate the JSON file |
| An updated answer does not appear | Redeploy not finished | Wait for Railway to show **Live**, then refresh |

To check the JSON is valid before committing, run:

```bash
python -m json.tool data/faqs.json
```

## 8. Running the Project Locally

```bash
git clone https://github.com/<M-Khan-AI>/car-workshop-faq.git
cd car-workshop-faq
python -m venv venv
venv\Scripts\Activate.ps1      # Windows (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

Create a `.env` file with `GROQ_API_KEY=your_key_here`, then run:

```bash
python app.py
```

Run the tests with `pytest -v`.

## 9. Suggested Future Improvements

- Chat history so follow-up questions work
- A larger FAQ with search, so only the relevant entries are sent to the AI
- A log of unanswered questions to show which FAQs to add
- A custom domain and a paid plan with no cold starts
- A booking form connected to the assistant
