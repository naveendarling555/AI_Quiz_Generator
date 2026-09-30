"""Question generation engine for the AI & NLP Quiz Generator."""

from __future__ import annotations

import random
import re
from typing import List, Dict, Any, Optional, Tuple

from nlp_processor import NLPProcessor


class QuizGenerator:
    def __init__(self, seed: Optional[int] = None) -> None:
        self.rng = random.Random(seed)
        self.nlp = NLPProcessor()

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _clean_phrase(text: str) -> str:
        return text.strip(" \t\n.,;:!?()[]{}\"'")

    def _difficulty(self, sentence: str, requested: str) -> str:
        if requested in {"easy", "medium", "hard"}:
            return requested
        words = self.nlp.tokens(sentence)
        if len(words) <= 12:
            return "easy"
        if len(words) <= 24:
            return "medium"
        return "hard"

    def _extract_definition(self, sentence: str) -> Optional[Tuple[str, str]]:
        patterns = [
            r"^(.+?)\s+(?:is|are|means|refers to|is defined as)\s+(.+)$",
            r"^(.+?)\s*:\s*(.+)$",
        ]
        for pattern in patterns:
            match = re.match(pattern, sentence, flags=re.I)
            if match:
                term = self._clean_phrase(match.group(1))
                definition = self._clean_phrase(match.group(2))
                if 1 <= len(term.split()) <= 8 and len(definition) >= 8:
                    return term, definition
        return None

    def _candidate_concepts(self, sentence: str) -> List[str]:
        items = self.nlp.concepts(sentence, limit=15)
        candidates = []
        for item in items:
            phrase = self._clean_phrase(item["text"])
            if 1 <= len(phrase.split()) <= 5 and len(phrase) >= 3:
                if phrase.lower() not in {x.lower() for x in candidates}:
                    candidates.append(phrase)
        return candidates

    def _distractors(self, answer: str, all_concepts: List[str], count: int = 3) -> List[str]:
        candidates = []
        answer_lower = answer.lower()
        for item in all_concepts:
            if item.lower() == answer_lower:
                continue
            if item.lower() in {x.lower() for x in candidates}:
                continue
            candidates.append(item)

        # Same-length-ish terms are more plausible distractors.
        candidates.sort(key=lambda x: abs(len(x.split()) - len(answer.split())))
        return candidates[:count]

    def generate_mcq(self, sentence: str, all_concepts: List[str], difficulty: str) -> Optional[Dict[str, Any]]:
        definition = self._extract_definition(sentence)
        if not definition:
            return None

        answer, definition_text = definition
        distractors = self._distractors(answer, all_concepts)
        if len(distractors) < 3:
            return None

        options = [answer] + distractors[:3]
        self.rng.shuffle(options)
        correct_index = options.index(answer)

        return {
            "id": "",
            "type": "mcq",
            "question": f"Which term best matches this description?\n\n{definition_text}",
            "options": options,
            "answer": answer,
            "answer_index": correct_index,
            "difficulty": self._difficulty(sentence, difficulty),
            "source": sentence,
        }

    def generate_true_false(self, sentence: str, difficulty: str) -> Dict[str, Any]:
        original = sentence.rstrip(".!?")
        is_true = self.rng.choice([True, False])

        if is_true:
            statement = original + "."
            answer = True
        else:
            words = original.split()
            if len(words) >= 5:
                # Make one controlled semantic change using a safe negation.
                if re.search(r"\bis\b", original, re.I):
                    statement = re.sub(r"\bis\b", "is not", original, count=1, flags=re.I) + "."
                elif re.search(r"\bare\b", original, re.I):
                    statement = re.sub(r"\bare\b", "are not", original, count=1, flags=re.I) + "."
                else:
                    statement = "It is false that " + original + "."
                answer = False
            else:
                statement = "It is false that " + original + "."
                answer = False

        return {
            "id": "",
            "type": "true_false",
            "question": f"True or False: {statement}",
            "options": ["True", "False"],
            "answer": "True" if answer else "False",
            "answer_index": 0 if answer else 1,
            "difficulty": self._difficulty(sentence, difficulty),
            "source": sentence,
        }

    def generate_fill_blank(self, sentence: str, difficulty: str) -> Optional[Dict[str, Any]]:
        concepts = self._candidate_concepts(sentence)
        if not concepts:
            words = [
                w for w in self.nlp.tokens(sentence)
                if w not in self.nlp.stop_words and len(w) > 4
            ]
            concepts = words[:5]

        if not concepts:
            return None

        answer = max(concepts, key=len)
        pattern = re.compile(re.escape(answer), flags=re.I)
        if not pattern.search(sentence):
            return None

        question = pattern.sub("__________", sentence, count=1)
        return {
            "id": "",
            "type": "fill_blank",
            "question": question,
            "options": [],
            "answer": answer,
            "answer_index": 0,
            "difficulty": self._difficulty(sentence, difficulty),
            "source": sentence,
        }

    def generate(
        self,
        text: str,
        count: int = 10,
        question_types: Optional[List[str]] = None,
        difficulty: str = "mixed",
    ) -> Dict[str, Any]:
        question_types = question_types or ["mcq", "true_false", "fill_blank"]
        question_types = [t for t in question_types if t in {"mcq", "true_false", "fill_blank"}]
        if not question_types:
            question_types = ["mcq", "true_false", "fill_blank"]

        sentences = self.nlp.important_sentences(text, limit=max(count * 3, 15))
        all_concepts = [x["text"] for x in self.nlp.concepts(text, limit=50)]

        generated = []
        seen = set()

        for sentence in sentences:
            if len(generated) >= count:
                break

            for qtype in question_types:
                if len(generated) >= count:
                    break

                if qtype == "mcq":
                    question = self.generate_mcq(sentence, all_concepts, difficulty)
                elif qtype == "true_false":
                    question = self.generate_true_false(sentence, difficulty)
                else:
                    question = self.generate_fill_blank(sentence, difficulty)

                if not question:
                    continue

                fingerprint = re.sub(r"\W+", "", question["question"].lower())
                if fingerprint in seen:
                    continue

                seen.add(fingerprint)
                question["id"] = f"q{len(generated) + 1}"
                generated.append(question)

        # Ensure requested count where possible by cycling through sentence/type combinations.
        if len(generated) < count:
            for sentence in sentences:
                for qtype in question_types:
                    if len(generated) >= count:
                        break
                    if qtype == "true_false":
                        q = self.generate_true_false(sentence, difficulty)
                    elif qtype == "fill_blank":
                        q = self.generate_fill_blank(sentence, difficulty)
                    else:
                        q = self.generate_mcq(sentence, all_concepts, difficulty)
                    if not q:
                        continue
                    fingerprint = re.sub(r"\W+", "", q["question"].lower())
                    if fingerprint in seen:
                        continue
                    seen.add(fingerprint)
                    q["id"] = f"q{len(generated) + 1}"
                    generated.append(q)
                if len(generated) >= count:
                    break

        return {
            "title": "AI & NLP Generated Quiz",
            "question_count": len(generated),
            "questions": generated,
            "analysis": self.nlp.analyze(text),
        }
