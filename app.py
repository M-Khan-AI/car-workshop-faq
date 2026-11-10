"""Flask web app: a simple page where customers ask the workshop assistant."""
import os
from flask import Flask, jsonify, render_template, request

from src.answer_engine import get_answer

app = Flask(__name__)

MAX_QUESTION_LENGTH = 300


@app.route("/")
def index():
    """Serve the chat page."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """Receive a question as JSON and return the answer as JSON."""
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({"error": "Please type a question."}), 400
    if len(question) > MAX_QUESTION_LENGTH:
        return jsonify(
            {"error": f"Question is too long (max {MAX_QUESTION_LENGTH} characters)."}
        ), 400

    answer = get_answer(question)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )