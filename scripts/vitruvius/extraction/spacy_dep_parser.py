"""spaCy dependency-parser Subject-Verb-Object triplet extractor — Task E.1.

Replaces regex-based relationship mining with syntactic awareness. Loads
`en_core_web_sm` lazily on first call (module import is always free) and
emits `SvoCandidate` records per sentence. When a `concept_vocabulary` is
supplied the emitted triplets are filtered to those whose subject or
object lemma substring-matches a vocabulary entry — principle P7, the
closed concept vocabulary gate that keeps noise out of the LLM review
layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:
    from spacy.language import Language  # noqa: F401


SPACY_MODEL_NAME = "en_core_web_sm"

_SUBJECT_DEPS = frozenset({"nsubj", "nsubjpass", "csubj", "csubjpass"})
_DIRECT_OBJECT_DEPS = frozenset({"dobj", "obj", "attr", "oprd"})


@dataclass(frozen=True)
class SvoCandidate:
    subject: str
    verb: str
    object: str
    sentence: str
    source_section_id: str
    sentence_start: int
    sentence_end: int
    # Stream Y1.5 — optional identity propagation. When the caller
    # passes a SourceIdentity to extract_svo_triplets, every emitted
    # candidate carries its fingerprint so downstream review paths can
    # cross-check against the priming identity. Default None preserves
    # legacy callers byte-for-byte.
    source_identity_fingerprint: "str | None" = None


@lru_cache(maxsize=1)
def _get_nlp() -> "Language":
    import spacy

    return spacy.load(SPACY_MODEL_NAME)


def extract_svo_triplets(
    text: str,
    *,
    concept_vocabulary: Iterable[str] | None = None,
    source_section_id: str = "",
    source_identity: "Any" = None,  # Stream Y1.5 — optional priming identity
) -> list[SvoCandidate]:
    if not text or not text.strip():
        return []

    vocab_terms: list[str] | None = None
    if concept_vocabulary is not None:
        vocab_terms = [term.lower() for term in concept_vocabulary if term]

    fingerprint = getattr(source_identity, "fingerprint", None)

    nlp = _get_nlp()
    doc = nlp(text)

    candidates: list[SvoCandidate] = []
    for sent in doc.sents:
        sentence_text = sent.text
        sentence_start = sent.start_char
        sentence_end = sent.end_char

        for token in sent:
            if token.dep_ != "ROOT":
                continue
            if token.pos_ not in {"VERB", "AUX"}:
                continue

            subjects = _collect_subjects(token)
            objects = _collect_objects(token)
            if not subjects or not objects:
                continue

            verb_lemma = token.lemma_.lower() or token.text.lower()

            for subj_text in subjects:
                for obj_text in objects:
                    if vocab_terms is not None and not _matches_vocab(
                        subj_text, obj_text, vocab_terms
                    ):
                        continue
                    candidates.append(
                        SvoCandidate(
                            subject=subj_text,
                            verb=verb_lemma,
                            object=obj_text,
                            sentence=sentence_text,
                            source_section_id=source_section_id,
                            sentence_start=sentence_start,
                            sentence_end=sentence_end,
                            source_identity_fingerprint=fingerprint,
                        )
                    )

    return candidates


def _collect_subjects(root) -> list[str]:
    out: list[str] = []
    for child in root.children:
        if child.dep_ in _SUBJECT_DEPS:
            out.append((child.lemma_ or child.text).lower())
    return out


def _collect_objects(root) -> list[str]:
    out: list[str] = []
    for child in root.children:
        if child.dep_ in _DIRECT_OBJECT_DEPS:
            out.append((child.lemma_ or child.text).lower())
            continue
        if child.dep_ == "agent":
            for sub in child.children:
                if sub.dep_ == "pobj":
                    out.append((sub.lemma_ or sub.text).lower())
        elif child.dep_ == "prep":
            for sub in child.children:
                if sub.dep_ == "pobj":
                    out.append((sub.lemma_ or sub.text).lower())
    return out


def _matches_vocab(subject: str, obj: str, vocab_terms: list[str]) -> bool:
    subject_l = subject.lower()
    object_l = obj.lower()
    for term in vocab_terms:
        if subject_l and (subject_l in term or term in subject_l):
            return True
        if object_l and (object_l in term or term in object_l):
            return True
    return False
