"""CRF trainer scaffold — Task E.2.

Trains a Conditional Random Fields sequence labeler on Phase 6 audit-log
keep/reject decisions. Refuses to train when the corpus has fewer than
``MIN_TRAINING_EXAMPLES`` (50) examples — the real audit log currently
holds only 2, so the scaffold ships infrastructure now and calibrates
when real data accumulates. Uses python-crfsuite with L-BFGS training
and persists model + metadata sidecar to disk under ``model_dir``.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


MIN_TRAINING_EXAMPLES = 50
DEFAULT_MODEL_DIR = Path("scripts/vitruvius/models")
MODEL_FILENAME_PREFIX = "crf_extractor_"
_TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"

_BOS = "<BOS>"
_EOS = "<EOS>"


class InsufficientTrainingDataError(ValueError):
    """Raised when the corpus has fewer than MIN_TRAINING_EXAMPLES examples."""


@dataclass(frozen=True)
class TrainingExample:
    tokens: tuple[str, ...]
    labels: tuple[str, ...]


@dataclass(frozen=True)
class TrainingMetadata:
    timestamp_utc: str
    training_corpus_hash: str
    example_count: int
    label_distribution: dict[str, int]
    model_path: str
    metadata_path: str


def token_features(
    tokens: Sequence[str],
    index: int,
    *,
    concept_vocabulary: frozenset[str] = frozenset(),
    pos_tags: Sequence[str] | None = None,
) -> dict[str, object]:
    if not tokens:
        raise ValueError("tokens must be non-empty")
    if not 0 <= index < len(tokens):
        raise IndexError(f"index {index} out of range for {len(tokens)} tokens")

    token = tokens[index]
    token_lower = token.lower()
    prev_token = tokens[index - 1] if index > 0 else _BOS
    next_token = tokens[index + 1] if index < len(tokens) - 1 else _EOS

    vocab_lower = {term.lower() for term in concept_vocabulary if term}
    in_vocab = bool(vocab_lower) and any(
        token_lower == term or token_lower in term or term in token_lower
        for term in vocab_lower
    )

    pos_tag = ""
    if pos_tags is not None and index < len(pos_tags):
        pos_tag = pos_tags[index]

    dist_to_root_verb = _distance_to_root_verb(tokens, index, pos_tags)

    return {
        "t": token_lower,
        "cap": token[:1].isupper(),
        "pos": pos_tag,
        "in_vocab": in_vocab,
        "prev_t": prev_token.lower() if prev_token not in (_BOS, _EOS) else prev_token,
        "next_t": next_token.lower() if next_token not in (_BOS, _EOS) else next_token,
        "bigram_prev": f"{prev_token}|{token}",
        "bigram_next": f"{token}|{next_token}",
        "dist_to_root_verb": dist_to_root_verb,
    }


def hash_corpus(examples: Sequence[TrainingExample]) -> str:
    digest = hashlib.sha256()
    for ex in examples:
        canonical = "|".join(ex.tokens) + "\t" + "|".join(ex.labels)
        digest.update(canonical.encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()[:16]


def train_crf(
    examples: Sequence[TrainingExample],
    *,
    model_dir: Path = DEFAULT_MODEL_DIR,
    concept_vocabulary: frozenset[str] = frozenset(),
    l2_coefficient: float = 1.0,
    max_iterations: int = 200,
    now_utc: datetime | None = None,
) -> TrainingMetadata:
    if len(examples) < MIN_TRAINING_EXAMPLES:
        raise InsufficientTrainingDataError(
            f"need >= {MIN_TRAINING_EXAMPLES} examples, got {len(examples)}"
        )

    for ex in examples:
        if len(ex.tokens) != len(ex.labels):
            raise ValueError(
                f"token/label length mismatch: {len(ex.tokens)} tokens vs "
                f"{len(ex.labels)} labels"
            )
        if not ex.tokens:
            raise ValueError("training example must have at least one token")

    import pycrfsuite

    model_dir.mkdir(parents=True, exist_ok=True)

    timestamp = now_utc or datetime.now(timezone.utc)
    timestamp_str = timestamp.strftime(_TIMESTAMP_FORMAT)
    model_filename = f"{MODEL_FILENAME_PREFIX}{timestamp_str}.crfsuite"
    metadata_filename = f"{MODEL_FILENAME_PREFIX}{timestamp_str}.meta.json"
    model_path = model_dir / model_filename
    metadata_path = model_dir / metadata_filename

    trainer = pycrfsuite.Trainer(verbose=False)
    label_distribution: dict[str, int] = {}

    for ex in examples:
        token_list = list(ex.tokens)
        pos_tags = _pos_tag_tokens(token_list)
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
        trainer.append(feature_seq, list(ex.labels))
        for label in ex.labels:
            label_distribution[label] = label_distribution.get(label, 0) + 1

    trainer.set_params(
        {
            "c1": 0.1,
            "c2": l2_coefficient,
            "max_iterations": max_iterations,
            "feature.possible_transitions": True,
        }
    )
    trainer.train(str(model_path))

    corpus_hash = hash_corpus(examples)

    metadata = TrainingMetadata(
        timestamp_utc=timestamp.isoformat(),
        training_corpus_hash=corpus_hash,
        example_count=len(examples),
        label_distribution=label_distribution,
        model_path=str(model_path),
        metadata_path=str(metadata_path),
    )

    metadata_path.write_text(json.dumps(asdict(metadata), indent=2, sort_keys=True))

    return metadata


def _featurize_to_crfsuite(features: dict[str, object]) -> list[str]:
    return [f"{key}={value}" for key, value in features.items()]


def _pos_tag_tokens(tokens: Sequence[str]) -> list[str]:
    return ["" for _ in tokens]


def _distance_to_root_verb(
    tokens: Sequence[str],
    index: int,
    pos_tags: Sequence[str] | None,
) -> int:
    if pos_tags is None:
        return len(tokens)
    for i, tag in enumerate(pos_tags):
        if tag == "VERB":
            return abs(i - index)
    return len(tokens)
