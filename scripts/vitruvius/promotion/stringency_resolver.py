from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml

StringencyVector = Literal["maximize", "minimize", "qualitative"]
DEFAULT_STRINGENCY_VECTOR: StringencyVector = "qualitative"

_VALID_VECTORS: frozenset[str] = frozenset(("maximize", "minimize", "qualitative"))
_FRONTMATTER_FENCE = "---"


@dataclass(frozen=True)
class CandidateEdge:
    """A minimal edge shape for resolver testing."""

    edge_id: str
    from_entity: str
    predicate: str
    to_entity: str
    numeric_value: float | None
    jurisdiction: str


@dataclass(frozen=True)
class StringencyVerdict:
    winner_edge_id: str | None
    loser_edge_id: str | None
    unresolved: bool
    reason: str


@dataclass(frozen=True)
class MigrationReport:
    total_files: int
    files_updated: int
    files_skipped: int
    updated_paths: tuple[str, ...]
    dry_run: bool


def _require_numeric(edge: CandidateEdge, vector: StringencyVector) -> None:
    if edge.numeric_value is None:
        raise ValueError(
            f"resolve_stringency: edge {edge.edge_id!r} has numeric_value=None "
            f"but stringency_vector={vector!r} requires a scalar value"
        )


def resolve_stringency(
    edge_a: CandidateEdge,
    edge_b: CandidateEdge,
    *,
    stringency_vector: StringencyVector,
) -> StringencyVerdict:
    """Pick the more-stringent edge based on `stringency_vector`."""
    if stringency_vector not in _VALID_VECTORS:
        raise ValueError(
            f"resolve_stringency: unknown stringency_vector {stringency_vector!r}; "
            f"expected one of {sorted(_VALID_VECTORS)}"
        )

    if stringency_vector == "qualitative":
        return StringencyVerdict(
            winner_edge_id=None,
            loser_edge_id=None,
            unresolved=True,
            reason=(
                f"qualitative comparison between {edge_a.edge_id!r} and "
                f"{edge_b.edge_id!r}: unresolved (caller delegates to LLM "
                f"or human ranger)"
            ),
        )

    _require_numeric(edge_a, stringency_vector)
    _require_numeric(edge_b, stringency_vector)

    value_a = edge_a.numeric_value
    value_b = edge_b.numeric_value
    assert value_a is not None and value_b is not None  # narrowed by checks above

    if stringency_vector == "maximize":
        a_wins = value_a >= value_b
    else:  # minimize
        a_wins = value_a <= value_b

    winner = edge_a if a_wins else edge_b
    loser = edge_b if a_wins else edge_a

    return StringencyVerdict(
        winner_edge_id=winner.edge_id,
        loser_edge_id=loser.edge_id,
        unresolved=False,
        reason=(
            f"stringency_vector={stringency_vector}: "
            f"{edge_a.edge_id}={value_a} vs {edge_b.edge_id}={value_b} "
            f"=> winner={winner.edge_id}"
        ),
    )


def _split_frontmatter(text: str) -> tuple[dict | None, str, str]:
    """Return (frontmatter_dict, frontmatter_block, body) or (None, "", text)."""
    if not text.startswith(_FRONTMATTER_FENCE):
        return None, "", text

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != _FRONTMATTER_FENCE:
        return None, "", text

    closing_index: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx].rstrip("\r\n") == _FRONTMATTER_FENCE:
            closing_index = idx
            break

    if closing_index is None:
        return None, "", text

    frontmatter_block = "".join(lines[1:closing_index])
    body = "".join(lines[closing_index + 1 :])

    try:
        parsed = yaml.safe_load(frontmatter_block) or {}
    except yaml.YAMLError:
        return None, "", text

    if not isinstance(parsed, dict):
        return None, "", text

    return parsed, frontmatter_block, body


def _serialize_frontmatter(frontmatter: dict, body: str) -> str:
    dumped = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    return f"{_FRONTMATTER_FENCE}\n{dumped}{_FRONTMATTER_FENCE}\n{body}"


def migrate_concept_frontmatter(
    concepts_dir: Path,
    *,
    dry_run: bool = True,
    default_vector: StringencyVector = DEFAULT_STRINGENCY_VECTOR,
) -> MigrationReport:
    """Add `stringency_vector: qualitative` to every concept .md lacking it."""
    if default_vector not in _VALID_VECTORS:
        raise ValueError(
            f"migrate_concept_frontmatter: invalid default_vector "
            f"{default_vector!r}; expected one of {sorted(_VALID_VECTORS)}"
        )

    md_files = sorted(p for p in concepts_dir.glob("*.md") if p.is_file())
    total = len(md_files)
    updated_relpaths: list[str] = []
    skipped = 0

    for path in md_files:
        text = path.read_text(encoding="utf-8")
        frontmatter, _block, body = _split_frontmatter(text)

        if frontmatter is None:
            skipped += 1
            continue

        if "stringency_vector" in frontmatter:
            skipped += 1
            continue

        frontmatter["stringency_vector"] = default_vector
        updated_relpaths.append(path.name)

        if not dry_run:
            new_text = _serialize_frontmatter(frontmatter, body)
            path.write_text(new_text, encoding="utf-8")

    return MigrationReport(
        total_files=total,
        files_updated=len(updated_relpaths),
        files_skipped=skipped,
        updated_paths=tuple(sorted(updated_relpaths)),
        dry_run=dry_run,
    )
