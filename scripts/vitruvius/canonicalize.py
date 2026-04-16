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

    # Sprint CLEANUP-1 C1.2 — optional collision-resolving canonical ID build.
    # Gated behind `p1c_slug_collision_policy`. When off, retain legacy
    # `build_canonical_id()` behaviour (silent overwrite on collision).
    # Perf call: cold path (once per canonicalize run), sub-ms hash + dict
    # lookup; above the Rust Line per AD-036.
    try:
        from .spatial._feature_gate import _load_features_cached
        _features = _load_features_cached()
    except Exception:
        _features = None

    if _features is not None and _features.is_enabled("p1c_slug_collision_policy"):
        from .collision_resolver import SlugAliasRegistry, resolve_canonical_id

        repo_root = get_repo_root()
        registry_path = (
            repo_root
            / "scripts"
            / "vitruvius"
            / "rules"
            / "slug_alias_registry.yaml"
        )
        registry = SlugAliasRegistry.load(registry_path)

        # Load existing ids from canonical_registry.csv if it exists.
        canonical_csv = (
            repo_root
            / "006_System-Manifests"
            / "registries"
            / "canonical_registry.csv"
        )
        existing_ids: set[str] = set()
        if canonical_csv.exists():
            import csv

            with canonical_csv.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "canonical_id" in row and row["canonical_id"]:
                        existing_ids.add(row["canonical_id"])

        validate_prefix(prefix)
        canonical_id = resolve_canonical_id(
            prefix=prefix,
            slug=slugify(title),
            source_path=str(relative_path),
            existing_ids=existing_ids,
            registry=registry,
        )
        registry.save()

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

def run_canonicalize_plan_one(
    relative_path: str | None = None,
    *,
    relative_markdown_path: str | None = None,
) -> int:
    path = relative_markdown_path or relative_path
    if path is None:
        raise TypeError("run_canonicalize_plan_one requires a markdown path")
    plan = build_plan(path)

    print("canonicalize-plan-one complete.")
    print(f"Title: {plan['title']}")
    print(f"ID: {plan['canonical_id']}")
    print(f"Type: {plan['source_type']}")
    print(f"Concepts: {plan['concepts']}")

    return 0


# --------------------------------------------------
# EXECUTION COMMAND
# --------------------------------------------------

def extract_section_headers(markdown_text: str) -> list[dict]:
    headers = []
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            title = stripped[3:].strip()
            if len(title) < 4:
                continue
            headers.append({"level": 2, "title": title})
        elif stripped.startswith("### "):
            title = stripped[4:].strip()
            if len(title) < 4:
                continue
            headers.append({"level": 3, "title": title})
    return headers


def extract_key_points(markdown_text: str, *, limit: int = 5) -> list[str]:
    """Pick short, standalone assertions: first sentence after each H2 that is
    not itself a header, trimmed to 300 chars."""
    points: list[str] = []
    current: list[str] = []
    collecting = False

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            if current:
                sentence = " ".join(current).split(". ")[0].strip()
                if sentence:
                    points.append(sentence[:300].rstrip(".") + ".")
            current = []
            collecting = True
            continue
        if collecting and _is_useful_text_line(stripped):
            current.append(stripped)

    if current:
        sentence = " ".join(current).split(". ")[0].strip()
        if sentence:
            points.append(sentence[:300].rstrip(".") + ".")

    return points[:limit]


def build_overview_paragraph(markdown_text: str) -> str:
    fallback = ""
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not _is_useful_text_line(stripped):
            continue
        if fallback == "":
            fallback = stripped[:500]
        if len(stripped.split()) >= 8:
            return stripped[:500]
    return fallback


def _is_useful_text_line(stripped: str) -> bool:
    if not stripped or stripped.startswith("#"):
        return False
    if stripped.startswith("!["):
        return False
    if stripped.startswith("|") and stripped.endswith("|"):
        return False
    return True


def _concept_title_from_slug(concept_slug: str) -> str:
    return concept_slug.replace("-", " ")


def resolve_referenced_concepts(body: str, *, repo_root: Path) -> list[str]:
    concepts_dir = Path(repo_root) / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    if not concepts_dir.exists():
        return []

    body_lower = body.lower()
    found: list[str] = []
    for md in sorted(concepts_dir.glob("*.md")):
        slug = md.stem
        spaced = slug.replace("-", " ")
        hyphenated = slug  # already hyphenated
        # Also check mixed forms where some words are hyphenated in body
        # but separated by spaces in others, e.g., "fire-resistive construction".
        # Simple heuristic: replace spaces in body with normalized separator,
        # then check if either spaced or hyphenated form appears.
        body_normalized = body_lower.replace("-", " ")
        if spaced in body_lower or hyphenated in body_lower or spaced in body_normalized:
            found.append(f"concept-{slug}")

    return found


def build_structured_source_file(
    *,
    repo_root: Path,
    relative_markdown_path: str,
) -> tuple[Path, str]:
    """Build the full canonical source markdown for one refined input.

    Returns the target path and the rendered content (the caller decides
    whether to write via canonical_diff.should_overwrite).
    """
    source_path = repo_root / CONVERSION_LAYER_NAME / relative_markdown_path
    if not source_path.exists():
        raise FileNotFoundError(f"Refined markdown not found: {source_path}")

    refined_text = source_path.read_text(encoding="utf-8")
    plan = build_plan(relative_markdown_path)

    headers = extract_section_headers(refined_text)
    key_points = extract_key_points(refined_text, limit=5)
    overview = build_overview_paragraph(refined_text)
    referenced = resolve_referenced_concepts(refined_text, repo_root=repo_root)

    lines = [
        "---",
        f"id: {plan['canonical_id']}",
        f"title: {plan['title']}",
        "page_type: source",
        f"trust_level: {plan['trust']}",
        "canonical_status: draft",
        f"last_canonicalized_utc: {datetime.now(timezone.utc).isoformat()}",
    ]
    if plan["aliases"]:
        lines.append("aliases:")
        for a in plan["aliases"]:
            lines.append(f"  - {a}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {plan['title']}")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(overview or f"{plan['title']} is a canonical source within the Vitruvius system.")
    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    for h in headers:
        lines.append(f"- {h['title']}")
    if not headers:
        lines.append("- (no headers detected in refined source)")
    lines.append("")
    lines.append("## Key Points")
    lines.append("")
    for kp in key_points:
        lines.append(f"- {kp}")
    if not key_points:
        lines.append("- (no key points extracted)")
    lines.append("")
    lines.append("## Referenced Concepts")
    lines.append("")
    for ref in referenced:
        lines.append(f"- {ref}")
    if not referenced:
        lines.append("- (none resolved against shared/concepts)")
    lines.append("")

    target = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    target.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(plan['title'])}.md"
    target_file = target / filename
    return target_file, "\n".join(lines)


def run_canonicalize_one(*, relative_markdown_path: str) -> int:
    from .canonical_diff import should_overwrite

    repo_root = get_repo_root()
    try:
        target_file, content = build_structured_source_file(
            repo_root=repo_root,
            relative_markdown_path=relative_markdown_path,
        )
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    decision = should_overwrite(target_file, content)
    if not decision.allowed:
        print(f"SKIP ({decision.reason}): {target_file}")
        return 0

    target_file.write_text(content, encoding="utf-8")
    print(f"canonicalize-one complete. Wrote: {target_file}")
    return 0


def run_canonicalize() -> int:
    """Walk 002_Raw-Conversion-Layer/*/raw_markdown/**/*.md and canonicalize each."""
    repo_root = get_repo_root()
    conversion_root = repo_root / CONVERSION_LAYER_NAME
    if not conversion_root.exists():
        print("No conversion layer found.")
        return 0

    processed = 0
    skipped = 0
    failed = 0
    for md_path in sorted(conversion_root.rglob("*.md")):
        rel = md_path.relative_to(conversion_root).as_posix()
        # Prefer refined markdown when available; fall back to raw.
        parts = Path(rel).parts
        if "raw_markdown" not in parts:
            continue
        try:
            rc = run_canonicalize_one(relative_markdown_path=rel)
        except Exception as exc:
            print(f"FAIL ({exc}): {rel}")
            failed += 1
            continue
        if rc == 0:
            processed += 1
        else:
            skipped += 1

    print(f"canonicalize (batch) complete. Processed: {processed}, Skipped: {skipped}, Failed: {failed}")
    return 0
