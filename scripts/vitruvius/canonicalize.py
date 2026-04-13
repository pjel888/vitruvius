from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .constants import CONVERSION_LAYER_NAME
from .paths import ensure_runs_dir, get_repo_root
from .reports import write_json, write_text
from .utils import safe_name_for_report, utc_now_stamp


SUPPORTED_PLAN_EXTENSIONS = {".md"}


# --------------------------------------------------
# LOAD RULES
# --------------------------------------------------

def load_rules() -> dict[str, Any]:
    repo_root = get_repo_root()
    rules_path = repo_root / "scripts" / "vitruvius" / "rules" / "canonical_rules.yaml"

    if not rules_path.exists():
        raise FileNotFoundError(f"canonical_rules.yaml not found at {rules_path}")

    with open(rules_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# --------------------------------------------------
# MATCHING ENGINE
# --------------------------------------------------

def matches_rule(rule: dict[str, Any], path: str) -> bool:
    path_lower = path.lower()
    match = rule.get("match", {})

    all_contains = match.get("all_contains", [])
    any_contains = match.get("any_contains", [])
    not_contains = match.get("not_contains", [])

    if any(term not in path_lower for term in all_contains):
        return False

    if any_contains and not any(term in path_lower for term in any_contains):
        return False

    if any(term in path_lower for term in not_contains):
        return False

    return True


def find_matching_rule(rules: dict[str, Any], path: str) -> dict[str, Any] | None:
    for rule in rules.get("rules", []):
        if matches_rule(rule, path):
            return rule
    return None


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def slugify(value: str) -> str:
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def normalize_title(path: str, rule: dict[str, Any] | None) -> str:
    stem = Path(path).stem.strip()

    if rule:
        canonical = rule.get("canonical", {})
        if "title" in canonical:
            return canonical["title"]

    return re.sub(r"\s+", " ", stem).strip(" -_")


def build_canonical_id(source_type: str, title: str) -> str:
    return f"{source_type}-{slugify(title)}"


def build_source_page_path(title: str) -> str:
    return f"003_Canonical-Knowledge-Layer/shared/sources/{slugify(title)}.md"


def build_concept_page_path(concept: str) -> str:
    return f"003_Canonical-Knowledge-Layer/shared/concepts/{slugify(concept)}.md"


def build_raw_source_document_path(relative_markdown_path: str) -> str:
    parts = Path(relative_markdown_path).parts
    if len(parts) < 3:
        return Path(relative_markdown_path).with_suffix(".pdf").as_posix()

    category = parts[0]
    nested_parts = parts[2:-1]
    filename = Path(parts[-1]).with_suffix(".pdf").name

    raw_doc_path = Path(category)
    if nested_parts:
        raw_doc_path = raw_doc_path.joinpath(*nested_parts)
    raw_doc_path = raw_doc_path / filename

    return raw_doc_path.as_posix()


# --------------------------------------------------
# PLAN BUILDER
# --------------------------------------------------

def build_plan(relative_markdown_path: str) -> dict[str, Any]:
    rules = load_rules()
    rule = find_matching_rule(rules, relative_markdown_path)

    source_type = "unknown"
    trust_level = "unknown"
    aliases: list[str] = []
    relationships: list[str] = []
    core_concepts: list[str] = []

    if rule:
        classification = rule.get("classification", {})
        source_type = classification.get("source_type", "unknown")
        trust_level = classification.get("trust_level", "unknown")

        canonical = rule.get("canonical", {})
        aliases = canonical.get("aliases", [])
        core_concepts = canonical.get("core_concepts", [])

        rels = canonical.get("relationships", {})
        for key, values in rels.items():
            for v in values:
                relationships.append(f"{key}: {v}")

    title = normalize_title(relative_markdown_path, rule)
    canonical_id = build_canonical_id(source_type, title)
    category = Path(relative_markdown_path).parts[0]

    outputs = [
        {
            "page_type": "source",
            "target_path": build_source_page_path(title),
        }
    ]

    for concept in core_concepts:
        outputs.append(
            {
                "page_type": "concept",
                "target_path": build_concept_page_path(concept),
                "concept_name": concept,
            }
        )

    return {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": {
            "relative_markdown_path": relative_markdown_path,
        },
        "classification": {
            "source_type": source_type,
            "trust_level": trust_level,
        },
        "normalized": {
            "title": title,
            "canonical_id": canonical_id,
            "category": category,
            "aliases": aliases,
            "relationships": relationships,
            "core_concepts": core_concepts,
        },
        "proposed_outputs": outputs,
    }


# --------------------------------------------------
# MARKDOWN GENERATION
# --------------------------------------------------

def build_source_page_markdown(plan: dict[str, Any], source_text: str) -> str:
    title = plan["normalized"]["title"]
    canonical_id = plan["normalized"]["canonical_id"]
    category = plan["normalized"]["category"]
    aliases = plan["normalized"]["aliases"]
    relationships = plan["normalized"]["relationships"]
    core_concepts = plan["normalized"]["core_concepts"]
    trust_level = plan["classification"]["trust_level"]

    raw_doc = build_raw_source_document_path(plan["input"]["relative_markdown_path"])

    frontmatter = [
        "---",
        f"id: {canonical_id}",
        f"title: {title}",
        "page_type: source",
        f"category: {category}",
        "aliases:",
    ]

    if aliases:
        for a in aliases:
            frontmatter.append(f"  - {a}")
    else:
        frontmatter.append("  - none")

    frontmatter.extend([
        "source_documents:",
        f"  - {raw_doc}",
        f"trust_level: {trust_level}",
        "canonical_status: draft",
        f"last_canonicalized_utc: {datetime.now(timezone.utc).isoformat()}",
        "relationships:",
    ])

    if relationships:
        for r in relationships:
            frontmatter.append(f"  - {r}")
    else:
        frontmatter.append("  - none")

    frontmatter.append("---\n")

    body = [
        f"# {title}",
        "",
        "## Overview",
        "",
        f"{title} is a canonical source under the Vitruvius system.",
        "",
        "## Related Concepts",
        "",
    ]

    if core_concepts:
        for c in core_concepts:
            body.append(f"- {c}")
    else:
        body.append("- none")

    return "\n".join(frontmatter + body)


# --------------------------------------------------
# COMMANDS
# --------------------------------------------------

def run_canonicalize_plan_one(relative_markdown_path: str) -> int:
    plan = build_plan(relative_markdown_path)

    print("Canonicalize-plan-one complete.")
    print(f"Type: {plan['classification']['source_type']}")
    print(f"Title: {plan['normalized']['title']}")

    return 0


def run_canonicalize_one(relative_markdown_path: str) -> int:
    repo_root = get_repo_root()

    source_path = repo_root / CONVERSION_LAYER_NAME / relative_markdown_path

    if not source_path.exists():
        print("ERROR: Source not found")
        return 1

    plan = build_plan(relative_markdown_path)
    source_text = source_path.read_text(encoding="utf-8", errors="ignore")

    source_output = next(
        item for item in plan["proposed_outputs"] if item["page_type"] == "source"
    )

    target_path = repo_root / source_output["target_path"]
    target_path.parent.mkdir(parents=True, exist_ok=True)

    md = build_source_page_markdown(plan, source_text)
    target_path.write_text(md, encoding="utf-8")

    print("Canonicalize-one complete.")
    print(f"Created: {target_path}")

    return 0