from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from .paths import get_repo_root


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def slugify(value: str) -> str:
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def title_case(value: str) -> str:
    return " ".join(word.capitalize() for word in value.split())


def build_concept_path(slug: str) -> Path:
    repo_root = get_repo_root()
    return repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / f"{slug}.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# --------------------------------------------------
# HEURISTICS
# --------------------------------------------------

def derive_aliases(concept: str) -> List[str]:
    aliases = []

    if concept == "occupancy classification":
        aliases.extend([
            "occupancy",
            "building occupancy classification",
        ])

    if concept == "means of egress":
        aliases.extend([
            "egress",
            "exit systems",
        ])

    return aliases


def derive_related_sources(concept: str) -> List[str]:
    # For now, we assume PD 1096 ecosystem
    return [
        "law-national-building-code-of-the-philippines",
        "irr-implementing-rules-and-regulations-of-the-national-building-code",
    ]


def derive_related_concepts(concept: str) -> List[str]:
    if concept == "occupancy classification":
        return [
            "occupancy load",
            "means of egress",
        ]

    if concept == "means of egress":
        return [
            "occupancy load",
            "exit width",
        ]

    return []


def derive_definition(concept: str) -> str:
    if concept == "occupancy classification":
        return (
            "Occupancy classification refers to the categorization of buildings or portions of buildings "
            "based on their use, which determines the applicable safety, design, and regulatory requirements."
        )

    if concept == "building permits":
        return (
            "A building permit is a formal approval issued by the local authority allowing construction, "
            "renovation, or alteration to proceed in compliance with applicable laws and regulations."
        )

    if concept == "light and ventilation":
        return (
            "Light and ventilation refer to the minimum requirements for natural lighting and airflow in "
            "buildings to ensure health, safety, and comfort of occupants."
        )

    # fallback
    return f"{title_case(concept)} is a defined concept within the Vitruvius knowledge system."


# --------------------------------------------------
# MARKDOWN GENERATION
# --------------------------------------------------

def build_concept_markdown(concept: str) -> str:
    slug = slugify(concept)
    title = title_case(concept)

    aliases = derive_aliases(concept)
    related_sources = derive_related_sources(concept)
    related_concepts = derive_related_concepts(concept)
    definition = derive_definition(concept)

    lines = [
        "---",
        f"id: concept-{slug}",
        f"title: {title}",
        "page_type: concept",
        "",
        "aliases:",
    ]

    if aliases:
        for a in aliases:
            lines.append(f"  - {a}")
    else:
        lines.append("  - none")

    lines.extend([
        "",
        "related_sources:",
    ])

    for s in related_sources:
        lines.append(f"  - {s}")

    lines.extend([
        "",
        "related_concepts:",
    ])

    if related_concepts:
        for rc in related_concepts:
            lines.append(f"  - {rc}")
    else:
        lines.append("  - none")

    lines.extend([
        "",
        "canonical_status: draft",
        f"last_canonicalized_utc: {utc_now()}",
        "---",
        "",
        f"# {title}",
        "",
        "## Definition",
        "",
        definition,
        "",
        "## Why It Matters",
        "",
        "- To be refined",
        "",
        "## Regulatory Basis",
        "",
        "- National Building Code of the Philippines",
        "- Implementing Rules and Regulations of the National Building Code",
        "",
        "## Relationships",
        "",
    ])

    if related_concepts:
        for rc in related_concepts:
            lines.append(f"- relates_to: {rc}")
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Source Linkage",
        "",
    ])

    for s in related_sources:
        lines.append(f"- {s}")

    lines.extend([
        "",
        "## Notes",
        "",
        "This concept page was generated automatically by canonicalize-concept-one.",
        "Further refinement is required.",
        "",
    ])

    return "\n".join(lines)


# --------------------------------------------------
# COMMAND
# --------------------------------------------------

def run_canonicalize_concept_one(concept_name: str) -> int:
    slug = slugify(concept_name)
    target_path = build_concept_path(slug)

    if target_path.exists():
        print(f"SKIP: Concept already exists -> {target_path}")
        return 0

    target_path.parent.mkdir(parents=True, exist_ok=True)

    markdown = build_concept_markdown(concept_name)
    target_path.write_text(markdown, encoding="utf-8")

    print("Canonicalize-concept-one complete.")
    print(f"Created: {target_path}")

    return 0