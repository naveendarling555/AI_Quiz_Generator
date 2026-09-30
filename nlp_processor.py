"""NLP preprocessing and concept extraction.

The processor uses NLTK and spaCy where available. It intentionally includes
fallback methods so the educational application remains runnable offline.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import List, Dict, Any

try:
    import nltk
except Exception:
    nltk = None

try:
    import spacy
except Exception:
    spacy = None

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
except Exception:
    TfidfVectorizer = None


class NLPProcessor:
    def __init__(self) -> None:
        self.nlp = None
        self.stop_words = set()
        self.lemmatizer = None
        self._load_resources()

    def _load_resources(self) -> None:
        if nltk:
            try:
                from nltk.corpus import stopwords
                self.stop_words = set(stopwords.words("english"))
            except Exception:
                self.stop_words = {
                    "the", "a", "an", "is", "are", "was", "were", "of",
                    "to", "in", "on", "for", "and", "or", "with", "by",
                    "as", "at", "from", "that", "this", "it", "be", "can"
                }
            try:
                from nltk.stem import WordNetLemmatizer
                self.lemmatizer = WordNetLemmatizer()
            except Exception:
                self.lemmatizer = None

        if spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except Exception:
                self.nlp = None

    @staticmethod
    def clean_text(text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def sentences(self, text: str) -> List[str]:
        text = self.clean_text(text)
        if not text:
            return []

        if self.nlp:
            return [s.text.strip() for s in self.nlp(text).sents if s.text.strip()]

        if nltk:
            try:
                from nltk.tokenize import sent_tokenize
                return [s.strip() for s in sent_tokenize(text) if s.strip()]
            except Exception:
                pass

        return [
            s.strip() for s in re.split(r"(?<=[.!?])\s+", text)
            if s.strip()
        ]

    def tokens(self, text: str) -> List[str]:
        if self.nlp:
            return [
                token.text.lower() for token in self.nlp(text)
                if token.is_alpha
            ]

        if nltk:
            try:
                from nltk.tokenize import word_tokenize
                return [
                    t.lower() for t in word_tokenize(text)
                    if t.isalpha()
                ]
            except Exception:
                pass

        return re.findall(r"[A-Za-z]+", text.lower())

    def keywords(self, text: str, limit: int = 20) -> List[str]:
        tokens = self.tokens(text)
        useful = [
            t for t in tokens
            if len(t) >= 3 and t not in self.stop_words
        ]
        counts = Counter(useful)
        return [word for word, _ in counts.most_common(limit)]

    def concepts(self, text: str, limit: int = 20) -> List[Dict[str, Any]]:
        concepts: List[Dict[str, Any]] = []

        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.text.strip() and ent.label_ not in {"CARDINAL", "DATE"}:
                    concepts.append({
                        "text": ent.text.strip(),
                        "label": ent.label_,
                        "source": "entity"
                    })

            for chunk in doc.noun_chunks:
                phrase = chunk.text.strip()
                if len(phrase.split()) <= 5 and len(phrase) >= 3:
                    concepts.append({
                        "text": phrase,
                        "label": "NOUN_PHRASE",
                        "source": "noun_chunk"
                    })

        seen = set()
        result = []
        for item in concepts:
            key = item["text"].lower()
            if key not in seen:
                seen.add(key)
                result.append(item)

        for keyword in self.keywords(text, limit):
            if keyword.lower() not in seen:
                result.append({
                    "text": keyword,
                    "label": "KEYWORD",
                    "source": "frequency"
                })
                seen.add(keyword.lower())

        return result[:limit]

    def important_sentences(self, text: str, limit: int = 10) -> List[str]:
        sents = self.sentences(text)
        if not sents:
            return []

        # Prefer sentences containing more useful non-stopword tokens.
        scored = []
        for sentence in sents:
            words = self.tokens(sentence)
            useful = [w for w in words if w not in self.stop_words]
            score = len(useful) + min(len(sentence) / 100.0, 2.0)
            scored.append((score, sentence))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [s for _, s in scored[:limit]]

    def tfidf_similarity(self, sentences: List[str]) -> List[float]:
        if not sentences:
            return []
        if TfidfVectorizer is None or len(sentences) == 1:
            return [1.0] * len(sentences)

        try:
            matrix = TfidfVectorizer(stop_words="english").fit_transform(sentences)
            centroid = matrix.mean(axis=0)
            scores = []
            for row in matrix:
                numerator = float(row.multiply(centroid).sum())
                denom = (float((row.multiply(row)).sum()) ** 0.5 *
                         float((centroid.multiply(centroid)).sum()) ** 0.5)
                scores.append(numerator / denom if denom else 0.0)
            return scores
        except Exception:
            return [1.0] * len(sentences)

    def analyze(self, text: str) -> Dict[str, Any]:
        cleaned = self.clean_text(text)
        sentences = self.sentences(cleaned)
        return {
            "characters": len(cleaned),
            "words": len(self.tokens(cleaned)),
            "sentences": len(sentences),
            "keywords": self.keywords(cleaned),
            "concepts": self.concepts(cleaned),
            "important_sentences": self.important_sentences(cleaned),
            "spacy_model_loaded": self.nlp is not None,
        }
