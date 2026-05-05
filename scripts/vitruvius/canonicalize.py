"""Canonical source-evidence artifact support.

Canonicalization remains the compatibility/provenance layer for source-derived
evidence records under the KG-first AEC-MEPFS direction. These helpers preserve
historical source IDs, governed write guards, and canonical storage paths; they
do not replace the authored backbone or authorize cleanup, KG reset, or live graph
promotion.
"""

from __future__ import annotations

import re
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .concept_matching import find_concepts_in_text, load_concept_term_map
from .constants import CONVERSION_LAYER_NAME
from .paths import get_repo_root
from .source_paths import logical_source_key_for_relative_path
from .utils import assert_windows_safe_path, slugify


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
    overlay_path = repo_root / "config" / "datasets" / "canonical_rules.generated.yaml"

    with open(path, "r", encoding="utf-8") as f:
        base_payload = yaml.safe_load(f) or {}

    if overlay_path.exists():
        with open(overlay_path, "r", encoding="utf-8") as f:
            overlay_payload = yaml.safe_load(f) or {}
        if isinstance(base_payload, dict) and isinstance(overlay_payload, dict):
            overlay_rules = overlay_payload.get("rules")
            if isinstance(overlay_rules, list) and overlay_rules:
                merged = dict(base_payload)
                base_rules = merged.get("rules")
                if not isinstance(base_rules, list):
                    base_rules = []
                merged["rules"] = [*base_rules, *overlay_rules]
                return merged

    return base_payload


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

def _clean_filename_stem(stem: str) -> str:
    """Turn '413839175-Taguig-CLUP-pdf' into 'Taguig CLUP'."""
    # Strip leading numeric tokens and common suffixes
    cleaned = re.sub(r"^\d+[-_]", "", stem)
    cleaned = re.sub(r"[-_](pdf|md|docx?|txt)$", "", cleaned, flags=re.IGNORECASE)
    cdp_match = re.fullmatch(r"(?i)cdp[-_ ]*(\d{4})[-_ ]*(\d{4})", cleaned.strip())
    if cdp_match:
        return f"Comprehensive Development Plan {cdp_match.group(1)} {cdp_match.group(2)}"
    # Replace remaining hyphens/underscores with spaces
    cleaned = cleaned.replace("-", " ").replace("_", " ")
    # Title-case each word
    return cleaned.title()


def extract_title_from_content(text: str, fallback: str) -> str:
    """Extract the document title from the first meaningful heading.

    Prefers H1, falls back to H2, then H3.  If no heading is found,
    returns the cleaned-up *fallback* stem.
    """
    fallback_title = _clean_filename_stem(fallback)
    # Look for ATX headings in the first 150 lines
    lines = text.splitlines()[:150]
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # H1: # Title
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            title = m.group(1).strip()
            return title if _is_valid_source_title(title) else fallback_title
        # H2: ## Title
        m = re.match(r"^##\s+(.+)$", line)
        if m and _is_valid_source_title(m.group(1).strip()):
            return m.group(1).strip()
        # H3: ### Title
        m = re.match(r"^###\s+(.+)$", line)
        if m and _is_valid_source_title(m.group(1).strip()):
            return m.group(1).strip()
    return fallback_title


def _is_valid_source_title(title: str) -> bool:
    cleaned = _clean_heading_title(title)
    title_slug = slugify(cleaned)
    alnum_count = sum(ch.isalnum() for ch in cleaned)
    if not title_slug or alnum_count < 3:
        return False
    generic_title_slugs = {
        "a",
        "acknowledgement",
        "acknowledgements",
        "acknowledgment",
        "acknowledgments",
        "annexes",
        "architecture",
        "berde",
        "clup",
        "contents",
        "department-of-health",
        "foreword",
        "list-of-figures",
        "list-of-tables",
        "m",
        "manual",
        "message",
        "n",
        "notes",
        "page",
        "preface",
        "sanitation",
        "table-of-contents",
        "untitled",
    }
    if title_slug in generic_title_slugs:
        return False
    if "http://" in cleaned.lower() or "https://" in cleaned.lower():
        return False
    if re.search(r"[.…]{4,}", cleaned) or re.search(r"\.{4,}", cleaned):
        return False
    if re.search(r"_{3,}", cleaned):
        return False
    if re.fullmatch(r"(?i)(pd|p\.d\.|bp|b\.p\.|ra|r\.a\.|no\.?)\s*[-.]?\s*[0-9a-z]+", cleaned):
        return False
    if re.fullmatch(r"(?i)cdp\s+\d{4}\s+\d{4}", cleaned):
        return False
    return True


def normalize_title(path: str, rule: dict | None) -> str:
    if rule and "canonical" in rule and "title" in rule["canonical"]:
        return rule["canonical"]["title"]

    return _clean_filename_stem(Path(path).stem)


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

    canonical_csv = (
        repo_root
        / "006_System-Manifests"
        / "registries"
        / "canonical_registry.csv"
    )
    existing_ids: set[str] = set()
    if canonical_csv.exists():
        with canonical_csv.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "canonical_id" in row and row["canonical_id"]:
                    existing_ids.add(row["canonical_id"])

    logical_source_key = logical_source_key_for_relative_path(relative_path)
    existing_canonical_id_for_source: str | None = None
    existing_sources_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    if existing_sources_dir.exists():
        for source_file in sorted(existing_sources_dir.glob("*.md")):
            text = source_file.read_text(encoding="utf-8", errors="ignore")
            if not text.startswith("---"):
                continue
            end = text.find("\n---", 3)
            if end == -1:
                continue
            try:
                fm = yaml.safe_load(text[3:end].strip())
            except yaml.YAMLError:
                continue
            if isinstance(fm, dict) and isinstance(fm.get("id"), str) and fm["id"]:
                existing_id = fm["id"]
                existing_ids.add(existing_id)
                existing_relative_path = fm.get("source_relative_markdown_path")
                if (
                    isinstance(existing_relative_path, str)
                    and logical_source_key_for_relative_path(existing_relative_path) == logical_source_key
                    and existing_canonical_id_for_source is None
                ):
                    existing_canonical_id_for_source = existing_id

    validate_prefix(prefix)
    if existing_canonical_id_for_source:
        canonical_id = existing_canonical_id_for_source
    else:
        canonical_id = resolve_canonical_id(
            prefix=prefix,
            slug=slugify(title),
            source_path=logical_source_key,
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

def _is_noise_heading(title: str) -> bool:
    lowered = title.lower()
    if 'http://' in lowered or 'https://' in lowered:
        return True
    if lowered.startswith('govph'):
        return True
    if 'implementing rules and regulations' in lowered and not lowered.startswith(('rule ', 'section ')):
        return True
    if 'rules and standards for economic and socialized housing projects' in lowered:
        return True
    if lowered in {'message', 'list of tables', 'annexes', 'page'}:
        return True
    if lowered.startswith('figure ') or lowered.startswith('fig. '):
        return True
    if lowered.startswith('table '):
        return True
    if 'working group' in lowered or 'director' in lowered or 'secretary' in lowered or '(ret)' in lowered:
        return True
    if lowered.startswith(('arch ', 'csupt ', 'ssupt ', 'usec ', 'director ')):
        return True
    if 'national council on disability affairs' in lowered or 'pambansang sanggunian' in lowered:
        return True
    if re.search(r"\b(viewing distance|size of symbol|character proportion|finish and contrast)\b", lowered):
        return True
    compact = re.sub(r"[^a-z0-9]+", " ", lowered).strip()
    if compact.startswith(('section ', 'rule ', 'chapter ', 'division ', 'appendix ', 'annex ', 'part ')):
        return False
    if re.match(r'^\d+\s', compact):
        return False
    if '. ' in title and any(ch.islower() for ch in title):
        return True
    if title.endswith(('that are', 'the following:', 'the following')):
        return True
    if title.isupper() and len(title.split()) <= 6:
        return True
    return False


def _looks_like_toc_heading(title: str) -> bool:
    return '....' in title or bool(re.search(r"\s+\d+$", title))


def _looks_like_numbered_heading_title(title: str) -> bool:
    body = re.sub(r"^\d+\.\s*", "", title).strip()
    if len(body.split()) > 8:
        return False
    if body.endswith(('.', ';', ':')):
        return False
    if any(ch.islower() for ch in body) and body[0].islower():
        return False
    return True


def _looks_like_headingish_line(stripped: str) -> bool:
    lowered = stripped.lower()
    if stripped.startswith('- ') and re.search(r'\b(section|rule|chapter|division|appendix|annex|part|table|figure|annexes|list of tables)\b', lowered):
        return True
    if re.match(r'^(rule|section|chapter|division|appendix|annex|part)\b', lowered):
        return True
    return False


def _is_structural_heading(title: str) -> bool:
    lowered = title.lower().strip()
    if re.match(r'^(rule|section|chapter|division|appendix|annex|part)\b', lowered):
        return True
    if re.match(r'^\d+\.\s+', title):
        return True
    return False

def _clean_heading_title(title: str) -> str:
    cleaned = title.strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'([A-Z0-9])([A-Z][a-z])', r'\1 \2', cleaned)
    cleaned = re.sub(r'(Section\s\d[\d.]*)([A-Z])', r'\1 \2', cleaned)
    cleaned = re.sub(r'(SECTION\s\d[\d.]*)([A-Z])', r'\1 \2', cleaned)
    cleaned = re.sub(r'(?i)(Sources)(The\b)', r'\1 \2', cleaned)
    cleaned = re.sub(r'(?i)(Functions)(The\b)', r'\1 \2', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


# Compiled once — used by extract_section_headers for plain-text heading detection.
_PLAIN_HEADER_PATTERN_1 = re.compile(
    r"^(RULE|SECTION|CHAPTER|DIVISION|APPENDIX|ANNEX|PART)\b[ .:-]*(.*)$",
    re.IGNORECASE,
)
_PLAIN_HEADER_PATTERN_2 = re.compile(r"^(\d+)\.\s+(.+)$")


def extract_section_headers(markdown_text: str) -> list[dict]:
    headers = []
    seen = set()
    plain_patterns = [_PLAIN_HEADER_PATTERN_1, _PLAIN_HEADER_PATTERN_2]
    for line in markdown_text.splitlines():
        stripped = line.strip()
        title = None
        level = None
        numbered = False
        match = re.match(r"^(#{2,6})\s+(.+?)$", stripped)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
        elif stripped and not stripped.startswith(('-', '*', '|', '![')):
            for pattern in plain_patterns:
                m = pattern.match(stripped)
                if m:
                    title = stripped
                    level = 2
                    numbered = pattern is plain_patterns[1]
                    break
        if title is None:
            continue
        structural = _is_structural_heading(title)
        if numbered and not _looks_like_numbered_heading_title(title):
            continue
        title = _clean_heading_title(title)
        if len(title) < 4 or _looks_like_toc_heading(title) or _is_noise_heading(title):
            continue
        key = (level, title)
        if key in seen:
            continue
        seen.add(key)
        headers.append({"level": level, "title": title})
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
                sentence = _clean_candidate_text(" ".join(current).split(". ")[0])
                if sentence:
                    points.append(sentence[:300].rstrip(".") + ".")
            current = []
            collecting = True
            continue
        if collecting and _is_useful_text_line(stripped):
            current.append(stripped)

    if current:
        sentence = _clean_candidate_text(" ".join(current).split(". ")[0])
        if sentence:
            points.append(sentence[:300].rstrip(".") + ".")

    return points[:limit]


def _looks_like_sentence(text: str) -> bool:
    if len(text.split()) < 8:
        return False
    if re.search(r"\b\d+\s*-\s*\d+\b", text):
        return False
    lowered = text.lower()
    if re.match(r"^(rule|section|chapter|division|appendix|annex|part|table|figure)\b", lowered):
        return False
    if any(ch.islower() for ch in text):
        return True
    if text.endswith(('.', ':', ';')):
        return True
    return False


def build_overview_paragraph(markdown_text: str) -> str:
    fallback = ""
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not _is_useful_text_line(stripped):
            continue
        if _looks_like_headingish_line(stripped):
            continue
        cleaned = _clean_candidate_text(stripped[:500])
        if fallback == "" and not re.search(r"\b\d+\s*-\s*\d+\b", cleaned):
            fallback = cleaned
        if _looks_like_sentence(cleaned):
            return cleaned
    return _clean_candidate_text(fallback)


def _is_useful_text_line(stripped: str) -> bool:
    if not stripped or stripped.startswith("#"):
        return False
    if stripped.startswith("!["):
        return False
    if stripped.startswith("|") and stripped.endswith("|"):
        return False
    lowered = stripped.lower()
    if "isbn " in lowered or lowered.startswith("isbn"):
        return False
    if "http://" in lowered or "https://" in lowered:
        return False
    if lowered.startswith("govph"):
        return False
    if "total registeredpersons withdisabilities" in lowered:
        return False
    if lowered in {"page", "downloadable files:", "list of tables", "annexes"}:
        return False
    if "table of contents" in lowered:
        return False
    if re.search(r"[.…]{4,}", stripped) or re.search(r"\.{4,}", stripped):
        return False
    page_ranges = re.findall(r"\b\d+\s*-\s*\d+\b", stripped)
    if len(page_ranges) >= 2:
        return False
    letters = [ch for ch in stripped if ch.isalpha()]
    if letters and page_ranges:
        uppercase_ratio = sum(ch.isupper() for ch in letters) / len(letters)
        if uppercase_ratio > 0.6:
            return False
    if stripped.isupper() and len(stripped.split()) <= 6:
        return False
    return True


def _clean_candidate_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^(?:[-*•·]+\s*)+", "", cleaned)
    cleaned = re.sub(r"^([A-Za-z])\s+(?=[a-z])", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def _summary_hygiene_flags(markdown_text: str) -> list[str]:
    lines = [line.strip() for line in markdown_text.splitlines() if line.strip()]
    first_window = lines[:160]
    lowered_window = [line.lower() for line in first_window]
    flags: list[str] = []
    if any("table of contents" in line for line in lowered_window):
        flags.append("table_of_contents_front_matter")
    if any(line in {"|preface|", "|message|"} for line in lowered_window):
        flags.append("preface_or_message_front_matter")
    if any("foreword" in line or "acknowledgement" in line for line in lowered_window):
        flags.append("preface_or_message_front_matter")
    if any("memorandum circular" in line for line in lowered_window):
        flags.append("administrative_front_matter")
    if sum(1 for line in first_window if line.startswith("![")) >= 3:
        flags.append("image_heavy_front_matter")
    if sum(1 for line in first_window if line.startswith("|") and line.endswith("|")) >= 6:
        flags.append("table_heavy_front_matter")
    return list(dict.fromkeys(flags))


def _summary_should_be_withheld(markdown_text: str) -> bool:
    lines = [line.strip() for line in markdown_text.splitlines() if line.strip()]
    image_lines = [line for line in lines if line.startswith("![")]
    table_lines = [line for line in lines if line.startswith("|") and line.endswith("|")]
    noise_lines = [
        line for line in lines
        if (
            "http://" in line.lower()
            or "https://" in line.lower()
            or "isbn" in line.lower()
            or "table of contents" in line.lower()
            or line.lower().startswith("govph")
        )
    ]
    useful_lines = [
        line for line in lines
        if line not in image_lines and line not in table_lines and line not in noise_lines
    ]
    useful_ratio = (len(useful_lines) / len(lines)) if lines else 0.0
    return useful_ratio < 0.6 or len(image_lines) > 500 or len(table_lines) > 800


def _summary_withheld_notice(title: str, markdown_text: str) -> str:
    flag_phrases = {
        "table_of_contents_front_matter": "table-of-contents material",
        "preface_or_message_front_matter": "preface/message prose",
        "administrative_front_matter": "administrative front matter",
        "image_heavy_front_matter": "image-heavy extraction",
        "table_heavy_front_matter": "table-heavy extraction",
    }
    reasons = [
        flag_phrases[flag]
        for flag in _summary_hygiene_flags(markdown_text)
        if flag in flag_phrases
    ]
    reason_text = ", ".join(reasons) if reasons else "extraction-difficulty signals"
    return (
        f"Automated summary withheld for {title} because the refined source includes "
        f"{reason_text}. Review the Coverage headings and authoritative benchmark/reference "
        "sources before relying on summary prose."
    )


def _concept_title_from_slug(concept_slug: str) -> str:
    return concept_slug.replace("-", " ")


def resolve_referenced_concepts(body: str, *, repo_root: Path) -> list[str]:
    concepts_dir = Path(repo_root) / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    if not concepts_dir.exists():
        return []
    concept_map = load_concept_term_map(concepts_dir)
    return find_concepts_in_text(body, concept_map)


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

    # Override the filename-derived title with an actual heading from the
    # document content whenever possible.
    plan["title"] = extract_title_from_content(refined_text, plan["title"])

    headers = extract_section_headers(refined_text)
    structural_headers = [h for h in headers if _is_structural_heading(h["title"])]
    if structural_headers:
        headers = structural_headers
    summary_withheld = _summary_should_be_withheld(refined_text)
    key_points = [] if summary_withheld else extract_key_points(refined_text, limit=5)
    overview = (
        _summary_withheld_notice(plan["title"], refined_text)
        if summary_withheld
        else build_overview_paragraph(refined_text)
    )
    referenced = resolve_referenced_concepts(refined_text, repo_root=repo_root)

    frontmatter: dict[str, Any] = {
        "id": plan["canonical_id"],
        "title": plan["title"],
        "page_type": "source",
        "trust_level": plan["trust"],
        "canonical_status": "draft",
        "source_relative_markdown_path": relative_markdown_path,
        "last_canonicalized_utc": datetime.now(timezone.utc).isoformat(),
    }
    if plan["aliases"]:
        frontmatter["aliases"] = list(plan["aliases"])

    frontmatter_block = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=1000000,
    ).rstrip()

    lines = [
        "---",
        frontmatter_block,
        "---",
    ]
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
        if summary_withheld:
            lines.append("- (automated key points withheld because source-summary trust is low; review operative sections directly)")
        else:
            lines.append("- (no key points extracted)")
    lines.append("")
    lines.append("## Referenced Concepts")
    lines.append("")
    for ref in referenced:
        lines.append(f"- {ref}")
    if not referenced:
        lines.append("- (none resolved against shared/concepts)")
    lines.append("")
    lines.append("## Source Text")
    lines.append("")
    source_body = refined_text.rstrip()
    lines.append(source_body if source_body else "(source text empty)")
    lines.append("")

    target = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    target.mkdir(parents=True, exist_ok=True)
    stem = slugify(plan["title"])
    # Windows MAX_PATH is 260; truncate aggressively to stay well under it
    # even when nested under long repo paths.
    MAX_FILENAME_LEN = 160
    if len(stem) > MAX_FILENAME_LEN - 3:
        stem = stem[: MAX_FILENAME_LEN - 3].rstrip("-")
    filename = f"{stem}.md"
    target_file = target / filename
    if target_file.exists():
        existing_text = target_file.read_text(encoding="utf-8", errors="ignore")
        existing_source_relative_markdown_path = None
        if existing_text.startswith("---"):
            end = existing_text.find("\n---", 3)
            if end != -1:
                try:
                    existing_fm = yaml.safe_load(existing_text[3:end].strip())
                except yaml.YAMLError:
                    existing_fm = None
                if isinstance(existing_fm, dict):
                    existing_source_relative_markdown_path = existing_fm.get("source_relative_markdown_path")
        if (
            isinstance(existing_source_relative_markdown_path, str)
            and existing_source_relative_markdown_path
            and existing_source_relative_markdown_path != relative_markdown_path
            and logical_source_key_for_relative_path(existing_source_relative_markdown_path)
            != logical_source_key_for_relative_path(relative_markdown_path)
        ):
            target_file = target / f"{plan['canonical_id']}.md"
    assert_windows_safe_path(target_file, what="canonical source output path")
    return target_file, "\n".join(lines)


def run_canonicalize_one(*, relative_markdown_path: str, force: bool = False) -> int:
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

    decision = should_overwrite(target_file, content, force=force)
    if not decision.allowed:
        print(f"SKIP ({decision.reason}): {target_file}")
        return 0

    target_file.write_text(content, encoding="utf-8")
    print(f"canonicalize-one complete. Wrote: {target_file}")
    return 0


def run_canonicalize() -> int:
    """Walk raw markdown paths and canonicalize matching refined markdown when available."""
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
        preferred_rel = rel
        raw_index = parts.index("raw_markdown")
        refined_parts = list(parts)
        refined_parts[raw_index] = "refined_markdown"
        refined_rel = Path(*refined_parts)
        if (conversion_root / refined_rel).exists():
            preferred_rel = refined_rel.as_posix()
        try:
            rc = run_canonicalize_one(relative_markdown_path=preferred_rel)
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
