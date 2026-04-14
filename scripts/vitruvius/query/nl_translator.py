from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Callable, Sequence


ALLOWED_FUNCTIONS: tuple[str, ...] = (
    "what_governs",
    "what_requires",
    "what_limits",
    "what_defines",
    "what_depends_on",
    "what_affects",
    "supersession_chain",
    "neighbors",
    "edges_between",
)

_MAX_KNOWN_ENTITIES = 100

_KEYWORD_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("what_governs", re.compile(r"\b(govern|governs|governed)\b", re.IGNORECASE)),
    ("what_requires", re.compile(r"\b(require|requires|required|requirement)\b", re.IGNORECASE)),
    ("what_limits", re.compile(r"\b(limit|limits|limited|restrict|restricts|cap|caps)\b", re.IGNORECASE)),
    ("what_defines", re.compile(r"\b(define|defines|defined|definition)\b", re.IGNORECASE)),
    ("what_depends_on", re.compile(r"\b(depend|depends|depended|dependency)\b", re.IGNORECASE)),
    ("what_affects", re.compile(r"\b(affect|affects|affected|impact|impacts)\b", re.IGNORECASE)),
    ("supersession_chain", re.compile(r"\b(superseded|supersedes|supersede|replaced|replaces)\b", re.IGNORECASE)),
    ("edges_between", re.compile(r"\b(between)\b", re.IGNORECASE)),
    ("neighbors", re.compile(r"\b(neighbor|neighbors|connected|related)\b", re.IGNORECASE)),
)


@dataclass(frozen=True)
class TranslationResult:
    function: str
    arguments: dict[str, str]
    confidence: float


def _match_subject(question: str, known_entities: Sequence[str]) -> str | None:
    lowered = question.lower()
    best: tuple[int, str] | None = None
    for entity in known_entities:
        slug = entity.split("-", 1)[-1] if "-" in entity else entity
        needle = slug.replace("-", " ").lower()
        if needle and needle in lowered:
            score = len(needle)
            if best is None or score > best[0]:
                best = (score, entity)
    return best[1] if best else None


def _regex_fallback(
    question: str,
    known_entities: Sequence[str],
) -> TranslationResult:
    for func, pattern in _KEYWORD_PATTERNS:
        if pattern.search(question):
            subject = _match_subject(question, known_entities)
            if subject is None:
                if func == "edges_between":
                    return TranslationResult(
                        function="neighbors",
                        arguments={},
                        confidence=0.1,
                    )
                return TranslationResult(
                    function=func,
                    arguments={},
                    confidence=0.3,
                )
            if func == "edges_between":
                # edges_between needs two entities; fall back to neighbors
                # with a single subject if we cannot find two.
                return TranslationResult(
                    function="neighbors",
                    arguments={"subject": subject},
                    confidence=0.4,
                )
            return TranslationResult(
                function=func,
                arguments={"subject": subject},
                confidence=0.75,
            )
    return TranslationResult(
        function="neighbors",
        arguments={},
        confidence=0.1,
    )


def _parse_llm_response(
    response: str,
    known_entities: Sequence[str],
) -> TranslationResult | None:
    try:
        payload = json.loads(response)
    except (ValueError, TypeError):
        return None
    if not isinstance(payload, dict):
        return None
    func = payload.get("function")
    if not isinstance(func, str) or func not in ALLOWED_FUNCTIONS:
        return None
    raw_args = payload.get("arguments") or {}
    if not isinstance(raw_args, dict):
        raw_args = {}
    args: dict[str, str] = {}
    for k, v in raw_args.items():
        if isinstance(k, str) and isinstance(v, str):
            args[k] = v
    confidence_raw = payload.get("confidence", 0.0)
    try:
        confidence = float(confidence_raw)
    except (TypeError, ValueError):
        confidence = 0.0
    subject = args.get("subject")
    if subject is not None and known_entities and subject not in known_entities:
        return None
    return TranslationResult(function=func, arguments=args, confidence=confidence)


def build_llm_prompt(
    question: str,
    known_entities: Sequence[str],
) -> str:
    capped = list(known_entities)[:_MAX_KNOWN_ENTITIES]
    payload = {
        "task": "Translate a natural-language question into a structured query call",
        "question": question,
        "allowed_functions": list(ALLOWED_FUNCTIONS),
        "known_entities": capped,
        "output_schema": {
            "function": "one of allowed_functions",
            "arguments": {"subject": "one of known_entities"},
            "confidence": "0.0-1.0",
        },
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def translate_question(
    question: str,
    *,
    known_entities: Sequence[str],
    llm_caller: Callable[[str], str] | None = None,
) -> TranslationResult:
    if llm_caller is None:
        return _regex_fallback(question, known_entities)
    prompt = build_llm_prompt(question, known_entities)
    try:
        response = llm_caller(prompt)
    except Exception:
        return _regex_fallback(question, known_entities)
    parsed = _parse_llm_response(response, known_entities)
    if parsed is None:
        return _regex_fallback(question, known_entities)
    return parsed
