"""Naive Bayes pre-review filter scaffold (Task F.1)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Sequence

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB


MIN_TRAINING_EXAMPLES = 50
DEFAULT_AUTO_ACCEPT_THRESHOLD = 0.95
DEFAULT_AUTO_REJECT_THRESHOLD = 0.05


Decision = Literal["keep", "reject"]
FilterAction = Literal["auto_accept", "auto_reject", "forward_to_llm"]


class InsufficientTrainingDataError(ValueError):
    """Raised when the corpus has fewer than MIN_TRAINING_EXAMPLES."""


@dataclass(frozen=True)
class CandidateFeatures:
    predicate: str
    regex_pattern_id: str
    char_distance: int
    evidence_length: int
    verb_voice: Literal["active", "passive", "unknown"]
    has_negation: bool


@dataclass(frozen=True)
class FilterDecision:
    action: FilterAction
    probability_keep: float
    probability_reject: float
    reason: str


@dataclass(frozen=True)
class TrainingExample:
    features: CandidateFeatures
    decision: Decision


@dataclass
class NBFilter:
    vectorizer: DictVectorizer | None = None
    model: MultinomialNB | None = None
    auto_accept_threshold: float = DEFAULT_AUTO_ACCEPT_THRESHOLD
    auto_reject_threshold: float = DEFAULT_AUTO_REJECT_THRESHOLD
    is_fitted: bool = False


def _features_to_dict(f: CandidateFeatures) -> dict[str, float | str]:
    return {
        "predicate": f.predicate,
        "regex_pattern_id": f.regex_pattern_id,
        "char_distance": float(f.char_distance),
        "evidence_length": float(f.evidence_length),
        "verb_voice": f.verb_voice,
        "has_negation": 1.0 if f.has_negation else 0.0,
    }


def _ensure_non_negative(matrix: np.ndarray) -> np.ndarray:
    # MultinomialNB requires non-negative features. All inputs from
    # _features_to_dict are already non-negative by construction, but
    # guard against upstream drift.
    if np.any(matrix < 0):
        raise ValueError("feature matrix must be non-negative for MultinomialNB")
    return matrix


def fit_filter(
    examples: Sequence[TrainingExample],
    *,
    auto_accept_threshold: float = DEFAULT_AUTO_ACCEPT_THRESHOLD,
    auto_reject_threshold: float = DEFAULT_AUTO_REJECT_THRESHOLD,
) -> NBFilter:
    if len(examples) < MIN_TRAINING_EXAMPLES:
        raise InsufficientTrainingDataError(
            f"need at least {MIN_TRAINING_EXAMPLES} examples, got {len(examples)}"
        )

    labels = [ex.decision for ex in examples]
    distinct = set(labels)
    if len(distinct) < 2:
        raise ValueError(
            f"training corpus must contain both 'keep' and 'reject' labels, got {distinct}"
        )

    feature_dicts = [_features_to_dict(ex.features) for ex in examples]
    vectorizer = DictVectorizer(sparse=False, sort=True)
    matrix = vectorizer.fit_transform(feature_dicts)
    _ensure_non_negative(matrix)

    model = MultinomialNB()
    model.fit(matrix, labels)

    return NBFilter(
        vectorizer=vectorizer,
        model=model,
        auto_accept_threshold=auto_accept_threshold,
        auto_reject_threshold=auto_reject_threshold,
        is_fitted=True,
    )


def _prob_keep(model: MultinomialNB, row: np.ndarray) -> float:
    probs = model.predict_proba(row)[0]
    classes = list(model.classes_)
    if "keep" not in classes:
        return 0.0
    return float(probs[classes.index("keep")])


def classify(filter_: NBFilter, features: CandidateFeatures) -> FilterDecision:
    if not filter_.is_fitted or filter_.model is None or filter_.vectorizer is None:
        return FilterDecision(
            action="forward_to_llm",
            probability_keep=0.5,
            probability_reject=0.5,
            reason="filter not fitted",
        )

    row = filter_.vectorizer.transform([_features_to_dict(features)])
    p_keep = _prob_keep(filter_.model, row)
    p_reject = 1.0 - p_keep

    if p_keep >= filter_.auto_accept_threshold:
        action: FilterAction = "auto_accept"
        reason = f"p(keep)={p_keep:.3f} >= {filter_.auto_accept_threshold}"
    elif p_keep <= filter_.auto_reject_threshold:
        action = "auto_reject"
        reason = f"p(keep)={p_keep:.3f} <= {filter_.auto_reject_threshold}"
    else:
        action = "forward_to_llm"
        reason = (
            f"p(keep)={p_keep:.3f} in ({filter_.auto_reject_threshold}, "
            f"{filter_.auto_accept_threshold})"
        )

    return FilterDecision(
        action=action,
        probability_keep=p_keep,
        probability_reject=p_reject,
        reason=reason,
    )


def save_filter(filter_: NBFilter, out_path: Path) -> None:
    if not filter_.is_fitted or filter_.model is None or filter_.vectorizer is None:
        raise ValueError("cannot save an unfitted filter")

    model = filter_.model
    vectorizer = filter_.vectorizer
    state = {
        "class_log_prior": model.class_log_prior_.tolist(),
        "feature_log_prob": model.feature_log_prob_.tolist(),
        "classes": list(model.classes_.tolist()),
        "n_features_in": int(model.n_features_in_),
        "vectorizer_feature_names": list(vectorizer.feature_names_),
        "vectorizer_vocabulary": {k: int(v) for k, v in vectorizer.vocabulary_.items()},
        "auto_accept_threshold": filter_.auto_accept_threshold,
        "auto_reject_threshold": filter_.auto_reject_threshold,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(state, sort_keys=True, indent=2))


def load_filter(path: Path) -> NBFilter:
    payload = json.loads(path.read_text())

    model = MultinomialNB()
    model.class_log_prior_ = np.array(payload["class_log_prior"], dtype=float)
    model.feature_log_prob_ = np.array(payload["feature_log_prob"], dtype=float)
    model.classes_ = np.array(payload["classes"])
    model.n_features_in_ = int(payload["n_features_in"])
    # MultinomialNB.predict_proba also reads class_count_ only during fit;
    # predict_proba itself only needs class_log_prior_ and feature_log_prob_.

    vectorizer = DictVectorizer(sparse=False, sort=True)
    vectorizer.feature_names_ = list(payload["vectorizer_feature_names"])
    vectorizer.vocabulary_ = {k: int(v) for k, v in payload["vectorizer_vocabulary"].items()}

    return NBFilter(
        vectorizer=vectorizer,
        model=model,
        auto_accept_threshold=float(payload["auto_accept_threshold"]),
        auto_reject_threshold=float(payload["auto_reject_threshold"]),
        is_fitted=True,
    )
