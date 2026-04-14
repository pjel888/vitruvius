"""Pure-numpy TransE link predictor — Task E.4.

Trains entity + relation embeddings on a list of ``Triple`` (or a
canonical ``003/shared/relationships/`` directory) using margin
hinge loss with 1:1 negative sampling, then ranks candidate tails for
``(head, relation, ?)`` queries by ascending ``||h + r - t||_2``.
Deterministic given a seed; persists to JSON only (no pickle, no .npy).
"""

from __future__ import annotations

import json
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np


DEFAULT_EMBED_DIM = 50
DEFAULT_LEARNING_RATE = 0.01
DEFAULT_MARGIN = 1.0
DEFAULT_EPOCHS = 100
DEFAULT_SEED = 0
MIN_TRIPLES_NO_WARN = 20

_NORM_EPS = 1e-9
_REQUIRED_FRONTMATTER = ("from_entity", "to_entity", "relationship_type")


@dataclass(frozen=True)
class Triple:
    head: str
    relation: str
    tail: str


@dataclass
class TransEModel:
    entity_vocab: tuple[str, ...]
    relation_vocab: tuple[str, ...]
    entity_embeddings: np.ndarray
    relation_embeddings: np.ndarray
    dim: int
    epochs_run: int
    final_loss: float

    @property
    def n_entities(self) -> int:
        return len(self.entity_vocab)

    @property
    def n_relations(self) -> int:
        return len(self.relation_vocab)


@dataclass(frozen=True)
class LinkCandidate:
    head: str
    relation: str
    tail: str
    score: float
    rank: int


@dataclass(frozen=True)
class LinkPredictionReport:
    query_head: str
    query_relation: str
    candidates: tuple[LinkCandidate, ...]


def _build_vocab(triples: Sequence[Triple]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    entities = sorted({t.head for t in triples} | {t.tail for t in triples})
    relations = sorted({t.relation for t in triples})
    return tuple(entities), tuple(relations)


def _vocab_index(vocab: tuple[str, ...]) -> dict[str, int]:
    return {name: i for i, name in enumerate(vocab)}


def _normalise_rows(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / (norms + _NORM_EPS)


def _sample_negative(
    h_idx: int,
    t_idx: int,
    n_entities: int,
    rng: np.random.Generator,
) -> tuple[int, int]:
    if n_entities <= 1:
        return h_idx, t_idx
    corrupt_head = bool(rng.integers(0, 2))
    if corrupt_head:
        new_h = int(rng.integers(0, n_entities))
        while new_h == h_idx:
            new_h = int(rng.integers(0, n_entities))
        return new_h, t_idx
    new_t = int(rng.integers(0, n_entities))
    while new_t == t_idx:
        new_t = int(rng.integers(0, n_entities))
    return h_idx, new_t


def train_transe(
    triples: Sequence[Triple],
    *,
    dim: int = DEFAULT_EMBED_DIM,
    learning_rate: float = DEFAULT_LEARNING_RATE,
    margin: float = DEFAULT_MARGIN,
    epochs: int = DEFAULT_EPOCHS,
    seed: int = DEFAULT_SEED,
) -> TransEModel:
    if not triples:
        raise ValueError("train_transe requires at least one triple")

    if len(triples) < MIN_TRIPLES_NO_WARN:
        warnings.warn(
            (
                f"TransE training on {len(triples)} triples "
                f"(min recommended {MIN_TRIPLES_NO_WARN}); "
                "model will be undertrained."
            ),
            UserWarning,
            stacklevel=2,
        )

    entity_vocab, relation_vocab = _build_vocab(triples)
    ent_index = _vocab_index(entity_vocab)
    rel_index = _vocab_index(relation_vocab)
    n_entities = len(entity_vocab)
    n_relations = len(relation_vocab)

    rng = np.random.default_rng(seed)
    bound = 6.0 / np.sqrt(dim)
    ent = rng.uniform(-bound, bound, size=(n_entities, dim))
    rel = rng.uniform(-bound, bound, size=(n_relations, dim))
    rel = _normalise_rows(rel)
    ent = _normalise_rows(ent)

    triple_matrix = np.array(
        [
            (ent_index[t.head], rel_index[t.relation], ent_index[t.tail])
            for t in triples
        ],
        dtype=np.int64,
    )
    n_triples = triple_matrix.shape[0]
    epoch_loss = 0.0

    for _ in range(epochs):
        order = np.arange(n_triples)
        rng.shuffle(order)
        epoch_loss = 0.0
        for i in order:
            h, r, t = triple_matrix[i]
            h_neg, t_neg = _sample_negative(int(h), int(t), n_entities, rng)
            pos_vec = ent[h] + rel[r] - ent[t]
            neg_vec = ent[h_neg] + rel[r] - ent[t_neg]
            d_pos = float(np.linalg.norm(pos_vec))
            d_neg = float(np.linalg.norm(neg_vec))
            loss = margin + d_pos - d_neg
            if loss <= 0.0:
                continue
            epoch_loss += loss
            grad_pos = pos_vec / (d_pos + _NORM_EPS)
            grad_neg = neg_vec / (d_neg + _NORM_EPS)
            ent[h] -= learning_rate * grad_pos
            ent[t] += learning_rate * grad_pos
            rel[r] -= learning_rate * (grad_pos - grad_neg)
            ent[h_neg] += learning_rate * grad_neg
            ent[t_neg] -= learning_rate * grad_neg
        ent = _normalise_rows(ent)

    return TransEModel(
        entity_vocab=entity_vocab,
        relation_vocab=relation_vocab,
        entity_embeddings=ent,
        relation_embeddings=rel,
        dim=dim,
        epochs_run=epochs,
        final_loss=float(epoch_loss),
    )


def score_triple(model: TransEModel, head: str, relation: str, tail: str) -> float:
    ent_index = _vocab_index(model.entity_vocab)
    rel_index = _vocab_index(model.relation_vocab)
    if head not in ent_index:
        raise KeyError(f"unknown entity: {head!r}")
    if tail not in ent_index:
        raise KeyError(f"unknown entity: {tail!r}")
    if relation not in rel_index:
        raise KeyError(f"unknown relation: {relation!r}")
    h_vec = model.entity_embeddings[ent_index[head]]
    r_vec = model.relation_embeddings[rel_index[relation]]
    t_vec = model.entity_embeddings[ent_index[tail]]
    return float(np.linalg.norm(h_vec + r_vec - t_vec))


def predict_tail(
    model: TransEModel,
    head: str,
    relation: str,
    *,
    top_k: int = 5,
) -> LinkPredictionReport:
    ent_index = _vocab_index(model.entity_vocab)
    rel_index = _vocab_index(model.relation_vocab)
    if head not in ent_index or relation not in rel_index:
        return LinkPredictionReport(
            query_head=head,
            query_relation=relation,
            candidates=(),
        )
    h_vec = model.entity_embeddings[ent_index[head]]
    r_vec = model.relation_embeddings[rel_index[relation]]
    target = h_vec + r_vec
    distances = np.linalg.norm(model.entity_embeddings - target, axis=1)
    k = max(0, min(top_k, model.n_entities))
    if k == 0:
        return LinkPredictionReport(
            query_head=head,
            query_relation=relation,
            candidates=(),
        )
    order = np.argsort(distances, kind="stable")[:k]
    candidates = tuple(
        LinkCandidate(
            head=head,
            relation=relation,
            tail=model.entity_vocab[int(idx)],
            score=float(distances[int(idx)]),
            rank=rank + 1,
        )
        for rank, idx in enumerate(order)
    )
    return LinkPredictionReport(
        query_head=head,
        query_relation=relation,
        candidates=candidates,
    )


def save_model(model: TransEModel, out_path: Path) -> None:
    payload = {
        "entity_vocab": list(model.entity_vocab),
        "relation_vocab": list(model.relation_vocab),
        "entity_embeddings": model.entity_embeddings.tolist(),
        "relation_embeddings": model.relation_embeddings.tolist(),
        "dim": int(model.dim),
        "epochs_run": int(model.epochs_run),
        "final_loss": float(model.final_loss),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def load_model(path: Path) -> TransEModel:
    data = json.loads(path.read_text(encoding="utf-8"))
    entity_vocab = tuple(data["entity_vocab"])
    relation_vocab = tuple(data["relation_vocab"])
    entity_embeddings = np.array(data["entity_embeddings"], dtype=np.float64)
    relation_embeddings = np.array(data["relation_embeddings"], dtype=np.float64)
    return TransEModel(
        entity_vocab=entity_vocab,
        relation_vocab=relation_vocab,
        entity_embeddings=entity_embeddings,
        relation_embeddings=relation_embeddings,
        dim=int(data["dim"]),
        epochs_run=int(data["epochs_run"]),
        final_loss=float(data["final_loss"]),
    )


def _parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    body = "\n".join(lines[1:end])
    import yaml

    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def load_triples_from_canonical(
    relationships_dir: Path,
) -> list[Triple]:
    if not relationships_dir.exists() or not relationships_dir.is_dir():
        return []
    triples: list[Triple] = []
    for md_path in sorted(relationships_dir.glob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
        except OSError:
            warnings.warn(
                f"could not read relationship file {md_path}", UserWarning, stacklevel=2
            )
            continue
        meta = _parse_frontmatter(text)
        if meta is None:
            warnings.warn(
                f"{md_path.name}: missing or unparseable YAML frontmatter; skipping",
                UserWarning,
                stacklevel=2,
            )
            continue
        missing = [k for k in _REQUIRED_FRONTMATTER if not meta.get(k)]
        if missing:
            warnings.warn(
                f"{md_path.name}: frontmatter missing fields {missing}; skipping",
                UserWarning,
                stacklevel=2,
            )
            continue
        triples.append(
            Triple(
                head=str(meta["from_entity"]),
                relation=str(meta["relationship_type"]),
                tail=str(meta["to_entity"]),
            )
        )
    return triples
