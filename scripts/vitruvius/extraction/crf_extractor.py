"""CRF extractor — Task E.3.

Loads the latest trained CRF model from ``model_dir`` and tags new token
sequences with BIO labels (``O``, ``B-SUBJ``, ``I-SUBJ``, ``B-PRED``,
``I-PRED``, ``B-OBJ``, ``I-OBJ``). Contiguous tag runs collapse into
``CrfCandidate`` records that mirror the existing regex extractor's
schema so ``pre_review_filter`` and ``ollama_review`` can consume both
streams without caller changes. When no model exists, returns ``[]``
and emits a ``UserWarning`` — the flag-on path never crashes.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

from .crf_trainer import (
    DEFAULT_MODEL_DIR,
    MODEL_FILENAME_PREFIX,
    token_features,
)

if TYPE_CHECKING:
    import pycrfsuite  # noqa: F401


_MODEL_SUFFIX = ".crfsuite"
_BIO_LABELS = frozenset(
    {
        "O",
        "B-SUBJ",
        "I-SUBJ",
        "B-PRED",
        "I-PRED",
        "B-OBJ",
        "I-OBJ",
    }
)


@dataclass(frozen=True)
class CrfCandidate:
    from_id: str
    predicate: str
    to_id: str
    occurrences: int
    examples: tuple[tuple[str, int, int], ...]
    source: str = "crf"


def find_latest_model_path(model_dir: Path = DEFAULT_MODEL_DIR) -> Path | None:
    if not model_dir.exists() or not model_dir.is_dir():
        return None
    candidates = sorted(
        p
        for p in model_dir.iterdir()
        if p.is_file()
        and p.name.startswith(MODEL_FILENAME_PREFIX)
        and p.name.endswith(_MODEL_SUFFIX)
    )
    return candidates[-1] if candidates else None


@lru_cache(maxsize=4)
def _load_tagger_for_path(model_path_str: str):
    import pycrfsuite

    tagger = pycrfsuite.Tagger()
    tagger.open(model_path_str)
    return tagger


def _featurize_to_crfsuite(features: dict[str, object]) -> list[str]:
    return [f"{key}={value}" for key, value in features.items()]


def _collapse_runs(
    tokens: Sequence[str], labels: Sequence[str]
) -> list[tuple[str, str, str, tuple[tuple[str, int, int], ...]]]:
    spans: dict[str, list[tuple[int, int]]] = {"SUBJ": [], "PRED": [], "OBJ": []}
    current_role: str | None = None
    current_start: int = -1

    def _close(end_inclusive: int) -> None:
        nonlocal current_role, current_start
        if current_role is not None and current_start >= 0:
            spans[current_role].append((current_start, end_inclusive))
        current_role = None
        current_start = -1

    for idx, raw_label in enumerate(labels):
        label = raw_label if raw_label in _BIO_LABELS else "O"
        if label == "O":
            _close(idx - 1)
            continue
        prefix, _, role = label.partition("-")
        if role not in spans:
            _close(idx - 1)
            continue
        if prefix == "B":
            _close(idx - 1)
            current_role = role
            current_start = idx
        elif prefix == "I":
            if current_role == role and current_start >= 0:
                continue
            _close(idx - 1)
            current_role = role
            current_start = idx
    _close(len(labels) - 1)

    if not (spans["SUBJ"] and spans["PRED"] and spans["OBJ"]):
        return []

    out: list[tuple[str, str, str, tuple[tuple[str, int, int], ...]]] = []
    for s_start, s_end in spans["SUBJ"]:
        for p_start, p_end in spans["PRED"]:
            for o_start, o_end in spans["OBJ"]:
                subj_text = " ".join(tokens[s_start : s_end + 1]).lower()
                pred_text = " ".join(tokens[p_start : p_end + 1]).lower()
                obj_text = " ".join(tokens[o_start : o_end + 1]).lower()
                if not (subj_text and pred_text and obj_text):
                    continue
                phrase = " ".join(tokens)
                example = (phrase, s_start, o_end)
                out.append((subj_text, pred_text, obj_text, (example,)))
    return out


def extract_from_sentence(
    tokens: Sequence[str],
    *,
    concept_vocabulary: frozenset[str] = frozenset(),
    model_dir: Path = DEFAULT_MODEL_DIR,
    pos_tags: Sequence[str] | None = None,
) -> list[CrfCandidate]:
    if not tokens:
        return []

    model_path = find_latest_model_path(model_dir)
    if model_path is None:
        warnings.warn(
            f"No CRF model found at {model_dir}; returning empty candidate list.",
            UserWarning,
            stacklevel=2,
        )
        return []

    tagger = _load_tagger_for_path(str(model_path))

    token_list = list(tokens)
    feature_seq = [
        _featurize_to_crfsuite(
            token_features(
                token_list,
                i,
                concept_vocabulary=concept_vocabulary,
                pos_tags=pos_tags,
            )
        )
        for i in range(len(token_list))
    ]
    labels = list(tagger.tag(feature_seq))

    runs = _collapse_runs(token_list, labels)
    return [
        CrfCandidate(
            from_id=subj,
            predicate=pred,
            to_id=obj,
            occurrences=1,
            examples=examples,
        )
        for subj, pred, obj, examples in runs
    ]


def extract_from_sentences(
    sentences: Sequence[Sequence[str]],
    *,
    concept_vocabulary: frozenset[str] = frozenset(),
    model_dir: Path = DEFAULT_MODEL_DIR,
) -> list[CrfCandidate]:
    if not sentences:
        return []

    merged: dict[tuple[str, str, str], CrfCandidate] = {}
    for tokens in sentences:
        for cand in extract_from_sentence(
            tokens,
            concept_vocabulary=concept_vocabulary,
            model_dir=model_dir,
        ):
            key = (cand.from_id, cand.predicate, cand.to_id)
            existing = merged.get(key)
            if existing is None:
                merged[key] = cand
            else:
                merged[key] = CrfCandidate(
                    from_id=existing.from_id,
                    predicate=existing.predicate,
                    to_id=existing.to_id,
                    occurrences=existing.occurrences + cand.occurrences,
                    examples=existing.examples + cand.examples,
                )

    return [merged[key] for key in sorted(merged.keys())]
