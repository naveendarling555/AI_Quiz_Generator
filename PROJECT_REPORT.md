# AI & NLP Quiz Generator - Project Report

## 1. Project title

**AI & NLP Quiz Generator**

## 2. Abstract

The AI & NLP Quiz Generator is an educational assessment application that converts
educational text into automatically generated quiz questions. The system applies
natural language processing techniques such as text cleaning, tokenization, sentence
segmentation, stop-word filtering, keyword extraction, concept extraction and
TF-IDF-based sentence importance. It then creates multiple-choice, true/false and
fill-in-the-blank questions, assigns difficulty levels, evaluates answers and presents
performance analytics.

## 3. Problem statement

Creating practice questions manually from large educational content takes time.
The project provides a lightweight automated approach that can transform source
material into an interactive practice quiz without requiring a database.

## 4. Objectives

1. Process educational text using NLP.
2. Identify important sentences and concepts.
3. Generate different question types.
4. Create plausible MCQ distractors.
5. Assign difficulty labels.
6. Assemble and evaluate quizzes.
7. Provide analytics and adaptive-difficulty feedback.
8. Provide an attractive web interface.
9. Export generated quizzes as JSON.
10. Demonstrate practical Python and NLP skills.

## 5. Technologies

- Python
- NLTK
- spaCy
- scikit-learn
- NumPy
- Pandas
- Flask
- HTML5
- CSS3
- JavaScript
- JSON

## 6. NLP pipeline

Input text -> cleaning -> sentence segmentation -> tokenization ->
stop-word filtering -> concept/keyword extraction -> important sentence selection ->
question generation -> difficulty tagging -> quiz assembly -> evaluation -> analytics.

## 7. Day-wise implementation

### Day 1 - Research & Planning
Question types, generation templates, project architecture, environment and dependencies.

### Day 2 - NLP Foundation
Text preprocessing, sentence extraction, keyword extraction, concept extraction and TF-IDF.

### Day 3 - MCQ Generation
Definition detection, answer extraction, distractor generation, option shuffling and answer keys.

### Day 4 - True/False & Fill-in-the-Blank
Statement generation, controlled negation, blank generation and difficulty tagging.

### Day 5 - Quiz Assembly
Question IDs, mixed question types, evaluation, scoring and JSON export.

### Day 6 - Testing & Bonus Features
Unit tests, analytics, adaptive difficulty recommendation, fallback NLP and responsive Flask UI.

## 8. Model/algorithm details

### NLTK
Used for tokenization, stop-word filtering and lemmatization support.

### spaCy
The optional `en_core_web_sm` model provides sentence boundaries, named entities and
noun phrases. If it is not available, the application automatically falls back to
NLTK/regular-expression processing.

### TF-IDF
TF-IDF is used to estimate sentence importance relative to the other sentences in
the source material. This helps select useful content for question generation.

### Rule-based question generation
The generator recognizes simple educational patterns such as:
"X is Y", "X are Y", "X means Y", "X refers to Y", and "X: Y".
These patterns are used to produce definition-style MCQs.

### Distractor generation
Other extracted concepts are selected as candidate incorrect options. The engine
prefers candidates with similar phrase lengths to make options more plausible.

### Adaptive difficulty
After evaluation:
- >= 80%: recommend increasing difficulty.
- 50-79%: recommend balanced difficulty and review.
- < 50%: recommend easier questions and revision.

## 9. No database design

The project intentionally does not use MySQL, MongoDB or another database.
Data is held in Python dictionaries/lists during runtime, source content is plain text,
and generated quizzes can be exported to JSON.

## 10. Testing

Run:

python -m unittest discover -s tests -p "test_*.py"

Tests cover:
- NLP analysis
- quiz generation
- answer evaluation
- score calculation

## 11. Limitations

Automated educational question generation can create imperfect questions when source
text is vague, grammatical, highly technical or lacks explicit definitions.
Generated questions should therefore be reviewed before formal examination use.
This project is a practical NLP demonstration rather than a replacement for a
large language model or expert question writer.

## 12. Future scope

- Transformer-based question generation using T5/BART.
- Semantic similarity using sentence-transformers.
- Better distractors using embeddings.
- Multilingual question generation.
- Teacher dashboard.
- Student login and history.
- PDF/DOCX import.
- Voice-based quiz.
- Larger adaptive learning engine.
- Cloud deployment.
