import unittest

from quiz_generator import QuizGenerator
from evaluator import evaluate_quiz


TEXT = """Artificial intelligence is a field of computer science.
Machine learning is a subset of artificial intelligence that enables systems to learn from data.
Natural language processing is a branch of artificial intelligence that helps computers process human language.
Tokenization is the process of breaking text into smaller units called tokens.
TF-IDF is a statistical technique used to estimate the importance of words in documents.
"""


class QuizGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.generator = QuizGenerator(seed=7)

    def test_analysis(self):
        result = self.generator.nlp.analyze(TEXT)
        self.assertGreater(result["words"], 10)
        self.assertGreater(result["sentences"], 2)
        self.assertTrue(result["keywords"])

    def test_generation(self):
        quiz = self.generator.generate(
            TEXT,
            count=5,
            question_types=["true_false", "fill_blank"],
            difficulty="mixed",
        )
        self.assertGreaterEqual(len(quiz["questions"]), 1)
        for question in quiz["questions"]:
            self.assertIn(question["type"], {"true_false", "fill_blank"})
            self.assertIn("answer", question)
            self.assertTrue(question["id"])

    def test_evaluation(self):
        quiz = {
            "questions": [
                {"id": "q1", "type": "mcq", "answer": "Python", "difficulty": "easy"},
                {"id": "q2", "type": "fill_blank", "answer": "NLP", "difficulty": "medium"},
            ]
        }
        result = evaluate_quiz(
            quiz,
            {"q1": "Python", "q2": "wrong"},
        )
        self.assertEqual(result["correct"], 1)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["percentage"], 50.0)


if __name__ == "__main__":
    unittest.main()
