from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from .paths import get_repo_root


VALID_PREFIX = "concept"


def slugify(value: str) -> str:
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


def build_id(name: str) -> str:
    return f"{VALID_PREFIX}-{slugify(name)}"


def run_canonicalize_concept_one(*, concept_name: str) -> int:
    name = concept_name
    repo_root = get_repo_root()

    slug = slugify(name)
    target = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    target.mkdir(parents=True, exist_ok=True)

    file = target / f"{slug}.md"

    if file.exists():
        print(f"SKIP: Concept already exists -> {file}")
        return 0

    lines = [
        "---",
        f"id: {build_id(name)}",
        f"title: {name.title()}",
        "page_type: concept",
        "canonical_status: draft",
        f"last_canonicalized_utc: {datetime.now(timezone.utc).isoformat()}",
        "---\n",
        f"# {name.title()}",
        "\n## Definition\n",
        f"{name.title()} is a defined concept within the Vitruvius system.",
    ]

    file.write_text("\n".join(lines), encoding="utf-8")

    print("canonicalize-concept-one complete.")
    print(f"Created: {file}")

    return 0