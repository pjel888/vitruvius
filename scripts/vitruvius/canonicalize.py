from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .constants import CONVERSION_LAYER_NAME
from .paths import get_repo_root


# --------------------------------------------------
# STRICT ID SYSTEM
# --------------------------------------------------

VALID_PREFIXES = {
    "law",
    "irr",
    "concept",
    "glossary",
    "relationship",
    "handout",
    "reviewer",
    "law-section",
    "source",
}


def slugify(value: str) -> str:
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


def validate_prefix(prefix: str):
    if prefix not in VALID_PREFIXES:
        raise ValueError(f"INVALID PREFIX: {prefix}")


def build_canonical_id(prefix: str, title: str) -> str:
    validate_prefix(prefix)
    return f"{prefix}-{slugify(title)}"


# --------------------------------------------------
# LOAD RULES
# --------------------------------------------------

def load_rules():
    repo_root = get_repo_root()
    path = repo_root / "scripts" / "vitruvius" / "rules" / "canonical_rules.yaml"

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# --------------------------------------------------
# MATCHING ENGINE
# --------------------------------------------------

def matches_rule(rule: dict, path: str) -> bool:
    path = path.lower()
    match = rule.get("match", {})

    if "all_contains" in match:
        if any(term not in path for term in match["all_contains"]):
            return False

    if "any_contains" in match:
        if not any(term in path for term in match["any_contains"]):
            return False

    if "not_contains" in match:
        if any(term in path for term in match["not_contains"]):
            return False

    return True


def find_rule(rules: dict, path: str):
    for rule in rules.get("rules", []):
        if matches_rule(rule, path):
            return rule
    return None


# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------

def normalize_title(path: str, rule: dict | None) -> str:
    if rule and "canonical" in rule and "title" in rule["canonical"]:
        return rule["canonical"]["title"]

    return Path(path).stem


def map_source_type_to_prefix(source_type: str) -> str:
    mapping = {
        "law": "law",
        "irr": "irr",
        "law_section": "law-section",
        "handout": "handout",
        "reviewer": "reviewer",
    }
    return mapping.get(source_type, "source")


# --------------------------------------------------
# PLAN BUILDER
# --------------------------------------------------

def build_plan(relative_path: str) -> dict[str, Any]:
    rules = load_rules()
    rule = find_rule(rules, relative_path)

    source_type = "unknown"
    trust = "unknown"
    aliases = []
    relationships = []
    concepts = []

    if rule:
        source_type = rule["classification"].get("source_type", "unknown")
        trust = rule["classification"].get("trust_level", "unknown")

        canonical = rule.get("canonical", {})
        aliases = canonical.get("aliases", [])
        concepts = canonical.get("core_concepts", [])

        rels = canonical.get("relationships", {})
        for k, v in rels.items():
            for item in v:
                relationships.append(f"{k}: {item}")

    title = normalize_title(relative_path, rule)
    prefix = map_source_type_to_prefix(source_type)

    canonical_id = build_canonical_id(prefix, title)

    return {
        "title": title,
        "canonical_id": canonical_id,
        "prefix": prefix,
        "source_type": source_type,
        "trust": trust,
        "aliases": aliases,
        "relationships": relationships,
        "concepts": concepts,
    }


# --------------------------------------------------
# PLAN COMMAND
# --------------------------------------------------

def run_canonicalize_plan_one(relative_path: str) -> int:
    plan = build_plan(relative_path)

    print("canonicalize-plan-one complete.")
    print(f"Title: {plan['title']}")
    print(f"ID: {plan['canonical_id']}")
    print(f"Type: {plan['source_type']}")
    print(f"Concepts: {plan['concepts']}")

    return 0


# --------------------------------------------------
# EXECUTION COMMAND
# --------------------------------------------------

def run_canonicalize_one(*, relative_markdown_path: str) -> int:
    repo_root = get_repo_root()

    source_path = repo_root / CONVERSION_LAYER_NAME / relative_markdown_path

    if not source_path.exists():
        print("ERROR: Source not found")
        return 1

    plan = build_plan(relative_markdown_path)

    target = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    target.mkdir(parents=True, exist_ok=True)

    filename = f"{slugify(plan['title'])}.md"
    target_file = target / filename

    lines = [
        "---",
        f"id: {plan['canonical_id']}",
        f"title: {plan['title']}",
        "page_type: source",
        f"trust_level: {plan['trust']}",
        "aliases:",
    ]

    if plan["aliases"]:
        for a in plan["aliases"]:
            lines.append(f"  - {a}")
    else:
        lines.append("  - none")

    lines.append("---\n")

    lines.append(f"# {plan['title']}\n")
    lines.append("## Related Concepts\n")

    if plan["concepts"]:
        for c in plan["concepts"]:
            lines.append(f"- concept-{slugify(c)}")
    else:
        lines.append("- none")

    target_file.write_text("\n".join(lines), encoding="utf-8")

    print("canonicalize-one complete.")
    print(f"Created: {target_file}")

    return 0