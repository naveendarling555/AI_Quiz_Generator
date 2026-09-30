"""Application configuration."""

APP_TITLE = "QuizForge AI"
MAX_INPUT_CHARS = 30000
DEFAULT_QUESTION_COUNT = 10
MIN_QUESTION_COUNT = 3
MAX_QUESTION_COUNT = 20

QUESTION_TYPES = {
    "mcq": "Multiple Choice",
    "true_false": "True / False",
    "fill_blank": "Fill in the Blank",
}

DIFFICULTIES = {"easy", "medium", "hard", "mixed"}
