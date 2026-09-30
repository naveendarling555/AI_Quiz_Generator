"""Flask web application for QuizForge AI."""

from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from config import (
    APP_TITLE, MAX_INPUT_CHARS, DEFAULT_QUESTION_COUNT,
    MIN_QUESTION_COUNT, MAX_QUESTION_COUNT,
)
from evaluator import evaluate_quiz
from quiz_generator import QuizGenerator

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

generator = QuizGenerator()


def safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@app.route("/")
def index():
    return render_template("index.html", title=APP_TITLE)


@app.post("/api/generate")
def api_generate():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()

    if not text:
        return jsonify({"error": "Please enter educational content."}), 400

    if len(text) > MAX_INPUT_CHARS:
        return jsonify({"error": f"Content is too long. Maximum is {MAX_INPUT_CHARS} characters."}), 400

    count = max(
        MIN_QUESTION_COUNT,
        min(MAX_QUESTION_COUNT, safe_int(data.get("count"), DEFAULT_QUESTION_COUNT))
    )

    types = data.get("types", ["mcq", "true_false", "fill_blank"])
    if not isinstance(types, list):
        types = ["mcq", "true_false", "fill_blank"]

    difficulty = str(data.get("difficulty", "mixed")).lower()
    if difficulty not in {"easy", "medium", "hard", "mixed"}:
        difficulty = "mixed"

    quiz = generator.generate(text, count=count, question_types=types, difficulty=difficulty)
    if not quiz["questions"]:
        return jsonify({
            "error": "Not enough usable educational sentences were found. Add clearer explanatory content with definitions or factual statements."
        }), 422

    return jsonify(quiz)


@app.post("/api/evaluate")
def api_evaluate():
    data = request.get_json(silent=True) or {}
    quiz = data.get("quiz")
    responses = data.get("responses", {})

    if not isinstance(quiz, dict) or not isinstance(responses, dict):
        return jsonify({"error": "Invalid quiz submission."}), 400

    result = evaluate_quiz(quiz, responses)
    return jsonify(result)


@app.post("/api/export")
def api_export():
    data = request.get_json(silent=True) or {}
    quiz = data.get("quiz")
    if not isinstance(quiz, dict):
        return jsonify({"error": "No quiz supplied."}), 400

    output = OUTPUT_DIR / "generated_quiz.json"
    output.write_text(json.dumps(quiz, indent=2, ensure_ascii=False), encoding="utf-8")
    return send_file(output, as_attachment=True, download_name="generated_quiz.json")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": APP_TITLE})


if __name__ == "__main__":
    print(f"{APP_TITLE} running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
