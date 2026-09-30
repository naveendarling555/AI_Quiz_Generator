"""Quiz evaluation and adaptive-difficulty analytics."""

from __future__ import annotations

from typing import Dict, Any, List


def evaluate_quiz(quiz: Dict[str, Any], responses: Dict[str, Any]) -> Dict[str, Any]:
    questions = quiz.get("questions", [])
    results: List[Dict[str, Any]] = []
    correct = 0

    for question in questions:
        qid = question["id"]
        expected = str(question.get("answer", "")).strip().lower()
        actual = str(responses.get(qid, "")).strip().lower()
        is_correct = bool(actual) and actual == expected

        if is_correct:
            correct += 1

        results.append({
            "id": qid,
            "type": question.get("type"),
            "correct": is_correct,
            "expected": question.get("answer", ""),
            "actual": responses.get(qid, ""),
            "difficulty": question.get("difficulty", "medium"),
        })

    total = len(questions)
    percentage = round((correct / total) * 100, 2) if total else 0.0

    by_type = {}
    for item in results:
        qtype = item["type"]
        by_type.setdefault(qtype, {"total": 0, "correct": 0})
        by_type[qtype]["total"] += 1
        by_type[qtype]["correct"] += int(item["correct"])

    by_difficulty = {}
    for item in results:
        diff = item["difficulty"]
        by_difficulty.setdefault(diff, {"total": 0, "correct": 0})
        by_difficulty[diff]["total"] += 1
        by_difficulty[diff]["correct"] += int(item["correct"])

    if percentage >= 80:
        recommendation = "Increase difficulty for the next quiz."
    elif percentage >= 50:
        recommendation = "Keep a balanced difficulty and review incorrect concepts."
    else:
        recommendation = "Use easier questions and revise the source material."

    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "percentage": percentage,
        "by_type": by_type,
        "by_difficulty": by_difficulty,
        "recommendation": recommendation,
        "results": results,
    }
