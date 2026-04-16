"""Concept enrichment orchestrator (Phase 3C Task 3).

Promotes placeholder concept files to enriched Knowledge Nodes by composing
the deterministic definition extractor and alias miner. Zero LLM calls.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .canonical_diff import should_overwrite
from .concept_aliases import mine_aliases_for_concept
from .concept_definitions import (
    DefinitionCandidate,
    extract_definitions_from_sections,
    extract_definitions_from_text,
    pick_best_definition,
)
from .paths import get_repo_root
from .source_identity import canonical_source_id_for_relative_path


_ENRICHABLE_STATUSES = {"placeholder", "draft", "unknown"}


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    try:
        fm = yaml.safe_load(text[3:end].strip()) or {}
    except yaml.YAMLError:
        fm = {}
    body_start = end + 4
    while body_start < len(text) and text[body_start] in "\n":
        body_start += 1
    return fm, text[body_start:]


def _collect_source_texts(repo_root: Path) -> list[tuple[str, str]]:
    """Return a list of (source_id, text) pairs to scan for definitions."""
    out: list[tuple[str, str]] = []

    refined_root = repo_root / "002_Raw-Conversion-Layer"
    if refined_root.exists():
        for md in refined_root.rglob("*.md"):
            if "refined_markdown" not in md.parts:
                continue
            try:
                rel = str(md.relative_to(refined_root))
                out.append((
                    canonical_source_id_for_relative_path(rel),
                    md.read_text(encoding="utf-8"),
                ))
            except Exception:
                continue

    sources_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    if sources_dir.exists():
        for md in sources_dir.glob("*.md"):
            try:
                text = md.read_text(encoding="utf-8")
                fm, body = _parse_frontmatter(text)
                source_id = fm.get("id") or md.stem
                out.append((source_id, body))
            except Exception:
                continue

    return out


def _collect_known_slugs(repo_root: Path) -> set[str]:
    concepts_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    if not concepts_dir.exists():
        return set()
    return {p.stem for p in concepts_dir.glob("*.md")}


def _render_enriched(
    *,
    existing_frontmatter: dict,
    definition: DefinitionCandidate,
    aliases: list[str],
) -> str:
    """Render the enriched concept file content (frontmatter + body)."""
    now = datetime.now(timezone.utc).isoformat()

    fm = dict(existing_frontmatter)
    fm["canonical_status"] = "enriched"
    fm["concept_status"] = "enriched"
    fm["last_canonicalized_utc"] = now
    fm["enriched_at_utc"] = now
    fm["regulatory_basis"] = [
        {
            "source_id": definition.source_id,
            "section_id": definition.source_section_id or "unknown",
            "evidence_snippet": definition.snippet[:500],
        }
    ]
    # Always clear stale aliases first — a prior enrichment pass may have
    # written noisy ones that the new mining rules would not produce. Only
    # set the key if we have fresh aliases to record.
    fm.pop("aliases", None)
    if aliases:
        fm["aliases"] = aliases

    # Sprint CLEANUP-1 C2.2 — optional bidirectional concept cross-refs.
    # Flag-off is byte-identical: the block below only mutates `fm` when
    # `p3_bidirectional_refs` is enabled AND relationship files exist for
    # the current concept id. Any failure is swallowed to preserve
    # flag-off byte-identity guarantees.
    try:
        from .spatial._feature_gate import _load_features_cached
        _features_xref = _load_features_cached()
    except Exception:
        _features_xref = None

    if _features_xref is not None and _features_xref.is_enabled("p3_bidirectional_refs"):
        try:
            from .concept_cross_ref import build_concept_cross_ref_map

            _xref_repo_root = get_repo_root()
            _xref_rels_dir = (
                _xref_repo_root
                / "003_Canonical-Knowledge-Layer"
                / "shared"
                / "relationships"
            )
            if _xref_rels_dir.exists():
                _xref_map = build_concept_cross_ref_map(_xref_rels_dir)
                _concept_id = fm.get("id")
                if isinstance(_concept_id, str):
                    _related = _xref_map.get(_concept_id, [])
                    if _related:
                        fm["related_concepts"] = _related
        except Exception:
            pass  # graceful degrade — flag-off byte-identity preserved

    ordered_keys = [
        "id", "title", "page_type",
        "canonical_status", "concept_status",
        "last_canonicalized_utc", "enriched_at_utc",
        "aliases",
        "related_concepts",
        "regulatory_basis",
    ]
    ordered: dict[str, Any] = {}
    for k in ordered_keys:
        if k in fm:
            ordered[k] = fm[k]
    for k, v in fm.items():
        if k not in ordered:
            ordered[k] = v

    yaml_text = yaml.safe_dump(
        ordered,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=1000000,
    )

    title = fm.get("title", fm.get("id", "Concept"))
    definition_text = definition.snippet.strip()

    body_lines = [
        "---",
        yaml_text.rstrip(),
        "---",
        "",
        f"# {title}",
        "",
        "## Definition",
        "",
        definition_text,
        "",
        "## Regulatory Basis",
        "",
        f"- **[{definition.source_id}]({definition.source_id})** - Section {definition.source_section_id or 'unknown'}: \"{definition.snippet[:200].strip()}...\"",
        "",
    ]
    return "\n".join(body_lines)


def enrich_concept_inner(
    *,
    concept_slug: str,
    repo_root: Path,
    force: bool = False,
) -> dict[str, Any]:
    """Enrich a single concept file."""
    concept_path = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts" / f"{concept_slug}.md"
    if not concept_path.exists():
        return {
            "concept_slug": concept_slug,
            "enriched": False,
            "reason": "concept_file_not_found",
        }

    existing_text = concept_path.read_text(encoding="utf-8")
    existing_fm, _existing_body = _parse_frontmatter(existing_text)

    status = existing_fm.get("canonical_status", "unknown")
    if not force and status not in _ENRICHABLE_STATUSES:
        return {
            "concept_slug": concept_slug,
            "enriched": False,
            "reason": f"already_enriched (canonical_status={status})",
        }

    known_slugs = _collect_known_slugs(repo_root)
    all_candidates: list[DefinitionCandidate] = []

    # Sprint CLEANUP-1 C2.1 — optional density-based extractor (flag-gated).
    # Flag-off is byte-identical: the `_density_on` short-circuit keeps the
    # inner loop identical to the pre-C2.1 version.
    _density_on = False
    try:
        from .spatial._feature_gate import _load_features_cached
        _features = _load_features_cached()
        if _features is not None and _features.is_enabled("p3_density_extractor"):
            _density_on = True
    except Exception:
        _features = None

    for source_id, text in _collect_source_texts(repo_root):
        anchor_cands = extract_definitions_from_text(
            text, source_id=source_id, known_slugs=known_slugs,
        )
        section_cands = extract_definitions_from_sections(
            text, source_id=source_id, known_slugs=known_slugs,
        )
        all_candidates.extend(c for c in anchor_cands if c.concept_slug == concept_slug)
        all_candidates.extend(c for c in section_cands if c.concept_slug == concept_slug)

        # Sprint CLEANUP-1 C2.1 — density extractor plugged here
        if _density_on:
            try:
                from .concepts.density_extractor import (
                    extract_definitions_by_density,
                )

                # Minimal alias set: the slug itself and its space-separated
                # form. Full alias mining runs later from the picked snippet;
                # the density pass only needs seed terms to find paragraphs.
                _density_aliases = [
                    concept_slug,
                    concept_slug.replace("-", " "),
                ]
                density_cands = extract_definitions_by_density(
                    text=text,
                    slug=concept_slug,
                    aliases=_density_aliases,
                    min_density=2.0,
                    window_chars=500,
                )
                for dc in density_cands:
                    all_candidates.append(
                        DefinitionCandidate(
                            concept_slug=dc.slug,
                            source_id=source_id,
                            source_section_id="density-match",
                            snippet=dc.definition,
                            anchor="density",
                            confidence=min(1.0, dc.density / 5.0),
                        )
                    )
            except Exception:
                # Degrade gracefully — if the extractor fails for any
                # reason, the existing 2-pass pipeline still runs.
                pass

    best = pick_best_definition(all_candidates)
    if best is None:
        return {
            "concept_slug": concept_slug,
            "enriched": False,
            "reason": "no_definition_found",
        }

    concept_title = existing_fm.get("title", concept_slug.replace("-", " ").title())
    # Narrow alias mining to the neighborhood of the definition snippet,
    # not the whole source file. The whole-file approach produced noise
    # like "the strategic program for climate resilience" as an alias for
    # "occupancy classification" because unrelated "also known as" phrases
    # appeared elsewhere in the file.
    alias_scope_text = best.snippet
    aliases = mine_aliases_for_concept(alias_scope_text, concept_title=concept_title)

    new_content = _render_enriched(
        existing_frontmatter=existing_fm,
        definition=best,
        aliases=aliases,
    )

    # When --force is set, bypass the diff guard entirely — the caller
    # explicitly asked for an overwrite. Otherwise, respect the guard so
    # manually-edited enriched files stay safe.
    if not force:
        decision = should_overwrite(concept_path, new_content)
        if not decision.allowed:
            return {
                "concept_slug": concept_slug,
                "enriched": False,
                "reason": f"blocked_by_diff_guard: {decision.reason}",
            }

    concept_path.write_text(new_content, encoding="utf-8")
    return {
        "concept_slug": concept_slug,
        "enriched": True,
        "definition_confidence": best.confidence,
        "definition_source_id": best.source_id,
        "definition_section_id": best.source_section_id,
        "aliases_count": len(aliases),
    }


def enrich_concepts_inner(
    *,
    repo_root: Path,
    force: bool = False,
) -> dict[str, Any]:
    """Batch-enrich every concept file."""
    concepts_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    if not concepts_dir.exists():
        return {"total": 0, "enriched": 0, "skipped": 0, "results": []}

    results: list[dict[str, Any]] = []
    for concept_file in sorted(concepts_dir.glob("*.md")):
        slug = concept_file.stem
        result = enrich_concept_inner(
            concept_slug=slug,
            repo_root=repo_root,
            force=force,
        )
        results.append(result)

    enriched = sum(1 for r in results if r.get("enriched"))
    skipped = len(results) - enriched
    return {
        "total": len(results),
        "enriched": enriched,
        "skipped": skipped,
        "results": results,
    }


def run_enrich_concept_one(*, concept_slug: str, force: bool = False) -> int:
    result = enrich_concept_inner(
        concept_slug=concept_slug,
        repo_root=get_repo_root(),
        force=force,
    )
    import json
    print(json.dumps(result, indent=2))
    return 0


def run_enrich_concepts(*, force: bool = False) -> int:
    summary = enrich_concepts_inner(
        repo_root=get_repo_root(),
        force=force,
    )
    print(f"enrich-concepts complete: total={summary['total']} enriched={summary['enriched']} skipped={summary['skipped']}")
    for r in summary["results"]:
        marker = "✓" if r.get("enriched") else "✗"
        detail = r.get("reason") if not r.get("enriched") else f"conf={r.get('definition_confidence')} from={r.get('definition_section_id')}"
        print(f"  {marker} {r['concept_slug']}  {detail}")
    return 0
