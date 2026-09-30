"""Download NLP resources used by the project.

Run:
    python setup_models.py

The application has fallbacks, so failure to download a resource does not
prevent the basic application from running.
"""

import nltk

def download_nltk():
    resources = [
        ("punkt", "tokenizers/punkt"),
        ("punkt_tab", "tokenizers/punkt_tab"),
        ("stopwords", "corpora/stopwords"),
        ("wordnet", "corpora/wordnet"),
        ("omw-1.4", "corpora/omw-1.4"),
    ]
    for name, path in resources:
        try:
            nltk.data.find(path)
            print(f"[OK] NLTK resource already available: {name}")
        except LookupError:
            print(f"[DOWNLOAD] {name}")
            try:
                nltk.download(name, quiet=False)
            except Exception as exc:
                print(f"[WARNING] Could not download {name}: {exc}")

def download_spacy():
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("[OK] spaCy model en_core_web_sm is available.")
        except Exception:
            print("[DOWNLOAD] spaCy model en_core_web_sm")
            try:
                from spacy.cli import download
                download("en_core_web_sm")
            except Exception as exc:
                print(f"[WARNING] spaCy model unavailable: {exc}")
                print("The project will use its built-in fallback NLP logic.")
    except ImportError:
        print("[WARNING] spaCy is not installed yet.")

if __name__ == "__main__":
    print("Setting up NLP resources...")
    download_nltk()
    download_spacy()
    print("Model/resource setup finished.")
