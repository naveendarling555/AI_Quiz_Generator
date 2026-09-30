# AI & NLP Quiz Generator

An educational AI/NLP project that converts learning content into:
- Multiple Choice Questions (MCQs)
- True/False questions
- Fill-in-the-Blank questions
- Answer keys
- Difficulty labels
- Automatic quiz evaluation
- Performance analytics
- JSON export
- A responsive Flask web interface

## Project goals

This project demonstrates practical skills in:
Python, NLP preprocessing, tokenization, sentence segmentation, keyword/concept extraction,
TF-IDF similarity, question generation, distractor generation, rule-based NLP,
quiz assembly, evaluation, analytics, Flask, HTML, CSS and JavaScript.

## Architecture

Input educational text
        |
        v
NLP preprocessing
        |
        +--> sentence extraction
        |
        +--> keyword/concept extraction
        |
        v
Question generation
        |
        +--> MCQ
        +--> True/False
        +--> Fill-in-the-Blank
        |
        v
Quiz assembly
        |
        +--> difficulty tagging
        +--> answer key
        +--> evaluation
        +--> analytics
        |
        v
Flask Web UI / JSON export

## Folder structure

AI_NLP_Quiz_Generator/
├── app.py
├── quiz_generator.py
├── nlp_processor.py
├── evaluator.py
├── config.py
├── setup_models.py
├── requirements.txt
├── README.md
├── LICENSE
├── data/
│   └── sample_content.txt
├── output/
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── tests/
│   └── test_quiz_generator.py
└── models/

## Installation - Windows

1. Install Python 3.10+ from python.org.
2. Open PowerShell in this project folder.
3. Create a virtual environment:

   python -m venv venv

4. Activate it:

   PowerShell:
   .\venv\Scripts\Activate.ps1

   If PowerShell blocks activation, use Command Prompt:

   venv\Scripts\activate.bat

   You can also skip activation and run:
   venv\Scripts\python.exe -m pip install -r requirements.txt

5. Install dependencies:

   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt

6. Download NLP resources:

   python setup_models.py

7. Start the application:

   python app.py

8. Open:
   http://127.0.0.1:5000

## If model download is unavailable

The application contains fallback NLP logic. It can still generate quizzes from normal English text.
Run `setup_models.py` again later when internet access is available for better NLP processing.

## Using the application

1. Enter or paste educational content.
2. Select number of questions.
3. Select difficulty.
4. Select question types.
5. Click Generate Quiz.
6. Answer the generated questions.
7. Submit to see score and analytics.
8. Export the generated quiz as JSON if required.

## Command-line test

python -m unittest discover -s tests -p "test_*.py"

## Academic workflow mapped to the 6-day plan

Day 1 - Research & Planning:
Architecture, question types, templates, environment.

Day 2 - NLP Foundation:
Cleaning, sentence splitting, tokenization, stopword removal,
keyword extraction, concept extraction and TF-IDF.

Day 3 - MCQ Generation:
Question templates, distractor generation and answer keys.

Day 4 - True/False & Fill-in-the-Blank:
Rule-based generation and difficulty tagging.

Day 5 - Quiz Assembly:
Mixed quiz creation, evaluation and JSON export.

Day 6 - Testing & Bonus:
Unit tests, analytics, adaptive difficulty, optimization and Flask UI.

## Important limitation

This is an educational rule-based NLP generator, not a large generative language model.
Its output should be reviewed by a teacher/student before high-stakes assessment use.
