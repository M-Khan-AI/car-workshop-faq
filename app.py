
"""Flask web app for the Car Workshop Assistant."""

from flask import Flask, jsonify, render_template, request

from src.answer_engine import get_answer

app = Flask(__name__)

MAX_QUESTION_LENGTH = 300


@app.route("/")
def index():
    """Serve the chatbot interface."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """Receive a customer question and return an answer."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data."}), 400

    question = str(data.get("question", "")).strip()

    # Validate empty questions
    if not question:
        return jsonify({
            "error": "Please type a question."
        }), 400

    # Validate question length
    if len(question) > MAX_QUESTION_LENGTH:
        return jsonify({
            "error": f"Question is too long (max {MAX_QUESTION_LENGTH} characters)."
        }), 400

    # Generate answer using the answer engine
    answer = get_answer(question)

    return jsonify({"answer": answer}), 200


if __name__ == "__main__":
    app.run(debug=True)
