"""Vitruvius pipeline CLI entrypoint.

All handler imports are lazy (inside each `if args.command == "..."` branch)
so running, e.g., `promote --help` does NOT transitively import
`opendataloader_pdf`, `pypdf`, or `ocrmypdf`. This makes the CLI usable in
minimal environments without the full conversion dependency stack.

See AD-015 in .ai/10_state/decisions.md for the rationale.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from vitruvius.cli_experience import (
    RAW_HELP_FORMATTER,
    ROOT_PARSER_DESCRIPTION,
    ROOT_PARSER_EPILOG,
    add_command_parser,
    execute_with_cli_experience,
)
from vitruvius.source_paths import logical_source_key_for_relative_path


def _add_review_model_args(parser: argparse.ArgumentParser) -> None:
    from vitruvius.config import get_ollama_8gb_safe_model, get_ollama_default_model

    parser.add_argument(
        "--review-model",
        default=None,
        help=(
            "Tier-1 review model override. When omitted, the CLI resolves the model from "
            f"--review-model-preset (default model: {get_ollama_default_model()}, "
            f"8GB-safe preset: {get_ollama_8gb_safe_model()})."
        ),
    )
    parser.add_argument(
        "--review-model-preset",
        choices=["default", "8gb-safe", "ultra-light", "high-quality"],
        default="default",
        help="Named review-model preset to use when --review-model is not set.",
    )


def run_pipeline() -> int:
    from vitruvius.linting import run_lint
    from vitruvius.scanner import run_scan
    from vitruvius.status import run_status

    scan_code = run_scan()
    if scan_code != 0:
        return scan_code

    status_code = run_status()
    if status_code != 0:
        return status_code

    return run_lint()


def run_pipeline_with_review() -> int:
    """Full pipeline ending with LLM review.

    Opt-in composite command. The default `run` stays minimal (scan +
    status + lint) so that CI and automation don't accidentally invoke
    Ollama. Users who want the full path call `run-with-review` explicitly.
    """
    from vitruvius.config import get_ollama_default_model, get_ollama_default_timeout
    from vitruvius.conversion import run_convert
    from vitruvius.normalization.refine import run_refine
    from vitruvius.ollama_review import run_review_relationships_ollama

    rc = run_pipeline()
    if rc != 0:
        return rc
    rc = run_convert()
    if rc != 0:
        return rc
    rc = run_refine()
    if rc != 0:
        return rc
    return run_review_relationships_ollama(
        model=get_ollama_default_model(),
        timeout_seconds=get_ollama_default_timeout(),
    )


def _reset_derived_artifacts(repo_root: Path, force: bool = False) -> bool:
    """Delete all machine-derived pipeline outputs. Return True if reset occurred."""
    targets: list[Path] = [
        repo_root / "002_Raw-Conversion-Layer",
        repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources",
        repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "relationships",
        repo_root / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2",
        repo_root / "006_System-Manifests" / "runs",
        repo_root / "006_System-Manifests" / "registries",
    ]

    print("The following derived artifacts will be DELETED:")
    for t in targets:
        if t.exists():
            print(f"  {t.relative_to(repo_root)}")

    if not force:
        print("\nThis is destructive. Re-run with --force-reset to confirm.")
        return False

    import shutil

    deleted = 0
    for t in targets:
        if t.exists():
            if t.is_dir():
                shutil.rmtree(str(t))
            else:
                t.unlink()
            deleted += 1
            print(f"  DELETED {t.relative_to(repo_root)}")
    print(f"\nReset complete. {deleted} artifact tree(s) removed.")
    return True


def _source_matches_subjects(source_md: Path, subject_set: set[str], repo_root: Path) -> bool:
    """Check whether a canonical source belongs to any of the requested subjects.

    Reads the frontmatter and looks for original_file / source_documents entries,
    then checks if the referenced PDF exists under 001_Raw-Source-Layer/<subject>/.
    Returns True if no subject filter is applied or if a match is found.
    """
    if not subject_set:
        return True
    try:
        text = source_md.read_text(encoding="utf-8")
    except OSError:
        return False
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    try:
        import yaml
        fm = yaml.safe_load(text[3:end].strip())
    except Exception:
        return False
    if not isinstance(fm, dict):
        return False

    frontmatter_rel = fm.get("source_relative_markdown_path")
    if isinstance(frontmatter_rel, str) and frontmatter_rel.strip():
        normalized_rel = Path(frontmatter_rel).as_posix()
        if _conversion_path_matches_subjects(normalized_rel, subject_set):
            return True

    pdf_names: list[str] = []
    orig = fm.get("original_file", "")
    if isinstance(orig, str) and orig.lower().endswith(".pdf"):
        pdf_names.append(Path(orig).name)
    docs = fm.get("source_documents", [])
    if isinstance(docs, list):
        for doc in docs:
            if isinstance(doc, str) and doc.lower().endswith(".pdf"):
                pdf_names.append(Path(doc).name)

    raw_root = repo_root / "001_Raw-Source-Layer"
    for basename in pdf_names:
        for found in raw_root.rglob(basename):
            rel = found.relative_to(raw_root).as_posix()
            if any(rel.startswith(s + "/") for s in subject_set):
                return True

    # Fallback: check if a refined markdown with the same stem exists under
    # any of the requested subjects in 002_Raw-Conversion-Layer.
    conversion_root = repo_root / "002_Raw-Conversion-Layer"
    if conversion_root.exists():
        for subj in subject_set:
            refined_dir = conversion_root / subj / "refined_markdown"
            if refined_dir.exists():
                for found in refined_dir.rglob(f"{source_md.stem}.md"):
                    return True
    return False


def _conversion_path_matches_subjects(relative_conversion_path: str, subject_set: set[str]) -> bool:
    normalized_rel = Path(relative_conversion_path).as_posix()
    rel_parts = Path(normalized_rel).parts

    for subject in subject_set:
        subject_parts = Path(subject).parts
        if normalized_rel.startswith(subject + "/"):
            return True
        if not subject_parts:
            continue

        top_level = subject_parts[0]
        nested_parts = subject_parts[1:]
        if not nested_parts:
            continue
        if len(rel_parts) < 2:
            continue
        if rel_parts[0] != top_level:
            continue
        if rel_parts[1] not in {"raw_markdown", "refined_markdown", "sidecar_json", "ocr_pdf"}:
            continue
        tail_parts = rel_parts[2: 2 + len(nested_parts)]
        if tuple(tail_parts) == tuple(nested_parts):
            return True

    return False


def _read_source_frontmatter(source_md: Path) -> dict[str, object]:
    try:
        text = source_md.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        import yaml

        payload = yaml.safe_load(text[3:end].strip())
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _select_current_phase_canonical_sources(
    canonical_sources: list[Path],
    current_refined_paths: set[str],
) -> tuple[list[Path], int, list[str]]:
    desired_keys = {
        logical_source_key_for_relative_path(path)
        for path in current_refined_paths
    }
    selected_by_key: dict[str, Path] = {}
    duplicate_candidates = 0
    for source_md in canonical_sources:
        frontmatter = _read_source_frontmatter(source_md)
        source_rel = frontmatter.get("source_relative_markdown_path")
        if not isinstance(source_rel, str) or not source_rel.strip():
            continue
        key = logical_source_key_for_relative_path(source_rel)
        if key not in desired_keys:
            continue
        existing = selected_by_key.get(key)
        if existing is not None:
            duplicate_candidates += 1
            if source_md.stat().st_mtime <= existing.stat().st_mtime:
                continue
        selected_by_key[key] = source_md
    missing = sorted(desired_keys - set(selected_by_key))
    return sorted(selected_by_key.values()), duplicate_candidates, missing


def _build_skip_review_high_confidence_payload(
    *,
    extract_report: dict[str, object],
    source_id: str,
) -> dict[str, object]:
    from vitruvius.utils import utc_now_stamp

    relationships = extract_report.get("relationships", [])
    candidates = []
    if isinstance(relationships, list):
        for relationship in relationships:
            if not isinstance(relationship, dict):
                continue
            candidates.append(
                {
                    "candidate": relationship,
                    "review": {
                        "decision": "keep",
                        "confidence": 1.0,
                        "reason": f"skip_review pipeline path for {source_id}",
                        "suggested_type": None,
                    },
                    "source": "skip_review_pipeline",
                }
            )

    return {
        "generated_at": utc_now_stamp(),
        "source_report_generated_at": extract_report.get("generated_at"),
        "source_model": None,
        "source": extract_report.get("source", source_id),
        "threshold": 0.0,
        "count": len(candidates),
        "candidates": candidates,
    }


def _convert_and_refine_for_kg_pipeline(
    *,
    repo_root: Path,
    relative_source_path: str,
    sample_pages: int = 5,
) -> dict[str, object]:
    import json

    from vitruvius.conversion import convert_pdf_at_path, run_convert_one
    from vitruvius.detection import detect_pdf_type
    from vitruvius.normalization.refine import run_refine_one
    from vitruvius.paths import build_conversion_relative_paths, build_ocr_pdf_relative_path

    source_path = repo_root / "001_Raw-Source-Layer" / relative_source_path
    markdown_rel, _json_rel = build_conversion_relative_paths(relative_source_path)
    result: dict[str, object] = {
        "source_relative_path": relative_source_path,
        "converted": False,
        "refined": False,
        "used_ocr": False,
        "ocr_required": False,
        "detection_result": None,
        "recommended_route": None,
    }

    if source_path.suffix.lower() != ".pdf":
        convert_rc = run_convert_one(relative_source_path)
        result["converted"] = convert_rc == 0
        if convert_rc != 0:
            result["error"] = "convert_failed"
            return result
        refine_rc = run_refine_one(relative_markdown_path=markdown_rel.as_posix())
        result["refined"] = refine_rc == 0
        if refine_rc != 0:
            result["error"] = "refine_failed"
        return result

    detection = detect_pdf_type(source_path, sample_pages=sample_pages)
    result["detection_result"] = detection.get("result")
    result["recommended_route"] = detection.get("recommended_route")

    if detection.get("recommended_route") != "OPENDATALOADER_DIRECT":
        import ocrmypdf

        result["ocr_required"] = True
        result["used_ocr"] = True
        ocr_rel = build_ocr_pdf_relative_path(relative_source_path)
        ocr_repo_rel = Path("002_Raw-Conversion-Layer") / ocr_rel
        ocr_abs = repo_root / ocr_repo_rel
        ocr_abs.parent.mkdir(parents=True, exist_ok=True)
        if ocr_abs.exists():
            ocr_abs.unlink()

        ocrmypdf.ocr(
            str(source_path),
            str(ocr_abs),
            languages=["eng"],
            deskew=True,
            skip_text=True,
            progress_bar=False,
        )

        converted = convert_pdf_at_path(
            ocr_abs,
            relative_source_path,
            run_command="run-kg-pipeline",
            detected_pdf_type="OCR_OUTPUT_PDF",
            processing_route="OCR_THEN_OPENDATALOADER",
            output_ocr_pdf_relative_path=ocr_repo_rel.as_posix(),
        )
        result["converted"] = True
        result["convert_output"] = json.dumps(
            {
                "markdown_output_relative": converted.get("markdown_output_relative"),
                "json_output_relative": converted.get("json_output_relative"),
                "status": converted.get("status"),
            }
        )
    else:
        convert_rc = run_convert_one(relative_source_path, sample_pages=sample_pages)
        result["converted"] = convert_rc == 0
        if convert_rc != 0:
            result["error"] = "convert_failed"
            return result

    refine_rc = run_refine_one(relative_markdown_path=markdown_rel.as_posix())
    result["refined"] = refine_rc == 0
    if refine_rc != 0:
        result["error"] = "refine_failed"
    return result


def run_kg_pipeline(
    *,
    dry_run: bool = False,
    skip_review: bool = False,
    review_model: str | None = None,
    review_model_preset: str | None = None,
    review_timeout_seconds: int | None = None,
    review_parallelism: int | None = None,
    snapshot_out_path: str | None = None,
    reset: bool = False,
    force_reset: bool = False,
    all_subjects: bool = False,
    subjects: list[str] | None = None,
    tier: str | None = None,
    force: bool = False,
    ensure_neo4j: bool = False,
) -> int:
    """Unified orchestrator: raw sources -> canonical layer -> KG v2 snapshot.

    Phase 1: scan + convert + refine
    Phase 2: canonicalize refined sources
    Phase 3: extract + review + promote relationships
    Phase 4: build unified KG v2 snapshot
    """
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    from vitruvius.config import (
        get_ollama_default_model,
        get_ollama_default_parallelism,
        get_ollama_default_timeout,
        is_kg_enabled,
        resolve_review_model,
        resolve_review_preset,
    )
    from vitruvius.paths import get_repo_root

    repo_root = get_repo_root()
    runs_dir = repo_root / "006_System-Manifests" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if not is_kg_enabled():
        print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
        return 1

    # --all implies full reset so previous outputs don't pollute the run
    if all_subjects:
        reset = True
        force_reset = True
        print("[--all] Processing all subjects with derived-artifact reset.")

    subject_set = set(subjects) if subjects else None
    if subject_set:
        print(f"[--subject] Restricting to: {sorted(subject_set)}")

    if reset:
        if dry_run:
            print("[DRY-RUN] Would reset derived artifacts")
        else:
            if not _reset_derived_artifacts(repo_root, force=force_reset):
                return 1

    # --tier maps to an appropriate review-model preset for convenience
    effective_preset = review_model_preset
    if tier:
        tier_map = {
            "lightweight": "ultra-light",
            "heavy": "default",
        }
        mapped = tier_map.get(tier)
        if mapped and not review_model_preset:
            effective_preset = mapped
            print(f"[--tier {tier}] Mapped to review-model preset '{mapped}'")

    # Resolve model / timeout / parallelism with preset awareness
    model = resolve_review_model(
        explicit_model=review_model,
        preset=effective_preset,
    )
    preset_cfg = resolve_review_preset(effective_preset)
    timeout = (
        review_timeout_seconds
        or (preset_cfg.get("timeout_seconds") if preset_cfg else None)
        or get_ollama_default_timeout()
    )
    parallelism = (
        review_parallelism
        or (preset_cfg.get("parallelism") if preset_cfg else None)
        or get_ollama_default_parallelism()
    )
    print(f"Review config: model={model}, timeout={timeout}s, parallelism={parallelism}")

    report: dict[str, object] = {
        "action": "run-kg-pipeline",
        "run_id": run_id,
        "dry_run": dry_run,
        "subjects": sorted(subject_set) if subject_set else None,
        "phases": [],
    }

    # ------------------------------------------------------------------
    # Phase 1 — Ingest & Convert
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Phase 1/5 — Scan, Convert, Refine")
    print("=" * 60)

    from vitruvius.conversion import SUPPORTED_DIRECT_INPUT_EXTENSIONS, run_convert, run_convert_one
    from vitruvius.normalization.refine import run_refine, run_refine_one
    from vitruvius.linting import run_lint
    from vitruvius.scanner import run_scan

    if not dry_run:
        if subject_set:
            # Scoped run: scan/status first, then filter and convert one-by-one
            rc = run_pipeline()
            if rc != 0:
                report["error"] = "scan/status/lint failed"
                return rc

            if force:
                # Developer mode: enumerate ALL raw PDFs under the requested subjects
                raw_root = repo_root / "001_Raw-Source-Layer"
                filtered: list[str] = []
                for subj in subject_set:
                    subj_dir = raw_root / subj
                    if subj_dir.exists():
                        for pdf_path in sorted(subj_dir.rglob("*.pdf")):
                            rel = pdf_path.relative_to(raw_root).as_posix()
                            filtered.append(rel)
                print(f"Phase 1 scoped (force): {len(filtered)} PDF(s) found in subject filter")
            else:
                status_report_path = (
                    repo_root / "006_System-Manifests" / "runs" / "latest_status_report.json"
                )
                if status_report_path.exists():
                    status_report = json.loads(status_report_path.read_text(encoding="utf-8"))
                    candidates = sorted(
                        set(status_report.get("new_files", []))
                        | set(status_report.get("changed_files", []))
                    )
                else:
                    candidates = []

                filtered = [p for p in candidates if any(p.startswith(s + "/") for s in subject_set)]
                print(f"Phase 1 scoped: {len(filtered)} file(s) match subject filter (out of {len(candidates)})")

            converted = 0
            refined = 0
            for rel_path in filtered:
                if Path(rel_path).suffix.lower() not in SUPPORTED_DIRECT_INPUT_EXTENSIONS:
                    continue
                try:
                    process_result = _convert_and_refine_for_kg_pipeline(
                        repo_root=repo_root,
                        relative_source_path=rel_path,
                    )
                except Exception as exc:
                    print(f"  WARN: failed to prepare {rel_path}: {exc}")
                    continue
                if process_result.get("converted"):
                    converted += 1
                if process_result.get("refined"):
                    refined += 1
                elif process_result.get("error"):
                    print(f"  WARN: {rel_path} prepare path failed ({process_result['error']})")

            # In force mode, also refine any existing raw_markdown in the subject scope
            # that may not have been touched above (e.g. from prior conversions).
            if force:
                conversion_root = repo_root / "002_Raw-Conversion-Layer"
                if conversion_root.exists():
                    for md_path in sorted(conversion_root.rglob("*.md")):
                        if "raw_markdown" not in md_path.parts:
                            continue
                        rel = md_path.relative_to(conversion_root).as_posix()
                        if any(rel.startswith(s + "/") for s in subject_set):
                            rc = run_refine_one(relative_markdown_path=rel)
                            if rc == 0:
                                refined += 1

            print(f"Phase 1 complete: {converted} converted, {refined} refined")
        else:
            if force:
                raw_root = repo_root / "001_Raw-Source-Layer"

                rc = run_scan()
                if rc != 0:
                    report["error"] = "scan failed"
                    return rc
                rc = run_lint()
                if rc != 0:
                    report["error"] = "lint failed"
                    return rc

                filtered = [
                    path.relative_to(raw_root).as_posix()
                    for path in sorted(raw_root.rglob("*"))
                    if path.is_file() and path.suffix.lower() in SUPPORTED_DIRECT_INPUT_EXTENSIONS
                ]
                print(f"Phase 1 full-scope (force): {len(filtered)} supported file(s) found in raw layer")

                converted = 0
                refined = 0
                for rel_path in filtered:
                    try:
                        process_result = _convert_and_refine_for_kg_pipeline(
                            repo_root=repo_root,
                            relative_source_path=rel_path,
                        )
                    except Exception as exc:
                        print(f"  WARN: failed to prepare {rel_path}: {exc}")
                        continue
                    if process_result.get("converted"):
                        converted += 1
                    if process_result.get("refined"):
                        refined += 1
                    elif process_result.get("error"):
                        print(f"  WARN: {rel_path} prepare path failed ({process_result['error']})")

                if (repo_root / "002_Raw-Conversion-Layer").exists():
                    for md_path in sorted((repo_root / "002_Raw-Conversion-Layer").rglob("*.md")):
                        if "raw_markdown" not in md_path.parts:
                            continue
                        rel = md_path.relative_to(repo_root / "002_Raw-Conversion-Layer").as_posix()
                        rc = run_refine_one(relative_markdown_path=rel)
                        if rc == 0:
                            refined += 1

                print(f"Phase 1 complete: {converted} converted, {refined} refined")
            else:
                # Full run: use batch convert + refine
                rc = run_pipeline()
                if rc != 0:
                    report["error"] = "scan/status/lint failed"
                    return rc
                rc = run_convert()
                if rc != 0:
                    report["error"] = "convert failed"
                    return rc
                from vitruvius.ocr import run_ocr_execute, run_ocr_queue

                rc = run_ocr_queue()
                if rc != 0:
                    report["error"] = "ocr queue failed"
                    return rc
                rc = run_ocr_execute()
                if rc != 0:
                    report["error"] = "ocr execute failed"
                    return rc
                rc = run_refine()
                if rc != 0:
                    report["error"] = "refine failed"
                    return rc
    else:
        if subject_set:
            print(f"[DRY-RUN] Would scan -> filter to {sorted(subject_set)} -> convert-one -> refine-one")
        else:
            print("[DRY-RUN] Would run: scan -> convert -> refine")

    report["phases"].append({"phase": 1, "name": "ingest_convert", "status": "ok"})

    # ------------------------------------------------------------------
    # Phase 2 — Canonicalize
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Phase 2/5 — Canonicalize refined sources")
    print("=" * 60)

    from vitruvius.canonicalize import run_canonicalize, run_canonicalize_one

    phase2_refined_rel_paths: set[str] = set()
    if not dry_run:
        if subject_set:
            conversion_root = repo_root / "002_Raw-Conversion-Layer"
            if conversion_root.exists():
                all_md = sorted(conversion_root.rglob("*.md"))
                all_md = [p for p in all_md if "refined_markdown" in p.parts]
                filtered_md = [
                    p for p in all_md
                    if _conversion_path_matches_subjects(
                        p.relative_to(conversion_root).as_posix(),
                        subject_set,
                    )
                ]
                print(f"Phase 2 scoped: {len(filtered_md)} refined markdown(s) match subject filter")
                phase2_refined_rel_paths = {
                    p.relative_to(conversion_root).as_posix()
                    for p in filtered_md
                }
                canonicalized = 0
                for md_path in filtered_md:
                    rel = md_path.relative_to(conversion_root).as_posix()
                    rc = run_canonicalize_one(relative_markdown_path=rel, force=force)
                    if rc == 0:
                        canonicalized += 1
                print(f"Phase 2 complete: {canonicalized} canonicalized")
            else:
                print("Phase 2: conversion layer empty")
        else:
            rc = run_canonicalize()
            if rc != 0:
                report["error"] = "canonicalize failed"
                return rc
    else:
        if subject_set:
            print(f"[DRY-RUN] Would canonicalize refined markdown under {sorted(subject_set)}")
        else:
            print("[DRY-RUN] Would run: canonicalize (batch)")

    report["phases"].append({"phase": 2, "name": "canonicalize", "status": "ok"})

    # ------------------------------------------------------------------
    # Phase 3 — Extract, Review & Promote
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Phase 3/5 — Extract, Review & Promote relationships")
    print("=" * 60)

    from vitruvius.ollama_review import run_review_relationships_ollama
    from vitruvius.promotion import run_promote_inner
    from vitruvius.relationships_sections import run_extract_relationships_sections_one_inner

    sources_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    relationships_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    relationships_dir.mkdir(parents=True, exist_ok=True)
    phase3_runs_dir = runs_dir / f"kg_pipeline_{run_id}"
    phase3_runs_dir.mkdir(parents=True, exist_ok=True)

    canonical_sources = sorted(sources_dir.glob("*.md")) if sources_dir.exists() else []
    if subject_set and phase2_refined_rel_paths:
        canonical_sources, duplicate_candidates, missing_sources = _select_current_phase_canonical_sources(
            canonical_sources,
            phase2_refined_rel_paths,
        )
        print(f"Found {len(canonical_sources)} current Phase 2 canonical source(s)")
        if duplicate_candidates:
            print(
                "  WARN: ignored "
                f"{duplicate_candidates} stale duplicate canonical source candidate(s)"
            )
        if missing_sources:
            print(
                "  WARN: "
                f"{len(missing_sources)} current refined source(s) have no canonical output"
            )
    elif subject_set:
        canonical_sources = [
            s for s in canonical_sources
            if _source_matches_subjects(s, subject_set, repo_root)
        ]
        print(f"Found {len(canonical_sources)} canonical source(s) after subject filter")
    else:
        print(f"Found {len(canonical_sources)} canonical source(s)")

    extracted_count = 0
    reviewed_count = 0
    promoted_count = 0
    skipped_count = 0
    extracted_relationship_total = 0
    high_confidence_candidate_total = 0
    promotion_candidate_total = 0
    promotion_created_total = 0
    promotion_merged_total = 0
    promotion_skipped_total = 0
    promotion_rejected_total = 0
    promotion_error_total = 0
    promoted_source_count = 0
    zero_relationship_source_count = 0
    zero_high_confidence_source_count = 0

    for source_md in canonical_sources:
        frontmatter = _read_source_frontmatter(source_md)
        source_id = str(frontmatter.get("id") or source_md.stem)
        source_run_dir = phase3_runs_dir / source_id
        source_run_dir.mkdir(parents=True, exist_ok=True)

        extract_json = source_run_dir / "extract.json"
        extract_txt = source_run_dir / "extract.txt"
        review_json = source_run_dir / "review.json"
        review_txt = source_run_dir / "review.txt"
        triage_json = source_run_dir / "triage.json"
        high_conf_json = source_run_dir / "high_conf.json"

        # Determine the input path for relationship extraction.
        # Prefer refined markdown in 002/; fall back to canonical source in 003/.
        refined_candidates: list[Path] = []
        frontmatter_rel = frontmatter.get("source_relative_markdown_path")
        if isinstance(frontmatter_rel, str) and frontmatter_rel.strip():
            candidate = repo_root / "002_Raw-Conversion-Layer" / frontmatter_rel
            if candidate.exists():
                refined_candidates = [candidate]
        if not refined_candidates:
            refined_candidates = [
                p for p in (repo_root / "002_Raw-Conversion-Layer").rglob(f"{source_md.name}")
                if "refined_markdown" in p.parts
            ]
        if not refined_candidates:
            refined_candidates = [
                p for p in (repo_root / "002_Raw-Conversion-Layer").rglob(f"{source_md.stem}.md")
                if "refined_markdown" in p.parts
            ]
        if refined_candidates:
            input_path = refined_candidates[0]
            rel_input = input_path.relative_to(repo_root / "002_Raw-Conversion-Layer").as_posix()
            extract_kwargs: dict[str, object] = {
                "repo_root": repo_root,
                "relative_markdown_path": rel_input,
                "json_output_path": extract_json,
                "txt_output_path": extract_txt,
                "source_id_override": source_id,
            }
        else:
            # Fallback: use canonical source directly
            input_path = source_md
            rel_input = input_path.relative_to(repo_root).as_posix()
            print(f"  NOTE {source_id}: using canonical source (no refined markdown)")
            extract_kwargs = {
                "repo_root": repo_root,
                "relative_markdown_path": rel_input,
                "json_output_path": extract_json,
                "txt_output_path": extract_txt,
                "source_id_override": source_id,
                "source_path": input_path,
            }

        if dry_run:
            print(f"  [DRY-RUN] {source_id}: extract -> review -> promote")
            extracted_count += 1
            continue

        # Extract
        rc = run_extract_relationships_sections_one_inner(**extract_kwargs)
        if rc != 0:
            print(f"  WARN {source_id}: extraction failed (rc={rc})")
            skipped_count += 1
            continue
        extract_report = json.loads(extract_json.read_text(encoding="utf-8"))
        extracted_relationships = int(extract_report.get("total_relationships") or 0)
        extracted_relationship_total += extracted_relationships
        if extracted_relationships == 0:
            zero_relationship_source_count += 1
        extracted_count += 1

        if skip_review:
            high_conf_json.write_text(
                json.dumps(
                    _build_skip_review_high_confidence_payload(
                        extract_report=extract_report,
                        source_id=source_id,
                    ),
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        else:
            # Review
            rc = run_review_relationships_ollama(
                model=str(model),
                timeout_seconds=int(timeout),
                parallelism=int(parallelism),
                extraction_report_path=extract_json,
                review_json_path=review_json,
                review_txt_path=review_txt,
                triage_report_path=triage_json,
                high_confidence_output_path=high_conf_json,
            )
            if rc != 0:
                print(f"  WARN {source_id}: review failed (rc={rc})")
                skipped_count += 1
                continue
            reviewed_count += 1

        high_conf_payload = json.loads(high_conf_json.read_text(encoding="utf-8"))
        high_conf_count = int(high_conf_payload.get("count") or 0)
        high_confidence_candidate_total += high_conf_count
        if high_conf_count == 0:
            zero_high_confidence_source_count += 1

        # Promote
        promote_result = run_promote_inner(
            repo_root=repo_root,
            execute=True,
            rollback_batch_id=None,
            high_confidence_input_path=high_conf_json,
            relationships_output_dir=relationships_dir,
            audit_log_path=phase3_runs_dir / "promotion_audit.log",
        )
        created_count = int(promote_result.get("created") or 0)
        merged_count = int(promote_result.get("merged") or 0)
        skipped_promotion_count = int(promote_result.get("skipped") or 0)
        rejected_promotion_count = int(promote_result.get("rejected") or 0)
        error_count = len(promote_result.get("errors") or [])
        promotion_candidate_total += int(promote_result.get("total_candidates") or 0)
        promotion_created_total += created_count
        promotion_merged_total += merged_count
        promotion_skipped_total += skipped_promotion_count
        promotion_rejected_total += rejected_promotion_count
        promotion_error_total += error_count
        promoted_count += created_count + merged_count
        if created_count or merged_count:
            promoted_source_count += 1
        if promote_result.get("rejected") or promote_result.get("errors"):
            print(f"  WARN {source_id}: promote had errors")

    report["phases"].append(
        {
            "phase": 3,
            "name": "extract_review_promote",
            "status": "ok",
            "sources_total": len(canonical_sources),
            "extracted": extracted_count,
            "extracted_relationships": extracted_relationship_total,
            "reviewed": reviewed_count,
            "promoted": promoted_count,
            "promoted_sources": promoted_source_count,
            "skipped": skipped_count,
            "zero_relationship_sources": zero_relationship_source_count,
            "zero_high_confidence_sources": zero_high_confidence_source_count,
            "high_confidence_candidates": high_confidence_candidate_total,
            "promotion_candidates": promotion_candidate_total,
            "promotion_created": promotion_created_total,
            "promotion_merged": promotion_merged_total,
            "promotion_skipped": promotion_skipped_total,
            "promotion_rejected": promotion_rejected_total,
            "promotion_errors": promotion_error_total,
        }
    )

    # ------------------------------------------------------------------
    # Phase 4 — Build KG v2 Snapshot
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Phase 4/5 — Build unified KG v2 snapshot")
    print("=" * 60)

    from vitruvius.kg.unified_snapshot_builder import UnifiedSnapshotBuilder

    snapshot = None
    if dry_run:
        print("[DRY-RUN] Would run: UnifiedSnapshotBuilder.build()")
        report["phases"].append({"phase": 4, "name": "build_snapshot", "status": "dry_run"})
    else:
        builder = UnifiedSnapshotBuilder(repo_root=repo_root)
        snapshot = builder.build()
        out_path = builder.write_snapshot(
            snapshot=snapshot,
            out_path=Path(snapshot_out_path) if snapshot_out_path else None,
        )
        counts = snapshot.entity_counts()
        print(f"Wrote unified snapshot to {out_path}")
        for key, count in counts.items():
            print(f"  {key}: {count}")
        if builder._warnings:
            print(f"Warnings ({len(builder._warnings)}):")
            for w in builder._warnings[:10]:
                print(f"  - {w}")
        report["phases"].append(
            {
                "phase": 4,
                "name": "build_snapshot",
                "status": "ok",
                "snapshot_path": str(out_path.relative_to(repo_root)),
                "counts": counts,
                "warnings": builder._warnings,
            }
        )

    # ------------------------------------------------------------------
    # Phase 5 — Load into Neo4j
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Phase 5/5 — Load into Neo4j")
    print("=" * 60)

    from vitruvius.config import (
        is_kg_neo4j_backend,
        get_kg_neo4j_uri,
        get_kg_neo4j_user,
        get_kg_neo4j_password,
    )

    if dry_run:
        print("[DRY-RUN] Would load snapshot into Neo4j if kg_transition.neo4j_backend=true")
        report["phases"].append({"phase": 5, "name": "neo4j_load", "status": "dry_run"})
    elif not is_kg_neo4j_backend():
        print("Neo4j backend disabled (kg_transition.neo4j_backend=false). Skipping.")
        print("To enable: set neo4j_backend: true in config/vitruvius.yaml")
        report["phases"].append(
            {
                "phase": 5,
                "name": "neo4j_load",
                "status": "skipped",
                "reason": "kg_transition.neo4j_backend=false",
            }
        )
    elif snapshot is None:
        print("No snapshot built. Skipping Neo4j load.")
        report["phases"].append(
            {
                "phase": 5,
                "name": "neo4j_load",
                "status": "skipped",
                "reason": "no_snapshot",
            }
        )
    else:
        from vitruvius.kg.neo4j_loader import Neo4jLoader
        from vitruvius.kg.neo4j_client import Neo4jClient

        neo4j_uri = get_kg_neo4j_uri()
        neo4j_user = get_kg_neo4j_user()
        neo4j_password = get_kg_neo4j_password()

        print(f"Connecting to Neo4j at {neo4j_uri} ...")
        neo4j = Neo4jClient(
            uri=neo4j_uri,
            user=neo4j_user,
            password=neo4j_password,
        )

        def _finish_neo4j_error(
            *,
            reason: str,
            messages: list[str],
            error: str = "",
        ) -> int:
            for message in messages:
                print(message)
            phase: dict[str, object] = {
                "phase": 5,
                "name": "neo4j_load",
                "status": "error",
                "reason": reason,
            }
            if error:
                phase["error"] = error
            report["phases"].append(phase)
            neo4j.close()
            report_path = runs_dir / f"kg_pipeline_report_{run_id}.json"
            report_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
            print(f"\nPipeline report: {report_path.relative_to(repo_root)}")
            print(json.dumps(report, indent=2, default=str))
            return 1

        connectivity = neo4j.check_connectivity()
        if not connectivity.ok:
            if connectivity.reason == "auth_failed":
                return _finish_neo4j_error(
                    reason="neo4j_auth_failed",
                    error=connectivity.error,
                    messages=[
                        "ERROR: Neo4j authentication failed.",
                        f"  URI: {neo4j_uri}",
                        f"  User: {neo4j_user}",
                        "  Update kg_transition.neo4j_user / neo4j_password in config/vitruvius.yaml,",
                        "  or reset the local Neo4j password to match that config.",
                    ],
                )
            if connectivity.reason == "driver_missing":
                return _finish_neo4j_error(
                    reason="neo4j_driver_missing",
                    error=connectivity.error,
                    messages=[
                        "ERROR: Neo4j Python driver is not installed.",
                        "  Install it with: pip install neo4j",
                    ],
                )
            if ensure_neo4j:
                print("Neo4j is not reachable. Auto-starting (--ensure-neo4j) ...")
                from vitruvius.kg.neo4j_manager import ensure_neo4j_running
                try:
                    ready = ensure_neo4j_running(wait_seconds=90)
                except Exception as exc:
                    print(f"ERROR: Failed to auto-start Neo4j: {exc}")
                    ready = False
                if not ready:
                    report["phases"].append(
                        {
                            "phase": 5,
                            "name": "neo4j_load",
                            "status": "error",
                            "reason": "neo4j_auto_start_failed",
                        }
                    )
                    neo4j.close()
                    report_path = runs_dir / f"kg_pipeline_report_{run_id}.json"
                    report_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
                    print(f"\nPipeline report: {report_path.relative_to(repo_root)}")
                    print(json.dumps(report, indent=2, default=str))
                    return 1
                # Re-create client after auto-start
                neo4j.close()
                neo4j = Neo4jClient(
                    uri=neo4j_uri,
                    user=neo4j_user,
                    password=neo4j_password,
                )
                connectivity = neo4j.check_connectivity()
                if not connectivity.ok:
                    if connectivity.reason == "auth_failed":
                        return _finish_neo4j_error(
                            reason="neo4j_auth_failed",
                            error=connectivity.error,
                            messages=[
                                "ERROR: Neo4j authentication failed after auto-start.",
                                f"  URI: {neo4j_uri}",
                                f"  User: {neo4j_user}",
                                "  Update kg_transition.neo4j_user / neo4j_password in config/vitruvius.yaml,",
                                "  or reset the local Neo4j password to match that config.",
                            ],
                        )
                    return _finish_neo4j_error(
                        reason="neo4j_unreachable",
                        error=connectivity.error,
                        messages=[
                            "ERROR: Neo4j is still not reachable after auto-start.",
                            f"  URI: {neo4j_uri}",
                        ],
                    )
            else:
                return _finish_neo4j_error(
                    reason="neo4j_unreachable",
                    error=connectivity.error,
                    messages=[
                        "ERROR: Neo4j is not reachable.",
                        "  Start it manually, or re-run with --ensure-neo4j to auto-start:",
                        "    python scripts/pipeline_cli.py run-kg-pipeline ... --ensure-neo4j",
                    ],
                )

        loader = Neo4jLoader(snapshot)
        neo4j.init_schema()
        result = loader.load(client=neo4j)
        executed = result.get("executed", False)
        statement_count = result.get("statement_count", 0)
        errors = result.get("errors", [])

        if executed:
            print(f"Loaded {statement_count} Cypher statements into Neo4j.")
        else:
            print(f"Neo4j load returned without execution. Statements: {statement_count}")

        if errors:
            print(f"Errors ({len(errors)}):")
            for err in errors[:5]:
                print(f"  - {err}")

        # Print browser URL
        browser_url = neo4j_uri.replace("bolt://", "http://").replace("neo4j://", "http://")
        if ":" in browser_url:
            host = browser_url.rsplit(":", 1)[0]
            browser_url = f"{host}:7474"
        else:
            browser_url = f"{browser_url}:7474"
        print(f"\nNeo4j Browser: {browser_url}")
        print(f"  User: {neo4j_user}")
        print(f"  Password: {'*' * len(neo4j_password)}")

        report["phases"].append(
            {
                "phase": 5,
                "name": "neo4j_load",
                "status": "ok" if executed and not errors else "partial",
                "statements": statement_count,
                "errors": len(errors),
            }
        )

        neo4j.close()

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    report_path = runs_dir / f"kg_pipeline_report_{run_id}.json"
    report_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(f"\nPipeline report: {report_path.relative_to(repo_root)}")
    print(json.dumps(report, indent=2, default=str))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=ROOT_PARSER_DESCRIPTION,
        epilog=ROOT_PARSER_EPILOG,
        formatter_class=RAW_HELP_FORMATTER,
    )
    parser.add_argument(
        "--output-mode",
        choices=["auto", "operator", "concise"],
        default="auto",
        help="How much operator framing to print around command output (default: auto).",
    )
    subparsers = parser.add_subparsers(dest="command")

    add_command_parser(subparsers, "scan")
    add_command_parser(subparsers, "status")
    add_command_parser(subparsers, "lint")
    add_command_parser(subparsers, "convert")
    add_command_parser(subparsers, "reconcile")
    add_command_parser(subparsers, "ocr-queue")
    add_command_parser(subparsers, "run")
    add_command_parser(subparsers, "migrate-ids-plan")
    add_command_parser(subparsers, "migrate-ids-apply")

    p_kv_migrate = add_command_parser(
        subparsers,
        "ple-kv-migrate",
    )
    p_kv_migrate.add_argument("--store", choices=["event", "registry"], required=True)
    p_kv_migrate.add_argument("--source", type=Path, required=True)
    p_kv_migrate.add_argument("--dest", type=Path, required=True)
    p_kv_migrate.add_argument("--dry-run", action="store_true")

    detect_parser = add_command_parser(subparsers, "detect-one")
    detect_parser.add_argument("relative_pdf_path")
    detect_parser.add_argument("--sample-pages", type=int, default=5)

    convert_one_parser = add_command_parser(subparsers, "convert-one")
    convert_one_parser.add_argument("relative_pdf_path")
    convert_one_parser.add_argument("--sample-pages", type=int, default=5)

    # Sprint PIPELINE-CLI Task 3 — Phase 1B parser-chain CLI.
    # Parallel command to convert-one; routes through
    # ParserOrchestrator + the p1b_* feature flags. See
    # scripts/vitruvius/parsers/cli_handler.py for the handler and
    # scripts/vitruvius/parsers/factory.py for the flag dispatch.
    convert_parsers_one_parser = add_command_parser(
        subparsers,
        "convert-parsers-one",
    )
    convert_parsers_one_parser.add_argument("relative_pdf_path")

    spreadsheet_parser = add_command_parser(subparsers, "convert-spreadsheet-one")
    spreadsheet_parser.add_argument("relative_source_path")

    ocr_parser = add_command_parser(subparsers, "ocr-execute")
    ocr_parser.add_argument("--languages", nargs="+", default=["eng"])
    ocr_parser.add_argument("--no-deskew", action="store_true")

    plan_parser = add_command_parser(subparsers, "canonicalize-plan-one")
    plan_parser.add_argument("relative_markdown_path")

    execute_parser = add_command_parser(subparsers, "canonicalize-one")
    execute_parser.add_argument("relative_markdown_path")

    concept_parser = add_command_parser(subparsers, "canonicalize-concept-one")
    concept_parser.add_argument("concept_name")

    rel_parser = add_command_parser(subparsers, "extract-relationships-one")
    rel_parser.add_argument("relative_markdown_path")

    sec_parser = add_command_parser(subparsers, "extract-relationships-sections-one")
    sec_parser.add_argument("relative_markdown_path")
    sec_parser.add_argument("--json-out", dest="json_output_path", default=None,
                            help="Optional explicit JSON output path")
    sec_parser.add_argument("--txt-out", dest="txt_output_path", default=None,
                            help="Optional explicit TXT output path")
    sec_parser.add_argument("--source-id", dest="source_id_override", default=None,
                            help="Optional explicit source node id override")
    sec_parser.add_argument("--concept-path", dest="concept_paths", action="append", default=None,
                            help="Optional concept markdown path to whitelist (repeatable)")

    review_parser = add_command_parser(subparsers, "review-relationships-ollama")
    review_parser.add_argument("--model", default="gemma4:31b")
    review_parser.add_argument("--timeout-seconds", type=int, default=600)
    review_parser.add_argument("--parallel", type=int, default=None,
                               help="Concurrent Ollama requests (default: config)")
    review_parser.add_argument("--input-report", dest="extraction_report_path", default=None,
                               help="Optional explicit extraction report JSON path")
    review_parser.add_argument("--review-json-out", dest="review_json_path", default=None,
                               help="Optional explicit review JSON output path")
    review_parser.add_argument("--review-txt-out", dest="review_txt_path", default=None,
                               help="Optional explicit review TXT output path")
    review_parser.add_argument("--triage-out", dest="triage_report_path", default=None,
                               help="Optional explicit triage JSON output path")
    review_parser.add_argument("--high-confidence-out", dest="high_confidence_output_path", default=None,
                               help="Optional explicit high-confidence JSON output path")

    promote_parser = add_command_parser(subparsers, "promote")
    promote_parser.add_argument("--execute", action="store_true",
                                help="Write changes (default: dry-run)")
    promote_parser.add_argument("--rollback", dest="rollback_batch_id",
                                default=None,
                                help="Rollback the given promotion batch ID")
    promote_parser.add_argument("--input-report", dest="high_confidence_input_path", default=None,
                                help="Optional explicit high-confidence review JSON path")
    promote_parser.add_argument("--relationships-out-dir", dest="relationships_output_dir", default=None,
                                help="Optional explicit relationship output directory")
    promote_parser.add_argument("--audit-log-path", dest="audit_log_path", default=None,
                                help="Optional explicit promotion audit log path")

    second_pass_parser = add_command_parser(subparsers, "review-relationships-ollama-second-pass")
    second_pass_parser.add_argument("--model", default=None,
                                    help="Tier-2 model (default: qwen3:30b)")
    second_pass_parser.add_argument("--timeout-seconds", type=int, default=None)
    second_pass_parser.add_argument("--input-review-report", dest="tier_one_report_path", default=None,
                                    help="Optional explicit tier-one review JSON path")
    second_pass_parser.add_argument("--merged-out", dest="merged_report_path", default=None,
                                    help="Optional explicit merged review output path")
    second_pass_parser.add_argument("--worklist-out", dest="worklist_path", default=None,
                                    help="Optional explicit human worklist output path")

    enrich_one_parser = add_command_parser(subparsers, "enrich-concept-one")
    enrich_one_parser.add_argument("concept_slug")
    enrich_one_parser.add_argument("--force", action="store_true",
                                   help="Re-enrich even if canonical_status is already enriched")

    enrich_parser = add_command_parser(subparsers, "enrich-concepts")
    enrich_parser.add_argument("--force", action="store_true",
                               help="Re-enrich even already-enriched concepts")

    add_command_parser(subparsers, "canonicalize")
    add_command_parser(subparsers, "refine")
    add_command_parser(subparsers, "run-with-review")

    aec_improve_parser = add_command_parser(subparsers, "aec-improve-relationships")
    aec_improve_parser.add_argument(
        "--input-path",
        type=Path,
        default=Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json"),
    )
    aec_improve_parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("006_System-Manifests/aec-mepfs-backbone/semantic-overlays"),
    )
    aec_improve_parser.add_argument("--run-id", default=None)
    aec_improve_parser.add_argument("--dry-run", action="store_true", default=True)
    aec_improve_parser.add_argument("--resume", action="store_true")
    aec_improve_parser.add_argument("--all-nodes", action="store_true", default=False)
    aec_improve_parser.add_argument("--all-pairs", dest="all_relationship_candidates", action="store_true", default=False)
    aec_improve_parser.add_argument("--all-relationship-candidates", dest="all_relationship_candidates", action="store_true")
    aec_improve_parser.add_argument("--all-node-consolidation-candidates", action="store_true", default=False)
    aec_improve_parser.add_argument("--max-nodes", type=int, default=1000)
    aec_improve_parser.add_argument("--max-pairs", type=int, default=5000)
    aec_improve_parser.add_argument("--candidate-top-k", type=int, default=20)
    aec_improve_parser.add_argument("--min-similarity", type=float, default=0.35)
    aec_improve_parser.add_argument("--accept-threshold", type=float, default=0.85)
    aec_improve_parser.add_argument("--verify-threshold", type=float, default=0.65)
    aec_improve_parser.add_argument("--verify-uncertain", action="store_true")
    aec_improve_parser.add_argument("--improve-nodes", action="store_true", default=False)
    aec_improve_parser.add_argument("--node-consolidation-mode", choices=["off", "candidates", "audit_only"], default="off")
    aec_improve_parser.add_argument("--node-candidate-top-k", type=int, default=10)
    aec_improve_parser.add_argument("--node-min-similarity", type=float, default=0.82)
    aec_improve_parser.add_argument("--node-max-pairs", type=int, default=1000)
    aec_improve_parser.add_argument("--node-accept-threshold", type=float, default=0.90)
    aec_improve_parser.add_argument("--node-review-threshold", type=float, default=0.75)
    aec_improve_parser.add_argument("--node-judge-provider", choices=["ollama", "deepseek", "auto"], default="auto")
    aec_improve_parser.add_argument("--embedding-model", default="qwen3-embedding:0.6b")
    aec_improve_parser.add_argument("--judge-model", default="qwen3.5:9b")
    aec_improve_parser.add_argument(
        "--verifier-model",
        default="deepseek-r1:8b-0528-qwen3-q4_K_M",
    )
    aec_improve_parser.add_argument("--ollama-base-url", default="http://localhost:11434")
    aec_improve_parser.add_argument("--sleep-seconds", type=float, default=2.0)
    aec_improve_parser.add_argument("--verifier-sleep-seconds", type=float, default=3.0)
    aec_improve_parser.add_argument("--embedding-batch-size", type=int, default=1)
    aec_improve_parser.add_argument("--num-ctx", type=int, default=4096)
    aec_improve_parser.add_argument("--num-predict", type=int, default=500)
    aec_improve_parser.add_argument("--temperature", type=float, default=0.1)
    aec_improve_parser.add_argument("--think", action="store_true")
    aec_improve_parser.add_argument("--include-existing-pairs", action="store_true")
    aec_improve_parser.add_argument("--store-embedding-text", action="store_true")
    aec_improve_parser.add_argument("--stable-embedding-cache", type=Path, default=None)
    aec_improve_parser.add_argument("--no-stable-embedding-cache", action="store_true")
    aec_improve_parser.add_argument("--use-global-ledger", action=argparse.BooleanOptionalAction, default=True)
    aec_improve_parser.add_argument(
        "--global-ledger-path",
        type=Path,
        default=None,
    )
    aec_improve_parser.add_argument("--ignore-global-ledger", action="store_true", default=False)
    aec_improve_parser.add_argument(
        "--global-ledger-decision-filter",
        default="accepted,candidate,rejected,validation_error",
    )
    aec_improve_parser.add_argument("--force-ledger-reuse", action="store_true", default=False)
    aec_improve_parser.add_argument("--use-node-consolidation-ledger", action=argparse.BooleanOptionalAction, default=True)
    aec_improve_parser.add_argument("--node-consolidation-ledger-path", type=Path, default=None)
    aec_improve_parser.add_argument("--ignore-node-consolidation-ledger", action="store_true", default=False)
    aec_improve_parser.add_argument(
        "--node-consolidation-ledger-decision-filter",
        default="accepted,candidate,rejected,validation_error",
    )
    aec_improve_parser.add_argument("--force-node-consolidation-ledger-reuse", action="store_true", default=False)
    aec_improve_parser.add_argument("--apply", action="store_true")
    aec_improve_parser.add_argument("--allow-cloud-ai", action="store_true")
    aec_improve_parser.add_argument(
        "--council-mode",
        choices=["local_only", "deepseek_local", "cloud_first", "adaptive_cloud", "local_first_cloud_verify", "audit_only"],
        default="local_only",
    )
    aec_improve_parser.add_argument("--cloud-cost-budget-usd", type=float, default=None)
    aec_improve_parser.add_argument("--cloud-total-max-calls", type=int, default=None)
    aec_improve_parser.add_argument("--cloud-timeout-seconds", type=int, default=120)
    aec_improve_parser.add_argument("--cloud-max-retries", type=int, default=2)
    aec_improve_parser.add_argument("--cloud-backoff-seconds", type=float, default=10.0)
    aec_improve_parser.add_argument("--cloud-circuit-breaker-failures", type=int, default=3)
    aec_improve_parser.add_argument("--cloud-redact-fields", default="")
    aec_improve_parser.add_argument("--judge-provider", choices=["ollama", "kimi", "deepseek", "auto"], default="auto")
    aec_improve_parser.add_argument("--verifier-provider", choices=["ollama", "kimi", "deepseek", "auto"], default="auto")
    aec_improve_parser.add_argument(
        "--adjudicator-provider",
        choices=["none", "ollama", "kimi", "deepseek", "auto"],
        default="none",
    )
    aec_improve_parser.add_argument("--kimi-base-url", default="https://api.kimi.com/coding/v1")
    aec_improve_parser.add_argument("--kimi-model", default="kimi-for-coding")
    aec_improve_parser.add_argument("--kimi-api-key-env", default="KIMI_API_KEY")
    aec_improve_parser.add_argument("--kimi-disable-thinking", action=argparse.BooleanOptionalAction, default=True)
    aec_improve_parser.add_argument("--kimi-max-tokens", type=int, default=700)
    aec_improve_parser.add_argument("--kimi-sleep-seconds", type=float, default=2.0)
    aec_improve_parser.add_argument("--kimi-max-calls", type=int, default=None)
    aec_improve_parser.add_argument("--kimi-estimated-cost-per-call-usd", type=float, default=0.0)
    aec_improve_parser.add_argument("--kimi-verify-accepted-sample-rate", type=float, default=0.25)
    aec_improve_parser.add_argument("--kimi-verify-uncertain", action="store_true", default=None)
    aec_improve_parser.add_argument("--allow-custom-kimi-base-url", action="store_true")
    aec_improve_parser.add_argument(
        "--enable-kimi-experimental",
        action="store_true",
        help="Deprecated/experimental. Kimi Code chat completion is not recommended for this workflow.",
    )
    aec_improve_parser.add_argument("--deepseek-base-url", default="https://api.deepseek.com")
    aec_improve_parser.add_argument("--deepseek-flash-model", default="deepseek-v4-flash")
    aec_improve_parser.add_argument("--deepseek-pro-model", default="deepseek-v4-pro")
    aec_improve_parser.add_argument("--deepseek-api-key-env", default="DEEPSEEK_API_KEY")
    aec_improve_parser.add_argument("--deepseek-disable-thinking", action=argparse.BooleanOptionalAction, default=True)
    aec_improve_parser.add_argument("--deepseek-reasoning-effort", choices=["high", "max"], default="high")
    aec_improve_parser.add_argument("--deepseek-max-tokens", type=int, default=700)
    aec_improve_parser.add_argument("--deepseek-sleep-seconds", type=float, default=1.0)
    aec_improve_parser.add_argument("--deepseek-flash-max-calls", type=int, default=None)
    aec_improve_parser.add_argument("--deepseek-pro-max-calls", type=int, default=None)
    aec_improve_parser.add_argument("--deepseek-flash-call-buffer", type=float, default=0.50)
    aec_improve_parser.add_argument("--allow-custom-deepseek-base-url", action="store_true")
    aec_improve_parser.add_argument("--cloud-preflight", action=argparse.BooleanOptionalAction, default=True)
    aec_improve_parser.add_argument("--deepseek-retry-truncated-json", action=argparse.BooleanOptionalAction, default=True)
    aec_improve_parser.add_argument("--hierarchy-canonical-predicate", choices=["broader_than", "narrower_than"], default="broader_than")
    aec_improve_parser.add_argument("--convert-taxonomy-part-of", action=argparse.BooleanOptionalAction, default=True)
    aec_improve_parser.add_argument("--enable-safe-schema-repair", action=argparse.BooleanOptionalAction, default=True)
    aec_improve_parser.add_argument(
        "--schema-repair-acceptance-policy",
        choices=["needs_review_only", "allow_accept_after_final_guard"],
        default="needs_review_only",
    )
    aec_improve_parser.add_argument("--verify-accepted-cloud", action="store_true", default=None)
    aec_improve_parser.add_argument("--verify-accepted-sample-rate", type=float, default=0.25)
    aec_improve_parser.add_argument("--adjudicate-disagreements", action="store_true", default=None)
    aec_improve_parser.add_argument("--high-impact-pro-adjudication", action="store_true", default=True)
    aec_improve_parser.add_argument("--fallback-to-local-on-cloud-exhaustion", action="store_true", default=True)
    aec_improve_parser.add_argument("--fallback-to-local-on-cloud-error", action="store_true", default=True)
    aec_improve_parser.add_argument("--fallback-to-local-on-rate-limit", action="store_true", default=True)
    aec_improve_parser.add_argument("--stop-on-cloud-auth-error", action="store_true")
    aec_improve_parser.add_argument("--strict-cloud-only", action="store_true")
    aec_improve_parser.add_argument("--reset-cloud-budget-for-resume", action="store_true")
    aec_improve_parser.add_argument("--progress-mode", choices=["auto", "rich", "plain", "off"], default="auto")
    aec_improve_parser.add_argument("--progress-refresh-per-second", type=float, default=2.0)
    aec_improve_parser.add_argument("--progress-log-every-seconds", type=float, default=30.0)
    aec_improve_parser.add_argument("--progress-show-recent", type=int, default=8)
    aec_improve_parser.add_argument("--progress-transient", action="store_true")
    aec_improve_parser.add_argument("--no-progress", dest="progress_mode", action="store_const", const="off")
    aec_improve_parser.add_argument("--force-rich-in-git-bash", action="store_true")
    aec_improve_parser.add_argument("--watch-run", default=None)
    aec_improve_parser.add_argument("--atomic-write-retries", type=int, default=20)
    aec_improve_parser.add_argument("--atomic-write-backoff-seconds", type=float, default=0.05)
    aec_improve_parser.add_argument("--atomic-write-max-backoff-seconds", type=float, default=1.0)
    aec_improve_parser.add_argument("--jsonl-fsync", action=argparse.BooleanOptionalAction, default=True)

    aec_watch_parser = add_command_parser(subparsers, "aec-watch-relationship-run")
    aec_watch_parser.add_argument("--run-id", default=None)
    aec_watch_parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("006_System-Manifests/aec-mepfs-backbone/semantic-overlays"),
    )
    aec_watch_parser.add_argument("--output-dir", type=Path, default=None)
    aec_watch_parser.add_argument("--progress-mode", choices=["auto", "rich", "plain", "off"], default="auto")
    aec_watch_parser.add_argument("--refresh-seconds", type=float, default=2.0)
    aec_watch_parser.add_argument("--show-recent", type=int, default=12)
    aec_watch_parser.add_argument("--exit-when-complete", action="store_true")
    aec_watch_parser.add_argument("--watch-latest", action="store_true")
    aec_watch_parser.add_argument("--force-rich-in-git-bash", action="store_true")

    kg_pipeline_parser = add_command_parser(subparsers, "run-kg-pipeline")
    kg_pipeline_parser.add_argument("--dry-run", action="store_true",
                                    help="Plan stages without executing writes")
    kg_pipeline_parser.add_argument("--skip-review", action="store_true",
                                    help="Skip LLM review and promote all extracted relationships")
    kg_pipeline_parser.add_argument("--review-model", default=None,
                                    help="Tier-1 review model override")
    kg_pipeline_parser.add_argument("--review-model-preset", default=None,
                                    choices=["default", "8gb-safe", "ultra-light", "high-quality"],
                                    help="Named review model preset (default, 8gb-safe, ultra-light, high-quality). When set, overrides --review-model unless explicitly provided.")
    kg_pipeline_parser.add_argument("--tier", default=None,
                                    choices=["lightweight", "heavy"],
                                    help=(
                                        "High-level model tier. lightweight -> qwen2.5:3b review + nomic-embed-text embeddings. "
                                        "heavy -> llama3.1:8b (or gemma4:31b with high-quality preset). "
                                        "Maps to an appropriate --review-model-preset unless one is explicitly provided."
                                    ))
    kg_pipeline_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                    help="Tier-1 review timeout seconds")
    kg_pipeline_parser.add_argument("--review-parallel", type=int, default=None,
                                    help="Tier-1 review parallelism override")
    kg_pipeline_parser.add_argument("--snapshot-out", default=None,
                                    help="Optional output path for the KG v2 snapshot JSON")
    kg_pipeline_parser.add_argument("--reset", action="store_true",
                                    help="Delete all derived artifacts (002, 003/sources, 003/relationships, 005/kg-v2, 006/runs, 006/registries) before running")
    kg_pipeline_parser.add_argument("--force-reset", action="store_true",
                                    help="Confirm destructive reset (required with --reset)")
    kg_pipeline_parser.add_argument("--all", action="store_true",
                                    help="Process all subjects. Automatically resets derived artifacts before running.")
    kg_pipeline_parser.add_argument("--subject", action="append", default=None,
                                    help=(
                                        "Restrict to a specific subject folder under 001_Raw-Source-Layer/ "
                                        "(e.g. 001-Laws). Repeatable for multiple subjects."
                                    ))
    kg_pipeline_parser.add_argument("--force", action="store_true",
                                    help="Force reprocessing of all files in scope, bypassing incremental guards (new/changed filters and canonical diff).")
    kg_pipeline_parser.add_argument("--ensure-neo4j", action="store_true",
                                    help="Automatically download and start Neo4j if it is not running before Phase 5.")

    neo4j_start_parser = add_command_parser(subparsers, "neo4j-start")
    neo4j_start_parser.add_argument("--wait-seconds", type=int, default=90,
                                    help="Seconds to wait for Neo4j to become ready")

    neo4j_stop_parser = add_command_parser(subparsers, "neo4j-stop")

    dataset_graph_parser = add_command_parser(subparsers, "run-dataset-graph")
    dataset_graph_parser.add_argument("--dataset-manifest", required=True,
                                      help="Dataset manifest to orchestrate")
    dataset_graph_parser.add_argument("--structured-check", action="append", default=None,
                                      help="Repeatable FUNCTION:SUBJECT structured check against the final snapshot")
    dataset_graph_parser.add_argument("--skip-export-owl", action="store_true",
                                      help="Skip dataset-local OWL/Turtle export")
    dataset_source_to_graph_parser = add_command_parser(subparsers, "run-dataset-source-to-graph")
    dataset_source_to_graph_parser.add_argument("--dataset-manifest", required=True,
                                               help="Dataset manifest to orchestrate")
    dataset_source_to_graph_parser.add_argument("--structured-check", action="append", default=None,
                                               help="Repeatable FUNCTION:SUBJECT structured check against the final snapshot")
    dataset_source_to_graph_parser.add_argument("--skip-export-owl", action="store_true",
                                               help="Skip dataset-local OWL/Turtle export")
    dataset_source_to_graph_parser.add_argument("--dry-run", action="store_true",
                                               help="Validate/plans stages without executing writes")
    dataset_source_to_graph_parser.add_argument("--review-model", default=None,
                                               help="Tier-1 review model for dataset-local review")
    dataset_source_to_graph_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                               help="Tier-1 review timeout seconds")
    dataset_source_to_graph_parser.add_argument("--review-parallel", type=int, default=None,
                                               help="Tier-1 review parallelism override")
    dataset_source_to_graph_parser.add_argument("--review-preset", default=None,
                                               help="Optional review preset (for example: m2-8gb-safe)")
    dataset_source_to_graph_parser.add_argument("--visualize", action="store_true",
                                               help="Render an HTML graph visualization after a successful non-dry-run execution")
    dataset_source_to_graph_parser.add_argument("--open-browser", action="store_true",
                                               help="Open the rendered HTML graph visualization in the default browser after a successful non-dry-run execution")
    dataset_source_to_graph_parser.add_argument("--visualization-out", default=None,
                                               help="Optional output HTML path for the post-run visualization")
    laws_pilot_parser = add_command_parser(subparsers, "run-laws-pilot")
    laws_pilot_parser.add_argument("--structured-check", action="append", default=None,
                                   help="Repeatable FUNCTION:SUBJECT structured check against the final snapshot")
    laws_pilot_parser.add_argument("--skip-export-owl", action="store_true",
                                   help="Skip dataset-local OWL/Turtle export")
    laws_pilot_parser.add_argument("--dry-run", action="store_true",
                                   help="Validate/plans stages without executing writes")
    laws_pilot_parser.add_argument("--review-model", default=None,
                                   help="Tier-1 review model for dataset-local review")
    laws_pilot_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                   help="Tier-1 review timeout seconds")
    laws_pilot_parser.add_argument("--review-parallel", type=int, default=None,
                                   help="Tier-1 review parallelism override")
    laws_pilot_parser.add_argument("--review-preset", default=None,
                                   help="Optional review preset (for example: m2-8gb-safe)")
    laws_pilot_parser.add_argument("--visualize", action="store_true",
                                   help="Explicitly keep visualization enabled (default for non-dry-run pilot runs)")
    laws_pilot_parser.add_argument("--open-browser", action="store_true",
                                   help="Open the rendered HTML graph visualization in the default browser after a successful non-dry-run execution")
    laws_pilot_parser.add_argument("--visualization-out", default=None,
                                   help="Optional output HTML path for the post-run visualization")
    all_laws_dry_run_parser = add_command_parser(subparsers, "run-laws-all-dry-run")
    all_laws_dry_run_parser.add_argument("--review-model", default=None,
                                         help="Optional review model override for readiness planning")
    all_laws_dry_run_parser.add_argument("--review-parallel", type=int, default=None,
                                         help="Optional review parallelism override for readiness planning")
    all_laws_dry_run_parser.add_argument("--review-preset", default=None,
                                         help="Optional review preset (for example: m2-8gb-safe)")
    tranche_dry_run_parser = add_command_parser(subparsers, "run-laws-tranche-dry-run")
    tranche_dry_run_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                        help="Scoped tranche manifest to inspect without widening into execute mode")
    tranche_dry_run_parser.add_argument("--review-model", default=None,
                                        help="Optional review model override for tranche planning")
    tranche_dry_run_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                        help="Optional review timeout override for tranche planning")
    tranche_dry_run_parser.add_argument("--review-parallel", type=int, default=None,
                                        help="Optional review parallelism override for tranche planning")
    tranche_dry_run_parser.add_argument("--review-preset", default=None,
                                        help="Optional review preset (for example: m2-8gb-safe)")
    laws_duplicate_parser = add_command_parser(subparsers, "run-laws-duplicate-dry-run")
    laws_duplicate_parser.add_argument("--tranche-manifest", default=None,
                                       help="Optional tranche manifest to restrict duplicate reporting to a bounded slice")
    tranche_source_prep_parser = add_command_parser(subparsers, "run-laws-tranche-source-prep-dry-run")
    tranche_source_prep_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                            help="Tranche manifest whose raw inputs should be inventoried for source preparation")
    tranche_source_prep_parser.add_argument("--sample-pages", type=int, default=5,
                                            help="Sample pages for per-PDF detection planning (default: 5)")
    tranche_source_prep_exec_parser = add_command_parser(subparsers, "run-laws-tranche-source-prep")
    tranche_source_prep_exec_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                 help="Tranche manifest whose raw inputs should be prepared into conversion/refinement outputs")
    tranche_source_prep_exec_parser.add_argument("--sample-pages", type=int, default=5,
                                                 help="Sample pages for per-PDF route detection (default: 5)")
    tranche_source_prep_exec_parser.add_argument("--allow-ocr", action="store_true",
                                                 help="When set, run OCR-first preparation for tranche PDFs that require OCR instead of only reporting them as blocked")
    tranche_source_admission_parser = add_command_parser(subparsers, "run-laws-tranche-source-admission-dry-run")
    tranche_source_admission_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                 help="Tranche manifest whose prepared outputs should be classified into ready-vs-blocked source admission state")
    tranche_source_admission_parser.add_argument("--source-prep-report", default=None,
                                                 help="Optional explicit tranche source-prep execute report to classify for source admission")
    tranche_source_admission_exec_parser = add_command_parser(subparsers, "run-laws-tranche-source-admission")
    tranche_source_admission_exec_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                      help="Tranche manifest whose selected prepared outputs should be admitted into canonical source pages")
    tranche_source_admission_exec_parser.add_argument("--source-prep-report", default=None,
                                                      help="Optional explicit tranche source-prep execute report to use during source admission")
    tranche_source_to_graph_dry_run_parser = add_command_parser(subparsers, "run-laws-tranche-source-to-graph-dry-run")
    tranche_source_to_graph_dry_run_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                        help="Tranche manifest whose admitted source state should be staged through the bounded source-to-graph dry-run")
    tranche_source_to_graph_dry_run_parser.add_argument("--review-preset", default=None,
                                                        help="Optional review preset override for the staged source-to-graph dry-run")
    tranche_source_to_graph_exec_parser = add_command_parser(subparsers, "run-laws-tranche-source-to-graph")
    tranche_source_to_graph_exec_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                     help="Tranche manifest whose admitted source state should be staged through the bounded source-to-graph execute wrapper")
    tranche_source_to_graph_exec_parser.add_argument("--review-preset", default=None,
                                                     help="Optional review preset override for the staged source-to-graph execute wrapper")
    aggregate_manifest_parser = add_command_parser(subparsers, "build-laws-completed-aggregate-manifest")
    aggregate_manifest_parser.add_argument("--out", default="config/datasets/laws-completed-aggregate.yaml",
                                          help="Output path for the generated completed-laws aggregate manifest")
    aggregate_run_parser = add_command_parser(subparsers, "run-laws-completed-aggregate")
    aggregate_run_parser.add_argument("--dry-run", action="store_true",
                                     help="Validate/plans stages without executing graph writes")
    aggregate_run_parser.add_argument("--review-model", default=None,
                                     help="Tier-1 review model for aggregate review")
    aggregate_run_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                     help="Tier-1 review timeout seconds")
    aggregate_run_parser.add_argument("--review-parallel", type=int, default=None,
                                     help="Tier-1 review parallelism override")
    aggregate_run_parser.add_argument("--review-preset", default=None,
                                     help="Optional review preset (for example: m2-8gb-safe)")
    aggregate_run_parser.add_argument("--skip-export-owl", action="store_true",
                                     help="Skip dataset-local OWL/Turtle export")
    generic_aggregate_manifest_parser = add_command_parser(subparsers, "build-completed-aggregate-manifest")
    generic_aggregate_manifest_parser.add_argument("--completed-ledger", required=True,
                                                  help="Completed-lanes ledger YAML path")
    generic_aggregate_manifest_parser.add_argument("--manifest-index", required=True,
                                                  help="Manifest index YAML path")
    generic_aggregate_manifest_parser.add_argument("--dataset-id", required=True)
    generic_aggregate_manifest_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_manifest_parser.add_argument("--out", required=True,
                                                  help="Output dataset manifest path")
    generic_aggregate_manifest_parser.add_argument("--graph-output-root", required=True)
    generic_aggregate_manifest_parser.add_argument("--run-output-root", required=True)
    generic_aggregate_manifest_parser.add_argument("--query-snapshot-template", required=True)
    generic_aggregate_profile_build_parser = add_command_parser(subparsers, "build-completed-aggregate-from-profile")
    generic_aggregate_profile_build_parser.add_argument("--profile", required=True,
                                                       help="Aggregate profile YAML path")
    generic_aggregate_catalog_build_parser = add_command_parser(subparsers, "build-completed-aggregate-from-catalog")
    generic_aggregate_catalog_build_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml")
    generic_aggregate_catalog_build_parser.add_argument("--dataset-id", required=True)
    generic_aggregate_catalog_build_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_catalog_build_parser.add_argument("--out", required=True)
    generic_aggregate_catalog_build_parser.add_argument("--graph-output-root", required=True)
    generic_aggregate_catalog_build_parser.add_argument("--run-output-root", required=True)
    generic_aggregate_catalog_build_parser.add_argument("--query-snapshot-template", required=True)
    generic_aggregate_catalog_build_parser.add_argument("--status", action="append", default=[])
    generic_aggregate_catalog_build_parser.add_argument("--family", action="append", default=[])
    generic_aggregate_register_parser = add_command_parser(subparsers, "register-completed-aggregate-family")
    generic_aggregate_register_parser.add_argument("--family", required=True)
    generic_aggregate_register_parser.add_argument("--profile", required=True,
                                                  help="Profile YAML path to create or update")
    generic_aggregate_register_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                                  help="Profile catalog YAML path")
    generic_aggregate_register_parser.add_argument("--dataset-id", required=True)
    generic_aggregate_register_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_register_parser.add_argument("--completed-ledger", required=True)
    generic_aggregate_register_parser.add_argument("--manifest-index", required=True)
    generic_aggregate_register_parser.add_argument("--out-manifest", required=True)
    generic_aggregate_register_parser.add_argument("--graph-output-root", required=True)
    generic_aggregate_register_parser.add_argument("--run-output-root", required=True)
    generic_aggregate_register_parser.add_argument("--query-snapshot-template", required=True)
    generic_aggregate_register_parser.add_argument("--scope-note", action="append", default=[])
    generic_aggregate_register_parser.add_argument("--lane-note-template", default=None)
    generic_aggregate_register_parser.add_argument("--status", default="ready")
    generic_aggregate_register_parser.add_argument("--note", default=None)
    generic_aggregate_promote_rules_parser = add_command_parser(subparsers, "promote-generated-canonical-rules")
    generic_aggregate_promote_rules_parser.add_argument("--rule-name", action="append", required=True)
    generic_aggregate_promote_rules_parser.add_argument("--generated-rules", default=None)
    generic_aggregate_promote_rules_parser.add_argument("--base-rules", default=None)
    generic_aggregate_promote_concepts_parser = add_command_parser(subparsers, "promote-scaffolded-concepts")
    generic_aggregate_promote_concepts_parser.add_argument("--concept-path", action="append", required=True)
    generic_aggregate_promote_relationships_parser = add_command_parser(subparsers, "promote-scaffolded-relationships")
    generic_aggregate_promote_relationships_parser.add_argument("--relationship-path", action="append", required=True)
    generic_aggregate_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-family")
    generic_aggregate_scaffold_parser.add_argument("--family", required=True)
    generic_aggregate_scaffold_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                                  help="Profile catalog YAML path")
    generic_aggregate_scaffold_parser.add_argument("--dataset-id", default=None)
    generic_aggregate_scaffold_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_scaffold_parser.add_argument("--profile", default=None)
    generic_aggregate_scaffold_parser.add_argument("--completed-ledger", default=None)
    generic_aggregate_scaffold_parser.add_argument("--manifest-index", default=None)
    generic_aggregate_scaffold_parser.add_argument("--out-manifest", default=None)
    generic_aggregate_scaffold_parser.add_argument("--graph-output-root", default=None)
    generic_aggregate_scaffold_parser.add_argument("--run-output-root", default=None)
    generic_aggregate_scaffold_parser.add_argument("--query-snapshot-template", default=None)
    generic_aggregate_scaffold_parser.add_argument("--scope-note", action="append", default=[])
    generic_aggregate_scaffold_parser.add_argument("--lane-note-template", default=None)
    generic_aggregate_scaffold_parser.add_argument("--status", default="scaffolded")
    generic_aggregate_scaffold_parser.add_argument("--note", default=None)
    generic_aggregate_admit_parser = add_command_parser(subparsers, "admit-completed-aggregate-manifest")
    generic_aggregate_admit_parser.add_argument("--family", required=True)
    generic_aggregate_admit_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                               help="Profile catalog YAML path")
    generic_aggregate_admit_parser.add_argument("--lane-id", required=True)
    generic_aggregate_admit_parser.add_argument("--manifest", required=True,
                                               help="Completed manifest YAML path to admit into the family ledgers")
    generic_aggregate_check_parser = add_command_parser(subparsers, "check-completed-aggregate-family")
    generic_aggregate_check_parser.add_argument("--family", required=True)
    generic_aggregate_check_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                               help="Profile catalog YAML path")
    generic_aggregate_lane_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-lane-manifest")
    generic_aggregate_lane_scaffold_parser.add_argument("--family", required=True)
    generic_aggregate_lane_scaffold_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                                       help="Profile catalog YAML path")
    generic_aggregate_lane_scaffold_parser.add_argument("--lane-id", required=True)
    generic_aggregate_lane_scaffold_parser.add_argument("--raw-root", required=True,
                                                       help="Repo-relative raw root directory to inventory")
    generic_aggregate_lane_scaffold_parser.add_argument("--out-manifest", default=None)
    generic_aggregate_lane_scaffold_parser.add_argument("--max-files", type=int, default=5)
    generic_aggregate_lane_scaffold_parser.add_argument("--extension", action="append", default=[],
                                                       help="Allowed file extension (repeatable). Defaults to supported direct-input extensions")
    generic_aggregate_lane_scaffold_parser.add_argument("--raw-path", action="append", default=[],
                                                       help="Explicit repo-relative raw file path to include (repeatable)")
    generic_aggregate_lane_inspect_parser = add_command_parser(subparsers, "inspect-completed-aggregate-lane-sources")
    generic_aggregate_lane_inspect_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_inspect_parser.add_argument("--sample-pages", type=int, default=5)
    generic_aggregate_lane_prep_parser = add_command_parser(subparsers, "prepare-completed-aggregate-lane-sources")
    generic_aggregate_lane_prep_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_prep_parser.add_argument("--sample-pages", type=int, default=5)
    generic_aggregate_lane_prep_parser.add_argument("--allow-ocr", action="store_true")
    generic_aggregate_lane_prep_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_lane_admission_parser = add_command_parser(subparsers, "source-admit-completed-aggregate-lane-dry-run")
    generic_aggregate_lane_admission_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_admission_parser.add_argument("--source-prep-report", default=None)
    generic_aggregate_lane_admission_exec_parser = add_command_parser(subparsers, "source-admit-completed-aggregate-lane")
    generic_aggregate_lane_admission_exec_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_admission_exec_parser.add_argument("--source-prep-report", default=None)
    generic_aggregate_lane_rule_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-lane-canonical-rules")
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--source-type", required=True)
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--trust-level", required=True)
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--output-rules", default=None)
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--core-concept", action="append", default=[])
    generic_aggregate_lane_concept_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-lane-concepts")
    generic_aggregate_lane_concept_scaffold_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_concept_scaffold_parser.add_argument("--output-dir", default=None)
    generic_aggregate_manifest_concept_admit_parser = add_command_parser(subparsers, "admit-concepts-to-manifest")
    generic_aggregate_manifest_concept_admit_parser.add_argument("--manifest", required=True)
    generic_aggregate_manifest_concept_admit_parser.add_argument("--folder-name", required=True)
    generic_aggregate_manifest_concept_admit_parser.add_argument("--concept-path", action="append", required=True,
                                                                 help="Repeatable concept markdown path to admit into the manifest.")
    generic_aggregate_lane_relationship_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-lane-relationships")
    generic_aggregate_lane_relationship_scaffold_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_relationship_scaffold_parser.add_argument("--predicate", default="governs")
    generic_aggregate_lane_relationship_scaffold_parser.add_argument("--output-dir", default=None)
    generic_aggregate_lane_relationship_promote_parser = add_command_parser(subparsers, "promote-completed-aggregate-lane-relationships")
    generic_aggregate_lane_relationship_promote_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_bootstrap_parser = add_command_parser(subparsers, "bootstrap-completed-aggregate-family-lane")
    generic_aggregate_lane_bootstrap_parser.add_argument("--family", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--lane-id", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--raw-root", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml")
    generic_aggregate_lane_bootstrap_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_lane_bootstrap_parser.add_argument("--source-type", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--trust-level", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--core-concept", action="append", default=[])
    generic_aggregate_lane_bootstrap_parser.add_argument("--predicate", default="governs")
    generic_aggregate_lane_bootstrap_parser.add_argument("--family-note", default=None)
    generic_aggregate_lane_bootstrap_parser.add_argument("--max-files", type=int, default=5)
    generic_aggregate_lane_bootstrap_parser.add_argument("--extension", action="append", default=[])
    generic_aggregate_lane_bootstrap_parser.add_argument("--raw-path", action="append", default=[])
    generic_aggregate_lane_bootstrap_parser.add_argument("--sample-pages", type=int, default=5)
    generic_aggregate_lane_bootstrap_parser.add_argument("--allow-ocr", action="store_true")
    generic_aggregate_candidate_parser = add_command_parser(subparsers, "suggest-completed-aggregate-family-candidates")
    generic_aggregate_candidate_parser.add_argument("--raw-root", required=True)
    generic_aggregate_candidate_parser.add_argument("--max-candidates", type=int, default=5)
    generic_aggregate_candidate_parser.add_argument("--sample-pages", type=int, default=5)
    generic_aggregate_candidate_parser.add_argument("--extension", action="append", default=[])
    generic_aggregate_build_report_summary_parser = add_command_parser(subparsers, "summarize-dataset-build-report")
    generic_aggregate_build_report_summary_parser.add_argument("--build-report", required=True)
    generic_aggregate_build_report_summary_parser.add_argument("--top-n", type=int, default=10)
    concept_candidate_parser = add_command_parser(subparsers, "suggest-concept-candidates-from-refined")
    concept_candidate_parser.add_argument("--refined-markdown-path", required=True,
                                         help="Path under 002_Raw-Conversion-Layer to inspect for definition-style concept candidates.")
    concept_candidate_parser.add_argument("--top-n", type=int, default=25)
    generic_aggregate_catalog_run_parser = add_command_parser(subparsers, "run-completed-aggregate-family")
    generic_aggregate_catalog_run_parser.add_argument("--family", required=True,
                                                     help="Registered dataset family name from the profile catalog")
    generic_aggregate_catalog_run_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                                     help="Profile catalog YAML path")
    generic_aggregate_catalog_run_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_catalog_run_parser.add_argument("--review-model", default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-timeout-seconds", type=int, default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-parallel", type=int, default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-preset", default=None)
    generic_aggregate_catalog_run_parser.add_argument("--skip-export-owl", action="store_true")
    generic_aggregate_run_parser = add_command_parser(subparsers, "run-completed-aggregate")
    generic_aggregate_run_parser.add_argument("--completed-ledger", required=True)
    generic_aggregate_run_parser.add_argument("--manifest-index", required=True)
    generic_aggregate_run_parser.add_argument("--dataset-id", required=True)
    generic_aggregate_run_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_run_parser.add_argument("--out", required=True)
    generic_aggregate_run_parser.add_argument("--graph-output-root", required=True)
    generic_aggregate_run_parser.add_argument("--run-output-root", required=True)
    generic_aggregate_run_parser.add_argument("--query-snapshot-template", required=True)
    generic_aggregate_run_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_run_parser.add_argument("--review-model", default=None)
    generic_aggregate_run_parser.add_argument("--review-timeout-seconds", type=int, default=None)
    generic_aggregate_run_parser.add_argument("--review-parallel", type=int, default=None)
    generic_aggregate_run_parser.add_argument("--review-preset", default=None)
    generic_aggregate_run_parser.add_argument("--skip-export-owl", action="store_true")
    generic_aggregate_profile_run_parser = add_command_parser(subparsers, "run-completed-aggregate-from-profile")
    generic_aggregate_profile_run_parser.add_argument("--profile", required=True,
                                                     help="Aggregate profile YAML path")
    generic_aggregate_profile_run_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_profile_run_parser.add_argument("--review-model", default=None)
    generic_aggregate_profile_run_parser.add_argument("--review-timeout-seconds", type=int, default=None)
    generic_aggregate_profile_run_parser.add_argument("--review-parallel", type=int, default=None)
    generic_aggregate_profile_run_parser.add_argument("--review-preset", default=None)
    generic_aggregate_profile_run_parser.add_argument("--skip-export-owl", action="store_true")
    generic_aggregate_catalog_run_parser = add_command_parser(subparsers, "run-completed-aggregate-from-catalog")
    generic_aggregate_catalog_run_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml")
    generic_aggregate_catalog_run_parser.add_argument("--dataset-id", required=True)
    generic_aggregate_catalog_run_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_catalog_run_parser.add_argument("--out", required=True)
    generic_aggregate_catalog_run_parser.add_argument("--graph-output-root", required=True)
    generic_aggregate_catalog_run_parser.add_argument("--run-output-root", required=True)
    generic_aggregate_catalog_run_parser.add_argument("--query-snapshot-template", required=True)
    generic_aggregate_catalog_run_parser.add_argument("--status", action="append", default=[])
    generic_aggregate_catalog_run_parser.add_argument("--family", action="append", default=[])
    generic_aggregate_catalog_run_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_catalog_run_parser.add_argument("--review-model", default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-timeout-seconds", type=int, default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-parallel", type=int, default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-preset", default=None)
    generic_aggregate_catalog_run_parser.add_argument("--skip-export-owl", action="store_true")
    refine_one_parser = add_command_parser(subparsers, "refine-one")
    refine_one_parser.add_argument("relative_markdown_path")

    rotate_parser = add_command_parser(subparsers, "rotate-registries")
    rotate_parser.add_argument("--keep", type=int, default=30,
                               help="Number of timestamped snapshots to retain per family (default: 30)")
    rotate_parser.add_argument("--dry-run", action="store_true",
                               help="Show what would be pruned without deleting")

    build_graph_parser = add_command_parser(subparsers, "build-graph")
    build_graph_parser.add_argument("--dry-run", action="store_true",
                                    help="Run walker + integrity checks only; do not write files")
    build_graph_parser.add_argument(
        "--dataset-manifest",
        default=None,
        help="Optional dataset manifest for scoped graph output",
    )

    query_graph_parser = add_command_parser(subparsers, "query-graph")
    query_graph_parser.add_argument("--from", dest="from_id", required=True,
                                    help="Source node id")
    query_graph_parser.add_argument("--to", dest="to_id", required=True,
                                    help="Target node id")
    query_graph_parser.add_argument("--max-depth", type=int, default=3,
                                    help="Max path depth (default: 3)")
    query_graph_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )

    export_graph_parser = add_command_parser(subparsers, "export-graph-snapshot")
    export_graph_parser.add_argument("--format", dest="fmt", default="json",
                                     choices=["json"],
                                     help="Output format (default: json)")
    export_graph_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )

    # Stream M.4 — export-graph-owl
    export_graph_owl_parser = add_command_parser(
        subparsers,
        "export-graph-owl",
    )
    export_graph_owl_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )
    export_graph_owl_parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Optional output Turtle path",
    )

    visualize_graph_parser = add_command_parser(subparsers, "visualize-graph")
    visualize_graph_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )
    visualize_graph_parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Optional output HTML path",
    )
    visualize_graph_parser.add_argument(
        "--version",
        dest="vis_version",
        default="auto",
        choices=["auto", "v1", "v2"],
        help="Snapshot format version (default: auto-detect)",
    )

    add_command_parser(subparsers, "ingest-spatial")

    # Sprint KG — evidence graph ingestion
    kg_ingest_evidence_parser = add_command_parser(subparsers, "kg-ingest-evidence")
    kg_ingest_evidence_parser.add_argument(
        "source_path",
        help="Path to raw source document (PDF or Markdown)",
    )
    kg_ingest_evidence_parser.add_argument(
        "--parser-id",
        default="unknown",
        help="Parser identifier for provenance",
    )
    kg_ingest_evidence_parser.add_argument(
        "--parser-version",
        default=None,
        help="Parser version for provenance",
    )

    # Sprint KG — file-native bulk materialization (no DB required)
    add_command_parser(subparsers, "kg-backfill-evidence")
    add_command_parser(subparsers, "kg-seed-taxonomy")

    # Phase 2 — atomic knowledge extraction
    kg_extract_parser = add_command_parser(subparsers, "kg-extract-candidates")
    kg_extract_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in 005_Operational-Intelligence-Layer/graph/kg-v2/)",
    )
    kg_extract_parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory for candidate JSONL (defaults to 006_System-Manifests/runs/kg_candidates/)",
    )
    kg_extract_parser.add_argument(
        "--unit-types",
        default="concept,definition,rule,procedure,exception",
        help="Comma-separated list of unit types to extract",
    )
    kg_extract_parser.add_argument(
        "--run-id",
        default=None,
        help="Extraction run ID (defaults to ISO timestamp)",
    )

    # Phase 3 — canonicalize and place
    kg_canonical_parser = add_command_parser(subparsers, "kg-canonicalize-candidates")
    kg_canonical_parser.add_argument(
        "--candidates",
        default=None,
        help="Path to candidate JSONL from kg-extract-candidates (defaults to latest in 006_System-Manifests/runs/kg_candidates/)",
    )
    kg_canonical_parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory for canonical JSONL (defaults to 006_System-Manifests/runs/kg_canonical/)",
    )
    kg_canonical_parser.add_argument(
        "--run-id",
        default=None,
        help="Canonicalization run ID (defaults to ISO timestamp)",
    )

    # Phase 4 — materialize canonical graph
    kg_materialize_parser = add_command_parser(subparsers, "kg-materialize-canonical")
    kg_materialize_parser.add_argument(
        "--taxonomy-snapshot",
        default=None,
        help="Path to taxonomy snapshot JSON (defaults to latest kg-v2 taxonomy)",
    )
    kg_materialize_parser.add_argument(
        "--canonical-jsonl",
        default=None,
        help="Path to Phase 3 canonical JSONL (defaults to latest in kg_canonical/)",
    )
    kg_materialize_parser.add_argument(
        "--out-path",
        default=None,
        help="Output path for unified canonical snapshot",
    )

    # Phase 4b — assertion validation
    kg_validate_parser = add_command_parser(subparsers, "kg-validate-assertions")
    kg_validate_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in kg-v2/)",
    )

    # Phase 4c — contradiction detection
    kg_contra_parser = add_command_parser(subparsers, "kg-detect-contradictions")
    kg_contra_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in kg-v2/)",
    )

    # Phase 4d — dematerialize edge (rollback helper)
    kg_dematerialize_parser = add_command_parser(subparsers, "kg-dematerialize-edge")
    kg_dematerialize_parser.add_argument(
        "assertion_id",
        help="Assertion ID whose fast edge should be removed",
    )
    kg_dematerialize_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in kg-v2/)",
    )
    kg_dematerialize_parser.add_argument(
        "--out-path",
        default=None,
        help="Output path for modified snapshot (defaults to overwrite original)",
    )

    # Phase 5/9 — build unified snapshot from all canonical sources
    kg_unified_parser = add_command_parser(subparsers, "kg-build-unified")
    kg_unified_parser.add_argument(
        "--out-path",
        default=None,
        help="Output path for unified snapshot (defaults to kg-v2/)",
    )

    kg_enrich_relationships_parser = add_command_parser(subparsers, "kg-enrich-relationships")
    kg_enrich_relationships_parser.add_argument(
        "--snapshot",
        default=None,
        help="Existing kg-v2 snapshot JSON to enrich (defaults to latest unified snapshot in kg-v2/)",
    )
    kg_enrich_relationships_parser.add_argument(
        "--out-path",
        default=None,
        help="Output path for enriched snapshot (defaults to timestamped kg-v2 unified_enriched file)",
    )
    kg_enrich_relationships_parser.add_argument(
        "--max-new-assertions",
        type=int,
        default=160,
        help="Maximum semantic relationship assertions to add",
    )
    kg_enrich_relationships_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the enrichment report without writing an output snapshot",
    )
    kg_enrich_relationships_parser.add_argument(
        "--load-neo4j",
        action="store_true",
        help="Load the enriched snapshot into Neo4j after writing it",
    )
    kg_enrich_relationships_parser.add_argument(
        "--clear-neo4j",
        action="store_true",
        help="Clear Neo4j before loading the enriched snapshot",
    )
    kg_enrich_relationships_parser.add_argument(
        "--ensure-neo4j",
        action="store_true",
        help="Try to start Neo4j before loading, if it is not already reachable",
    )

    # Sprint KG — review queue (Gate 6)
    kg_review_queue_parser = add_command_parser(subparsers, "kg-review-queue")
    kg_review_queue_parser.add_argument(
        "--status",
        default="REVIEW_REQUIRED",
        choices=["CANDIDATE", "VALIDATED", "REVIEW_REQUIRED", "REJECTED"],
        help="Filter assertions by validation status",
    )
    kg_review_queue_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in 005_Operational-Intelligence-Layer/graph/kg-v2/)",
    )

    kg_review_action_parser = add_command_parser(subparsers, "kg-review-action")
    kg_review_action_parser.add_argument(
        "assertion_id",
        help="ID of the assertion to act on",
    )
    kg_review_action_parser.add_argument(
        "--action",
        required=True,
        choices=["approve", "reject", "escalate"],
        help="Operator decision",
    )
    kg_review_action_parser.add_argument(
        "--reason",
        default="",
        help="Human-readable reason for the decision",
    )
    kg_review_action_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in 005_Operational-Intelligence-Layer/graph/kg-v2/)",
    )

    # Phase 7 — canonical graph inspection
    kg_inspect_node_parser = add_command_parser(subparsers, "kg-inspect-node")
    kg_inspect_node_parser.add_argument(
        "node_id",
        help="Canonical node ID to inspect",
    )
    kg_inspect_node_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in kg-v2/)",
    )

    kg_inspect_assertion_parser = add_command_parser(subparsers, "kg-inspect-assertion")
    kg_inspect_assertion_parser.add_argument(
        "assertion_id",
        help="Assertion ID to inspect",
    )
    kg_inspect_assertion_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in kg-v2/)",
    )

    # Phase 5 — canonical-first query commands
    kg_query_nodes_parser = add_command_parser(subparsers, "kg-query-nodes")
    kg_query_nodes_parser.add_argument(
        "query",
        help="Label substring to search for",
    )
    kg_query_nodes_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in kg-v2/)",
    )
    kg_query_nodes_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum results to return",
    )

    kg_query_neighborhood_parser = add_command_parser(subparsers, "kg-query-neighborhood")
    kg_query_neighborhood_parser.add_argument(
        "node_id",
        help="Canonical node ID to explore",
    )
    kg_query_neighborhood_parser.add_argument(
        "--snapshot",
        default=None,
        help="Path to a kg-v2 snapshot JSON (defaults to latest in kg-v2/)",
    )

    evaluate_spatial_parser = add_command_parser(subparsers, "evaluate-spatial")
    evaluate_spatial_parser.add_argument(
        "--concepts",
        required=True,
        help="Comma-separated concept slugs to evaluate",
    )
    evaluate_spatial_parser.add_argument(
        "--observations",
        dest="observations_path",
        required=True,
        help="Path to JSON observation file (dict: variable -> value)",
    )
    evaluate_spatial_parser.add_argument(
        "--rules",
        dest="rules_path",
        default=None,
        help="Optional path to JSON rules file (concept_id -> rule)",
    )

    # Stream Y3.4 — ple-cotrace-dump
    ple_cotrace_parser = add_command_parser(
        subparsers,
        "ple-cotrace-dump",
    )
    ple_cotrace_parser.add_argument(
        "--cot-dir",
        dest="cot_dir",
        required=True,
        help="Directory containing <utc-ts>_<hash>.json CoT trace files",
    )

    # Stream Y4.3 — ple-registry-purge
    ple_purge_parser = add_command_parser(
        subparsers,
        "ple-registry-purge",
    )
    ple_purge_parser.add_argument(
        "--db",
        dest="registry_db",
        required=True,
        help="Path to the SQLite registry file",
    )
    ple_purge_parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Retention window in days (default: 30)",
    )

    # Stream Y5.3 — ple-vision-probe
    ple_vision_probe_parser = add_command_parser(
        subparsers,
        "ple-vision-probe",
    )
    ple_vision_probe_parser.add_argument(
        "--required-free-gb",
        type=float,
        default=3.5,
        dest="required_free_gb",
        help="Minimum free RAM to require (default: 3.5 GB)",
    )
    ple_vision_probe_parser.add_argument(
        "--model",
        default="moondream:latest",
        help="Vision model family to check for (default: moondream:latest)",
    )

    query_parser = add_command_parser(subparsers, "query")
    query_parser.add_argument("question", help="Natural-language question")
    query_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )

    query_struct_parser = add_command_parser(subparsers, "query-structured")
    query_struct_parser.add_argument(
        "--function", required=True,
        help="One of what_governs, what_requires, what_limits, what_defines, "
             "what_depends_on, what_affects, supersession_chain, neighbors, "
             "edges_between",
    )
    query_struct_parser.add_argument("--subject", default=None,
                                     help="Subject entity id")
    query_struct_parser.add_argument("--a", dest="a", default=None,
                                     help="Entity a (edges_between only)")
    query_struct_parser.add_argument("--b", dest="b", default=None,
                                     help="Entity b (edges_between only)")
    query_struct_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    def _run(command_name: str, handler) -> int:
        return execute_with_cli_experience(
            command_name,
            output_mode=args.output_mode,
            handler=handler,
        )

    if args.command == "scan":
        from vitruvius.scanner import run_scan
        return _run("scan", run_scan)

    if args.command == "status":
        from vitruvius.status import run_status
        return _run("status", run_status)

    if args.command == "lint":
        from vitruvius.linting import run_lint
        return _run("lint", run_lint)

    if args.command == "convert":
        from vitruvius.conversion import run_convert
        return _run("convert", run_convert)

    if args.command == "reconcile":
        from vitruvius.reconcile import run_reconcile
        return _run("reconcile", run_reconcile)

    if args.command == "ocr-queue":
        from vitruvius.ocr import run_ocr_queue
        return _run("ocr-queue", run_ocr_queue)

    if args.command == "ocr-execute":
        from vitruvius.ocr import run_ocr_execute
        return _run(
            "ocr-execute",
            lambda: run_ocr_execute(
            languages=args.languages,
            deskew=not args.no_deskew,
            ),
        )

    if args.command == "run":
        return _run("run", run_pipeline)

    if args.command == "detect-one":
        from vitruvius.detection import run_detect_one
        return _run(
            "detect-one",
            lambda: run_detect_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
            ),
        )

    if args.command == "convert-one":
        from vitruvius.conversion import run_convert_one
        return _run(
            "convert-one",
            lambda: run_convert_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
            ),
        )

    if args.command == "convert-parsers-one":
        # Sprint PIPELINE-CLI Task 3. Lazy-import — see AD-015.
        from vitruvius.parsers.cli_handler import run_convert_parsers_one
        return _run(
            "convert-parsers-one",
            lambda: run_convert_parsers_one(
            relative_pdf_path=args.relative_pdf_path,
            ),
        )

    if args.command == "convert-spreadsheet-one":
        from vitruvius.spreadsheets import run_convert_spreadsheet_one
        return _run(
            "convert-spreadsheet-one",
            lambda: run_convert_spreadsheet_one(
            relative_source_path=args.relative_source_path,
            ),
        )

    if args.command == "canonicalize-plan-one":
        from vitruvius.canonicalize import run_canonicalize_plan_one
        return _run(
            "canonicalize-plan-one",
            lambda: run_canonicalize_plan_one(
            relative_markdown_path=args.relative_markdown_path,
            ),
        )

    if args.command == "canonicalize-one":
        from vitruvius.canonicalize import run_canonicalize_one
        return _run(
            "canonicalize-one",
            lambda: run_canonicalize_one(
            relative_markdown_path=args.relative_markdown_path,
            ),
        )

    if args.command == "canonicalize-concept-one":
        from vitruvius.concepts import run_canonicalize_concept_one
        return _run(
            "canonicalize-concept-one",
            lambda: run_canonicalize_concept_one(
            concept_name=args.concept_name,
            ),
        )

    if args.command == "migrate-ids-plan":
        from vitruvius.migrations import run_migrate_ids_plan
        return _run("migrate-ids-plan", run_migrate_ids_plan)

    if args.command == "migrate-ids-apply":
        from vitruvius.migrations import run_migrate_ids_apply
        return _run("migrate-ids-apply", run_migrate_ids_apply)

    if args.command == "ple-kv-migrate":
        from vitruvius.kv_migrate import run_kv_migrate
        return _run(
            "ple-kv-migrate",
            lambda: run_kv_migrate(
            store=args.store,
            source=args.source,
            dest=args.dest,
            dry_run=args.dry_run,
            ),
        )

    if args.command == "extract-relationships-one":
        from vitruvius.relationships import run_extract_relationships_one
        return _run(
            "extract-relationships-one",
            lambda: run_extract_relationships_one(
            relative_markdown_path=args.relative_markdown_path,
            ),
        )

    if args.command == "extract-relationships-sections-one":
        from vitruvius.relationships_sections import run_extract_relationships_sections_one
        return _run(
            "extract-relationships-sections-one",
            lambda: run_extract_relationships_sections_one(
            relative_markdown_path=args.relative_markdown_path,
            json_output_path=Path(args.json_output_path) if args.json_output_path else None,
            txt_output_path=Path(args.txt_output_path) if args.txt_output_path else None,
            source_id_override=args.source_id_override,
            concept_paths=[Path(p) for p in args.concept_paths] if args.concept_paths else None,
            ),
        )

    if args.command == "review-relationships-ollama":
        from vitruvius.ollama_review import run_review_relationships_ollama
        return _run(
            "review-relationships-ollama",
            lambda: run_review_relationships_ollama(
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            parallelism=args.parallel,
            extraction_report_path=Path(args.extraction_report_path) if args.extraction_report_path else None,
            review_json_path=Path(args.review_json_path) if args.review_json_path else None,
            review_txt_path=Path(args.review_txt_path) if args.review_txt_path else None,
            triage_report_path=Path(args.triage_report_path) if args.triage_report_path else None,
            high_confidence_output_path=Path(args.high_confidence_output_path) if args.high_confidence_output_path else None,
            ),
        )

    if args.command == "promote":
        from vitruvius.promotion import run_promote
        return _run(
            "promote",
            lambda: run_promote(
            execute=args.execute,
            rollback_batch_id=args.rollback_batch_id,
            high_confidence_input_path=Path(args.high_confidence_input_path) if args.high_confidence_input_path else None,
            relationships_output_dir=Path(args.relationships_output_dir) if args.relationships_output_dir else None,
            audit_log_path=Path(args.audit_log_path) if args.audit_log_path else None,
            ),
        )

    if args.command == "review-relationships-ollama-second-pass":
        from vitruvius.ollama_review_second_pass import run_second_pass
        return _run(
            "review-relationships-ollama-second-pass",
            lambda: run_second_pass(
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            tier_one_report_path=Path(args.tier_one_report_path) if args.tier_one_report_path else None,
            merged_report_path=Path(args.merged_report_path) if args.merged_report_path else None,
            worklist_path=Path(args.worklist_path) if args.worklist_path else None,
            ),
        )

    if args.command == "enrich-concept-one":
        from vitruvius.concept_enrichment import run_enrich_concept_one
        return _run(
            "enrich-concept-one",
            lambda: run_enrich_concept_one(
            concept_slug=args.concept_slug,
            force=args.force,
            ),
        )

    if args.command == "enrich-concepts":
        from vitruvius.concept_enrichment import run_enrich_concepts
        return _run(
            "enrich-concepts",
            lambda: run_enrich_concepts(force=args.force),
        )

    if args.command == "canonicalize":
        from vitruvius.canonicalize import run_canonicalize
        return _run("canonicalize", run_canonicalize)

    if args.command == "refine":
        from vitruvius.normalization.refine import run_refine
        return _run("refine", run_refine)

    if args.command == "run-with-review":
        return _run("run-with-review", run_pipeline_with_review)

    if args.command == "run-kg-pipeline":
        return _run(
            "run-kg-pipeline",
            lambda: run_kg_pipeline(
                dry_run=args.dry_run,
                skip_review=args.skip_review,
                review_model=args.review_model,
                review_model_preset=args.review_model_preset,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                snapshot_out_path=args.snapshot_out,
                reset=args.reset,
                force_reset=args.force_reset,
                all_subjects=args.all,
                subjects=args.subject,
                tier=args.tier,
                force=args.force,
                ensure_neo4j=args.ensure_neo4j,
            ),
        )

    if args.command == "aec-improve-relationships":
        from vitruvius.kg.aec_relationship_improvement import (
            ApplyModeDeferredError,
            CloudAIRequiredError,
            CloudProviderError,
            RunFatalError,
            WatchRunConfig,
            config_from_args,
            ensure_apply_mode_is_deferred,
            run_relationship_improvement,
            watch_relationship_run,
        )

        def _run_aec_improve_relationships() -> int:
            try:
                config = config_from_args(args)
                ensure_apply_mode_is_deferred(config.apply)
                if config.watch_run:
                    watch_target = Path(config.watch_run)
                    watch_config = WatchRunConfig(
                        run_id=None if watch_target.exists() or any(sep in config.watch_run for sep in ("/", "\\")) else config.watch_run,
                        output_root=config.output_root,
                        output_dir=watch_target if watch_target.exists() or any(sep in config.watch_run for sep in ("/", "\\")) else None,
                        progress_mode=config.progress_mode,
                        refresh_seconds=max(0.1, 1.0 / max(config.progress_refresh_per_second, 0.1)),
                        show_recent=config.progress_show_recent,
                        force_rich_in_git_bash=config.force_rich_in_git_bash,
                    )
                    return watch_relationship_run(watch_config)
                summary = run_relationship_improvement(config)
            except ApplyModeDeferredError as exc:
                print(f"ERROR: {exc}")
                return 2
            except CloudAIRequiredError as exc:
                print(f"ERROR: {exc}")
                return 2
            except CloudProviderError as exc:
                print(f"ERROR: {exc}")
                return 2
            except RunFatalError:
                return 1
            except RuntimeError as exc:
                print(f"ERROR: {exc}")
                return 2
            except KeyboardInterrupt:
                return 130
            print(json.dumps(summary.to_record(), indent=2, ensure_ascii=False, sort_keys=True))
            return 0

        return _run("aec-improve-relationships", _run_aec_improve_relationships)

    if args.command == "aec-watch-relationship-run":
        from vitruvius.kg.aec_relationship_improvement import WatchRunConfig, watch_relationship_run

        def _run_aec_watch_relationship_run() -> int:
            try:
                return watch_relationship_run(
                    WatchRunConfig(
                        run_id=args.run_id,
                        output_root=args.output_root,
                        output_dir=args.output_dir,
                        progress_mode=args.progress_mode,
                        refresh_seconds=args.refresh_seconds,
                        show_recent=args.show_recent,
                        exit_when_complete=args.exit_when_complete,
                        watch_latest=args.watch_latest,
                        force_rich_in_git_bash=args.force_rich_in_git_bash,
                    )
                )
            except RuntimeError as exc:
                print(f"ERROR: {exc}")
                return 2
            except (FileNotFoundError, ValueError) as exc:
                print(f"ERROR: {exc}")
                return 2
            except KeyboardInterrupt:
                return 130

        return _run("aec-watch-relationship-run", _run_aec_watch_relationship_run)

    if args.command == "neo4j-start":
        from vitruvius.kg.neo4j_manager import ensure_neo4j_running
        def _run_neo4j_start():
            ok = ensure_neo4j_running(wait_seconds=args.wait_seconds)
            return 0 if ok else 1
        return _run("neo4j-start", _run_neo4j_start)

    if args.command == "neo4j-stop":
        from vitruvius.kg.neo4j_manager import stop_neo4j
        def _run_neo4j_stop():
            stop_neo4j()
            return 0
        return _run("neo4j-stop", _run_neo4j_stop)

    if args.command == "run-dataset-graph":
        from vitruvius.dataset_pipeline import (
            DatasetPipelineError,
            parse_structured_check,
            run_dataset_graph_pipeline,
        )
        try:
            structured_checks = [
                parse_structured_check(raw) for raw in (args.structured_check or [])
            ]
        except DatasetPipelineError as exc:
            print(json.dumps({"error": str(exc)}, indent=2))
            return 2
        return _run(
            "run-dataset-graph",
            lambda: run_dataset_graph_pipeline(
                dataset_manifest=args.dataset_manifest,
                structured_checks=structured_checks,
                export_owl=not args.skip_export_owl,
            ),
        )

    if args.command == "run-dataset-source-to-graph":
        from vitruvius.dataset_pipeline import (
            DatasetPipelineError,
            parse_structured_check,
            run_dataset_source_to_graph_pipeline,
        )
        try:
            structured_checks = [
                parse_structured_check(raw) for raw in (args.structured_check or [])
            ]
        except DatasetPipelineError as exc:
            print(json.dumps({"error": str(exc)}, indent=2))
            return 2
        return _run(
            "run-dataset-source-to-graph",
            lambda: run_dataset_source_to_graph_pipeline(
                dataset_manifest=args.dataset_manifest,
                structured_checks=structured_checks,
                export_owl=not args.skip_export_owl,
                dry_run=args.dry_run,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                review_preset=args.review_preset,
                visualize_graph=args.visualize or args.open_browser,
                open_browser=args.open_browser,
                visualization_out_path=args.visualization_out,
            ),
        )

    if args.command == "run-laws-pilot":
        from vitruvius.dataset_pipeline import (
            DatasetPipelineError,
            parse_structured_check,
            run_dataset_source_to_graph_pipeline,
        )
        try:
            structured_checks = [
                parse_structured_check(raw) for raw in (args.structured_check or [])
            ]
        except DatasetPipelineError as exc:
            print(json.dumps({"error": str(exc)}, indent=2))
            return 2
        return _run(
            "run-laws-pilot",
            lambda: run_dataset_source_to_graph_pipeline(
                dataset_manifest="config/datasets/laws-core-bundle-m1.yaml",
                structured_checks=structured_checks,
                export_owl=not args.skip_export_owl,
                dry_run=args.dry_run,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                review_preset=args.review_preset,
                visualize_graph=(not args.dry_run) or args.visualize or args.open_browser,
                open_browser=args.open_browser,
                visualization_out_path=args.visualization_out,
            ),
        )

    if args.command == "run-laws-all-dry-run":
        from vitruvius.laws_readiness import run_all_laws_dry_run
        return _run(
            "run-laws-all-dry-run",
            lambda: run_all_laws_dry_run(
                pilot_manifest="config/datasets/laws-core-bundle-m1.yaml",
                review_model=args.review_model,
                review_model_preset=args.review_preset,
            ),
        )

    if args.command == "run-laws-tranche-dry-run":
        from vitruvius.laws_readiness import run_laws_tranche_dry_run
        return _run(
            "run-laws-tranche-dry-run",
            lambda: run_laws_tranche_dry_run(
                tranche_manifest=args.tranche_manifest,
                pilot_manifest="config/datasets/laws-core-bundle-m1.yaml",
                review_model=args.review_model,
                review_model_preset=args.review_preset,
            ),
        )

    if args.command == "run-laws-duplicate-dry-run":
        from vitruvius.laws_readiness import run_laws_duplicate_dry_run
        return _run(
            "run-laws-duplicate-dry-run",
            lambda: run_laws_duplicate_dry_run(
                tranche_manifest=args.tranche_manifest,
            ),
        )

    if args.command == "run-laws-tranche-source-prep-dry-run":
        from vitruvius.laws_readiness import run_laws_tranche_source_prep_dry_run
        return _run(
            "run-laws-tranche-source-prep-dry-run",
            lambda: run_laws_tranche_source_prep_dry_run(
                tranche_manifest=args.tranche_manifest,
                sample_pages=args.sample_pages,
            ),
        )

    if args.command == "run-laws-tranche-source-prep":
        from vitruvius.laws_readiness import run_laws_tranche_source_prep
        return _run(
            "run-laws-tranche-source-prep",
            lambda: run_laws_tranche_source_prep(
                tranche_manifest=args.tranche_manifest,
                sample_pages=args.sample_pages,
                allow_ocr=args.allow_ocr,
            ),
        )

    if args.command == "run-laws-tranche-source-admission-dry-run":
        from vitruvius.laws_readiness import run_laws_tranche_source_admission_dry_run
        return _run(
            "run-laws-tranche-source-admission-dry-run",
            lambda: run_laws_tranche_source_admission_dry_run(
                tranche_manifest=args.tranche_manifest,
                source_prep_report=args.source_prep_report,
            ),
        )

    if args.command == "run-laws-tranche-source-admission":
        from vitruvius.laws_readiness import run_laws_tranche_source_admission
        return _run(
            "run-laws-tranche-source-admission",
            lambda: run_laws_tranche_source_admission(
                tranche_manifest=args.tranche_manifest,
                source_prep_report=args.source_prep_report,
            ),
        )

    if args.command == "run-laws-tranche-source-to-graph-dry-run":
        from vitruvius.laws_readiness import run_laws_tranche_source_to_graph_dry_run
        return _run(
            "run-laws-tranche-source-to-graph-dry-run",
            lambda: run_laws_tranche_source_to_graph_dry_run(
                tranche_manifest=args.tranche_manifest,
                review_preset=args.review_preset,
            ),
        )

    if args.command == "run-laws-tranche-source-to-graph":
        from vitruvius.laws_readiness import run_laws_tranche_source_to_graph
        return _run(
            "run-laws-tranche-source-to-graph",
            lambda: run_laws_tranche_source_to_graph(
                tranche_manifest=args.tranche_manifest,
                review_preset=args.review_preset,
            ),
        )

    if args.command == "build-completed-aggregate-manifest":
        from vitruvius.aggregate_manifest import build_generic_completed_aggregate_manifest, print_aggregate_manifest_summary
        def _run_generic():
            repo_root = Path.cwd().resolve()
            completed_ledger_path = Path(args.completed_ledger)
            if not completed_ledger_path.is_absolute():
                completed_ledger_path = repo_root / completed_ledger_path
            manifest_index_path = Path(args.manifest_index)
            if not manifest_index_path.is_absolute():
                manifest_index_path = repo_root / manifest_index_path
            out_manifest_path = Path(args.out)
            if not out_manifest_path.is_absolute():
                out_manifest_path = repo_root / out_manifest_path
            aggregate_payload = build_generic_completed_aggregate_manifest(
                repo_root=repo_root,
                completed_ledger_path=completed_ledger_path,
                manifest_index_path=manifest_index_path,
                out_manifest_path=out_manifest_path,
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_path_template=args.query_snapshot_template,
                scope_notes=[f"Aggregate graph input for completed lanes from {completed_ledger_path.name}."],
                lane_note_builder=lambda lane_id: f"Aggregate lane: {lane_id}",
                folder_name_resolver=lambda item: str(item.get('raw_folder_name') or item.get('folder_name') or ''),
            )
            print_aggregate_manifest_summary(
                repo_root=repo_root,
                out_manifest_path=out_manifest_path,
                aggregate_payload=aggregate_payload,
            )
            return 0
        return _run("build-completed-aggregate-manifest", _run_generic)

    if args.command == "build-completed-aggregate-from-profile":
        from vitruvius.aggregate_manifest import (
            build_generic_completed_aggregate_manifest_from_profile,
            print_aggregate_manifest_summary,
        )
        def _run_generic_from_profile():
            repo_root = Path.cwd().resolve()
            out_manifest_path, aggregate_payload, _profile = build_generic_completed_aggregate_manifest_from_profile(
                repo_root=repo_root,
                profile_path=Path(args.profile),
            )
            print_aggregate_manifest_summary(
                repo_root=repo_root,
                out_manifest_path=out_manifest_path,
                aggregate_payload=aggregate_payload,
            )
            return 0
        return _run("build-completed-aggregate-from-profile", _run_generic_from_profile)

    if args.command == "build-completed-aggregate-from-catalog":
        from vitruvius.aggregate_manifest import (
            build_catalog_completed_aggregate_manifest,
            print_aggregate_manifest_summary,
        )
        def _run_generic_from_catalog():
            repo_root = Path.cwd().resolve()
            out_manifest_path = Path(args.out)
            if not out_manifest_path.is_absolute():
                out_manifest_path = repo_root / out_manifest_path
            aggregate_payload = build_catalog_completed_aggregate_manifest(
                repo_root=repo_root,
                catalog_path=Path(args.catalog),
                out_manifest_path=out_manifest_path,
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_path_template=args.query_snapshot_template,
                scope_notes=[f"Catalog aggregate graph input from {Path(args.catalog).name}."],
                statuses=list(args.status or []),
                families=list(args.family or []),
            )
            print_aggregate_manifest_summary(
                repo_root=repo_root,
                out_manifest_path=out_manifest_path,
                aggregate_payload=aggregate_payload,
            )
            return 0
        return _run("build-completed-aggregate-from-catalog", _run_generic_from_catalog)

    if args.command == "register-completed-aggregate-family":
        from vitruvius.aggregate_manifest import register_completed_aggregate_family
        def _run_register_generic_family():
            repo_root = Path.cwd().resolve()
            resolved_profile_path, resolved_catalog_path, profile_payload, catalog_entry = register_completed_aggregate_family(
                repo_root=repo_root,
                family=args.family,
                profile_path=Path(args.profile),
                catalog_path=Path(args.catalog),
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                completed_ledger=args.completed_ledger,
                manifest_index=args.manifest_index,
                out_manifest=args.out_manifest,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_template=args.query_snapshot_template,
                scope_notes=list(args.scope_note or []),
                lane_note_template=args.lane_note_template,
                status=args.status,
                note=args.note,
            )
            print(json.dumps({
                "action": "register-completed-aggregate-family",
                "family": args.family,
                "profile_path": str(resolved_profile_path.relative_to(repo_root)),
                "catalog_path": str(resolved_catalog_path.relative_to(repo_root)),
                "dataset_id": profile_payload["dataset_id"],
                "dataset_kind": profile_payload["dataset_kind"],
                "catalog_entry": catalog_entry,
            }, indent=2))
            return 0
        return _run("register-completed-aggregate-family", _run_register_generic_family)

    if args.command == "promote-generated-canonical-rules":
        from vitruvius.aggregate_manifest import promote_generated_canonical_rules
        def _run_promote_generated_rules():
            repo_root = Path.cwd().resolve()
            summary = promote_generated_canonical_rules(
                repo_root=repo_root,
                rule_names=list(args.rule_name or []),
                generated_rules_path=Path(args.generated_rules) if args.generated_rules else None,
                base_rules_path=Path(args.base_rules) if args.base_rules else None,
            )
            print(json.dumps({
                "action": "promote-generated-canonical-rules",
                **summary,
            }, indent=2))
            return 0
        return _run("promote-generated-canonical-rules", _run_promote_generated_rules)

    if args.command == "promote-scaffolded-concepts":
        from vitruvius.aggregate_manifest import promote_scaffolded_concepts
        def _run_promote_scaffolded_concepts():
            repo_root = Path.cwd().resolve()
            summary = promote_scaffolded_concepts(
                repo_root=repo_root,
                concept_paths=[Path(path) for path in (args.concept_path or [])],
            )
            print(json.dumps({
                "action": "promote-scaffolded-concepts",
                **summary,
            }, indent=2))
            return 0
        return _run("promote-scaffolded-concepts", _run_promote_scaffolded_concepts)

    if args.command == "promote-scaffolded-relationships":
        from vitruvius.aggregate_manifest import promote_scaffolded_relationships
        def _run_promote_scaffolded_relationships():
            repo_root = Path.cwd().resolve()
            summary = promote_scaffolded_relationships(
                repo_root=repo_root,
                relationship_paths=[Path(path) for path in (args.relationship_path or [])],
            )
            print(json.dumps({
                "action": "promote-scaffolded-relationships",
                **summary,
            }, indent=2))
            return 0
        return _run("promote-scaffolded-relationships", _run_promote_scaffolded_relationships)

    if args.command == "scaffold-completed-aggregate-family":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_family
        def _run_scaffold_generic_family():
            repo_root = Path.cwd().resolve()
            scaffold_result = scaffold_completed_aggregate_family(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                profile_path=Path(args.profile) if args.profile else None,
                completed_ledger_path=Path(args.completed_ledger) if args.completed_ledger else None,
                manifest_index_path=Path(args.manifest_index) if args.manifest_index else None,
                out_manifest=args.out_manifest,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_template=args.query_snapshot_template,
                scope_notes=list(args.scope_note or []),
                lane_note_template=args.lane_note_template,
                status=args.status,
                note=args.note,
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-family",
                "family": args.family,
                "profile_path": str(scaffold_result["profile_path"].relative_to(repo_root)),
                "catalog_path": str(scaffold_result["catalog_path"].relative_to(repo_root)),
                "completed_ledger_path": str(scaffold_result["completed_ledger_path"].relative_to(repo_root)),
                "manifest_index_path": str(scaffold_result["manifest_index_path"].relative_to(repo_root)),
                "dataset_id": scaffold_result["profile_payload"]["dataset_id"],
                "dataset_kind": scaffold_result["profile_payload"]["dataset_kind"],
                "catalog_entry": scaffold_result["catalog_entry"],
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-family", _run_scaffold_generic_family)

    if args.command == "admit-completed-aggregate-manifest":
        from vitruvius.aggregate_manifest import admit_completed_manifest_to_family
        def _run_admit_generic_manifest():
            repo_root = Path.cwd().resolve()
            result = admit_completed_manifest_to_family(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
                lane_id=args.lane_id,
                manifest_path=Path(args.manifest),
            )
            print(json.dumps({
                "action": "admit-completed-aggregate-manifest",
                "family": args.family,
                "lane_id": result["lane_id"],
                "manifest_path": str(result["manifest_path"].relative_to(repo_root)),
                "completed_ledger_path": str(result["completed_ledger_path"].relative_to(repo_root)),
                "manifest_index_path": str(result["manifest_index_path"].relative_to(repo_root)),
            }, indent=2))
            return 0
        return _run("admit-completed-aggregate-manifest", _run_admit_generic_manifest)

    if args.command == "check-completed-aggregate-family":
        from vitruvius.aggregate_manifest import check_completed_aggregate_family_readiness
        def _run_check_generic_family():
            repo_root = Path.cwd().resolve()
            readiness = check_completed_aggregate_family_readiness(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
            )
            print(json.dumps({
                "action": "check-completed-aggregate-family",
                **readiness,
            }, indent=2))
            return 0
        return _run("check-completed-aggregate-family", _run_check_generic_family)

    if args.command == "scaffold-completed-aggregate-lane-manifest":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_lane_manifest
        def _run_scaffold_generic_lane():
            repo_root = Path.cwd().resolve()
            result = scaffold_completed_aggregate_lane_manifest(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
                lane_id=args.lane_id,
                raw_root=Path(args.raw_root),
                out_manifest_path=Path(args.out_manifest) if args.out_manifest else None,
                max_files=args.max_files,
                extensions=list(args.extension or []),
                raw_paths=[Path(path) for path in (args.raw_path or [])],
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-lane-manifest",
                "family": args.family,
                "lane_id": result["lane_id"],
                "raw_root": str(result["raw_root"].relative_to(repo_root)),
                "out_manifest_path": str(result["out_manifest_path"].relative_to(repo_root)),
                "selected_file_count": len(result["selected_files"]),
                "selected_files": [str(path.relative_to(repo_root)) for path in result["selected_files"]],
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-lane-manifest", _run_scaffold_generic_lane)

    if args.command == "inspect-completed-aggregate-lane-sources":
        from vitruvius.aggregate_manifest import inspect_completed_aggregate_lane_sources
        def _run_inspect_generic_lane():
            repo_root = Path.cwd().resolve()
            inspection = inspect_completed_aggregate_lane_sources(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                sample_pages=args.sample_pages,
            )
            print(json.dumps({
                "action": "inspect-completed-aggregate-lane-sources",
                **inspection,
            }, indent=2))
            return 0
        return _run("inspect-completed-aggregate-lane-sources", _run_inspect_generic_lane)

    if args.command == "prepare-completed-aggregate-lane-sources":
        from vitruvius.aggregate_manifest import prepare_completed_aggregate_lane_sources
        def _run_prepare_generic_lane():
            repo_root = Path.cwd().resolve()
            summary = prepare_completed_aggregate_lane_sources(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                sample_pages=args.sample_pages,
                allow_ocr=args.allow_ocr,
                dry_run=args.dry_run,
            )
            print(json.dumps(summary, indent=2))
            return 0
        return _run("prepare-completed-aggregate-lane-sources", _run_prepare_generic_lane)

    if args.command == "source-admit-completed-aggregate-lane-dry-run":
        from vitruvius.aggregate_manifest import source_admit_completed_aggregate_lane_dry_run
        def _run_source_admit_generic_lane():
            repo_root = Path.cwd().resolve()
            summary = source_admit_completed_aggregate_lane_dry_run(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                source_prep_report_path=Path(args.source_prep_report) if args.source_prep_report else None,
            )
            print(json.dumps(summary, indent=2))
            return 0
        return _run("source-admit-completed-aggregate-lane-dry-run", _run_source_admit_generic_lane)

    if args.command == "source-admit-completed-aggregate-lane":
        from vitruvius.aggregate_manifest import source_admit_completed_aggregate_lane_execute
        def _run_source_admit_generic_lane_execute():
            repo_root = Path.cwd().resolve()
            summary = source_admit_completed_aggregate_lane_execute(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                source_prep_report_path=Path(args.source_prep_report) if args.source_prep_report else None,
            )
            print(json.dumps(summary, indent=2))
            return 0
        return _run("source-admit-completed-aggregate-lane", _run_source_admit_generic_lane_execute)

    if args.command == "scaffold-completed-aggregate-lane-canonical-rules":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_lane_canonical_rules
        def _run_scaffold_generic_lane_rules():
            repo_root = Path.cwd().resolve()
            summary = scaffold_completed_aggregate_lane_canonical_rules(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                source_type=args.source_type,
                trust_level=args.trust_level,
                output_rules_path=Path(args.output_rules) if args.output_rules else None,
                core_concepts=list(args.core_concept or []),
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-lane-canonical-rules",
                **summary,
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-lane-canonical-rules", _run_scaffold_generic_lane_rules)

    if args.command == "scaffold-completed-aggregate-lane-concepts":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_lane_concepts
        def _run_scaffold_generic_lane_concepts():
            repo_root = Path.cwd().resolve()
            summary = scaffold_completed_aggregate_lane_concepts(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                output_dir=Path(args.output_dir) if args.output_dir else None,
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-lane-concepts",
                **summary,
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-lane-concepts", _run_scaffold_generic_lane_concepts)

    if args.command == "admit-concepts-to-manifest":
        from vitruvius.aggregate_manifest import admit_concepts_to_manifest
        def _run_admit_concepts_to_manifest():
            repo_root = Path.cwd().resolve()
            summary = admit_concepts_to_manifest(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                folder_name=args.folder_name,
                concept_paths=[Path(path) for path in (args.concept_path or [])],
            )
            print(json.dumps({
                "action": "admit-concepts-to-manifest",
                **summary,
            }, indent=2))
            return 0
        return _run("admit-concepts-to-manifest", _run_admit_concepts_to_manifest)

    if args.command == "scaffold-completed-aggregate-lane-relationships":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_lane_relationships
        def _run_scaffold_generic_lane_relationships():
            repo_root = Path.cwd().resolve()
            summary = scaffold_completed_aggregate_lane_relationships(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                predicate=args.predicate,
                output_dir=Path(args.output_dir) if args.output_dir else None,
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-lane-relationships",
                **summary,
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-lane-relationships", _run_scaffold_generic_lane_relationships)

    if args.command == "promote-completed-aggregate-lane-relationships":
        from vitruvius.aggregate_manifest import promote_completed_aggregate_lane_relationships
        def _run_promote_generic_lane_relationships():
            repo_root = Path.cwd().resolve()
            summary = promote_completed_aggregate_lane_relationships(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
            )
            print(json.dumps({
                "action": "promote-completed-aggregate-lane-relationships",
                **summary,
            }, indent=2))
            return 0
        return _run("promote-completed-aggregate-lane-relationships", _run_promote_generic_lane_relationships)

    if args.command == "bootstrap-completed-aggregate-family-lane":
        from vitruvius.aggregate_manifest import bootstrap_completed_aggregate_family_lane
        def _run_bootstrap_generic_family_lane():
            repo_root = Path.cwd().resolve()
            summary = bootstrap_completed_aggregate_family_lane(
                repo_root=repo_root,
                family=args.family,
                lane_id=args.lane_id,
                raw_root=Path(args.raw_root),
                dataset_kind=args.dataset_kind,
                catalog_path=Path(args.catalog),
                source_type=args.source_type,
                trust_level=args.trust_level,
                core_concepts=list(args.core_concept or []),
                predicate=args.predicate,
                family_note=args.family_note,
                max_files=args.max_files,
                extensions=list(args.extension or []),
                raw_paths=[Path(path) for path in (args.raw_path or [])],
                sample_pages=args.sample_pages,
                allow_ocr=args.allow_ocr,
            )
            print(json.dumps({
                "action": "bootstrap-completed-aggregate-family-lane",
                **summary,
            }, indent=2))
            return 0
        return _run("bootstrap-completed-aggregate-family-lane", _run_bootstrap_generic_family_lane)

    if args.command == "suggest-completed-aggregate-family-candidates":
        from vitruvius.aggregate_manifest import suggest_completed_aggregate_family_candidates
        def _run_suggest_generic_family_candidates():
            repo_root = Path.cwd().resolve()
            summary = suggest_completed_aggregate_family_candidates(
                repo_root=repo_root,
                raw_root=Path(args.raw_root),
                max_candidates=args.max_candidates,
                sample_pages=args.sample_pages,
                extensions=list(args.extension or []),
            )
            print(json.dumps({
                "action": "suggest-completed-aggregate-family-candidates",
                **summary,
            }, indent=2))
            return 0
        return _run("suggest-completed-aggregate-family-candidates", _run_suggest_generic_family_candidates)

    if args.command == "summarize-dataset-build-report":
        from vitruvius.aggregate_manifest import summarize_dataset_build_report
        def _run_summarize_dataset_build_report():
            repo_root = Path.cwd().resolve()
            summary = summarize_dataset_build_report(
                repo_root=repo_root,
                build_report_path=Path(args.build_report),
                top_n=args.top_n,
            )
            print(json.dumps({
                "action": "summarize-dataset-build-report",
                **summary,
            }, indent=2))
            return 0
        return _run("summarize-dataset-build-report", _run_summarize_dataset_build_report)

    if args.command == "suggest-concept-candidates-from-refined":
        from vitruvius.concept_candidate_suggestions import run_suggest_concept_candidates

        def _run_suggest_concept_candidates_from_refined():
            return run_suggest_concept_candidates(
                refined_markdown_path=args.refined_markdown_path,
                top_n=args.top_n,
            )

        return _run("suggest-concept-candidates-from-refined", _run_suggest_concept_candidates_from_refined)

    if args.command == "run-completed-aggregate":
        from vitruvius.aggregate_manifest import build_generic_completed_aggregate_manifest, print_aggregate_manifest_summary
        from vitruvius.dataset_pipeline import run_dataset_source_to_graph_pipeline
        def _run_generic_aggregate():
            repo_root = Path.cwd().resolve()
            completed_ledger_path = Path(args.completed_ledger)
            if not completed_ledger_path.is_absolute():
                completed_ledger_path = repo_root / completed_ledger_path
            manifest_index_path = Path(args.manifest_index)
            if not manifest_index_path.is_absolute():
                manifest_index_path = repo_root / manifest_index_path
            out_manifest_path = Path(args.out)
            if not out_manifest_path.is_absolute():
                out_manifest_path = repo_root / out_manifest_path
            aggregate_payload = build_generic_completed_aggregate_manifest(
                repo_root=repo_root,
                completed_ledger_path=completed_ledger_path,
                manifest_index_path=manifest_index_path,
                out_manifest_path=out_manifest_path,
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_path_template=args.query_snapshot_template,
                scope_notes=[f"Aggregate graph input for completed lanes from {completed_ledger_path.name}."],
                lane_note_builder=lambda lane_id: f"Aggregate lane: {lane_id}",
                folder_name_resolver=lambda item: str(item.get('raw_folder_name') or item.get('folder_name') or ''),
            )
            print_aggregate_manifest_summary(
                repo_root=repo_root,
                out_manifest_path=out_manifest_path,
                aggregate_payload=aggregate_payload,
            )
            return run_dataset_source_to_graph_pipeline(
                dataset_manifest=str(out_manifest_path.relative_to(repo_root)),
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
            )
        return _run("run-completed-aggregate", _run_generic_aggregate)

    if args.command == "run-completed-aggregate-from-profile":
        from vitruvius.aggregate_manifest import run_generic_completed_aggregate_from_profile
        return _run(
            "run-completed-aggregate-from-profile",
            lambda: run_generic_completed_aggregate_from_profile(
                repo_root=Path.cwd().resolve(),
                profile_path=Path(args.profile),
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
            ),
        )

    if args.command == "run-completed-aggregate-from-catalog":
        from vitruvius.aggregate_manifest import (
            build_catalog_completed_aggregate_manifest,
            print_aggregate_manifest_summary,
        )
        from vitruvius.dataset_pipeline import run_dataset_source_to_graph_pipeline
        def _run_generic_catalog_aggregate():
            repo_root = Path.cwd().resolve()
            out_manifest_path = Path(args.out)
            if not out_manifest_path.is_absolute():
                out_manifest_path = repo_root / out_manifest_path
            aggregate_payload = build_catalog_completed_aggregate_manifest(
                repo_root=repo_root,
                catalog_path=Path(args.catalog),
                out_manifest_path=out_manifest_path,
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_path_template=args.query_snapshot_template,
                scope_notes=[f"Catalog aggregate graph input from {Path(args.catalog).name}."],
                statuses=list(args.status or []),
                families=list(args.family or []),
            )
            print_aggregate_manifest_summary(
                repo_root=repo_root,
                out_manifest_path=out_manifest_path,
                aggregate_payload=aggregate_payload,
            )
            return run_dataset_source_to_graph_pipeline(
                dataset_manifest=str(out_manifest_path.relative_to(repo_root)),
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
            )
        return _run("run-completed-aggregate-from-catalog", _run_generic_catalog_aggregate)

    if args.command == "run-completed-aggregate-family":
        from vitruvius.aggregate_manifest import (
            resolve_completed_aggregate_profile_path,
            run_generic_completed_aggregate_from_profile,
        )
        def _run_generic_family():
            repo_root = Path.cwd().resolve()
            resolved_profile_path = resolve_completed_aggregate_profile_path(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
            )
            return run_generic_completed_aggregate_from_profile(
                repo_root=repo_root,
                profile_path=resolved_profile_path,
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
            )
        return _run("run-completed-aggregate-family", _run_generic_family)

    if args.command == "build-laws-completed-aggregate-manifest":
        from vitruvius.laws_readiness import build_laws_completed_aggregate_manifest
        return _run(
            "build-laws-completed-aggregate-manifest",
            lambda: build_laws_completed_aggregate_manifest(
                out_path=args.out,
            ),
        )

    if args.command == "run-laws-completed-aggregate":
        from vitruvius.laws_readiness import run_laws_completed_aggregate
        return _run(
            "run-laws-completed-aggregate",
            lambda: run_laws_completed_aggregate(
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
            ),
        )

    if args.command == "refine-one":
        from vitruvius.normalization.refine import run_refine_one
        return _run(
            "refine-one",
            lambda: run_refine_one(relative_markdown_path=args.relative_markdown_path),
        )

    if args.command == "rotate-registries":
        from vitruvius.registry_rotation import run_rotate_registries
        return _run(
            "rotate-registries",
            lambda: run_rotate_registries(keep=args.keep, dry_run=args.dry_run),
        )

    if args.command == "build-graph":
        from vitruvius.graph.cli import run_build_graph
        return _run(
            "build-graph",
            lambda: run_build_graph(
                dry_run=args.dry_run,
                dataset_manifest=args.dataset_manifest,
            ),
        )

    if args.command == "query-graph":
        from vitruvius.graph.cli import run_query_graph
        return _run(
            "query-graph",
            lambda: run_query_graph(
            from_id=args.from_id,
            to_id=args.to_id,
            max_depth=args.max_depth,
            snapshot_path=args.snapshot_path,
            ),
        )

    if args.command == "export-graph-snapshot":
        from vitruvius.graph.cli import run_export_graph_snapshot
        return _run(
            "export-graph-snapshot",
            lambda: run_export_graph_snapshot(
                fmt=args.fmt,
                snapshot_path=args.snapshot_path,
            ),
        )

    if args.command == "export-graph-owl":
        from vitruvius.ontology.cli import run_export_graph_owl
        return _run(
            "export-graph-owl",
            lambda: run_export_graph_owl(
                snapshot_path=args.snapshot_path,
                out_path=args.out_path,
            ),
        )

    if args.command == "visualize-graph":
        from vitruvius.config import is_kg_enabled
        from vitruvius.graph.visualize import run_visualize_graph
        if args.vis_version == "v2" and not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml to visualize v2 snapshots.")
            return 1
        return _run(
            "visualize-graph",
            lambda: run_visualize_graph(
                snapshot_path=args.snapshot_path,
                out_path=args.out_path,
                version=args.vis_version,
            ),
        )

    if args.command == "ingest-spatial":
        from vitruvius.spatial.cli import run_ingest_spatial
        return _run("ingest-spatial", run_ingest_spatial)

    if args.command == "kg-ingest-evidence":
        from vitruvius.config import (
            get_kg_neo4j_uri,
            get_kg_neo4j_user,
            get_kg_neo4j_password,
            get_kg_postgres_conninfo,
            is_kg_enabled,
        )
        from vitruvius.kg.evidence_ingestor import EvidenceIngestor
        from vitruvius.kg.neo4j_client import Neo4jClient
        from vitruvius.kg.postgres_client import PostgresClient
        from vitruvius.paths import get_repo_root

        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.config import is_kg_evidence_graph
        if not is_kg_evidence_graph():
            print("ERROR: kg_transition.evidence_graph is false. Set it to true to ingest evidence.")
            return 1

        neo4j = Neo4jClient(
            uri=get_kg_neo4j_uri(),
            user=get_kg_neo4j_user(),
            password=get_kg_neo4j_password(),
        )
        postgres = PostgresClient(conninfo=get_kg_postgres_conninfo())
        ingestor = EvidenceIngestor(
            neo4j=neo4j,
            postgres=postgres,
            raw_source_root=get_repo_root() / "001_Raw-Source-Layer",
        )
        neo4j.init_schema()
        try:
            doc_version = ingestor.ingest(
                source_path=Path(args.source_path),
                parser_id=args.parser_id,
                parser_version=args.parser_version,
            )
            print(f"Ingested document version: {doc_version.id}")
            return 0
        except Exception as exc:
            print(f"ERROR: {exc}")
            return 1
        finally:
            neo4j.close()
            postgres.close()

    if args.command == "evaluate-spatial":
        from vitruvius.spatial.cli import run_evaluate_spatial
        return _run(
            "evaluate-spatial",
            lambda: run_evaluate_spatial(
            concepts=args.concepts,
            observations_path=args.observations_path,
            rules_path=args.rules_path,
            ),
        )

    if args.command == "ple-cotrace-dump":
        from vitruvius.review.cot_audit import run_ple_cotrace_dump
        return _run(
            "ple-cotrace-dump",
            lambda: run_ple_cotrace_dump(cot_dir=Path(args.cot_dir)),
        )

    if args.command == "ple-registry-purge":
        from vitruvius.review.stateful_registry import run_ple_registry_purge
        return _run(
            "ple-registry-purge",
            lambda: run_ple_registry_purge(
            db_path=Path(args.registry_db),
            days=args.days,
            ),
        )

    if args.command == "ple-vision-probe":
        from vitruvius.parsers.vision_ocr import run_ple_vision_probe
        return _run(
            "ple-vision-probe",
            lambda: run_ple_vision_probe(
            required_free_gb=args.required_free_gb,
            model=args.model,
            ),
        )

    if args.command == "query":
        from vitruvius.query.cli import run_query
        return _run(
            "query",
            lambda: run_query(args.question, snapshot_path=args.snapshot_path),
        )

    if args.command == "query-structured":
        from vitruvius.query.cli import run_query_structured
        return _run(
            "query-structured",
            lambda: run_query_structured(
            function=args.function,
            subject=args.subject,
            a=args.a,
            b=args.b,
            snapshot_path=args.snapshot_path,
            ),
        )

    if args.command == "kg-backfill-evidence":
        from vitruvius.config import is_kg_assertion_layer, is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        if not is_kg_assertion_layer():
            print("ERROR: kg_transition.assertion_layer is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.evidence_materializer import EvidenceMaterializer
        from vitruvius.paths import get_repo_root

        materializer = EvidenceMaterializer(get_repo_root())
        snapshot = materializer.materialize_all()
        path = materializer.write_snapshot()
        print(f"Wrote evidence snapshot: {path}")
        print(json.dumps(snapshot.entity_counts(), indent=2))
        if materializer._warnings:
            print(f"Warnings ({len(materializer._warnings)}):")
            for w in materializer._warnings[:10]:
                print(f"  - {w}")
        return 0

    if args.command == "kg-seed-taxonomy":
        from vitruvius.config import is_kg_enabled, is_kg_taxonomy_seeding
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        if not is_kg_taxonomy_seeding():
            print("ERROR: kg_transition.taxonomy_seeding is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.evidence_materializer import TaxonomyLoader
        from vitruvius.paths import get_repo_root

        loader = TaxonomyLoader(get_repo_root())
        snapshot = loader.load_all()
        path = loader.write_snapshot()
        print(f"Wrote taxonomy snapshot: {path}")
        print(json.dumps(snapshot.entity_counts(), indent=2))
        if loader._warnings:
            print(f"Warnings ({len(loader._warnings)}):")
            for w in loader._warnings[:10]:
                print(f"  - {w}")
        return 0

    if args.command == "kg-extract-candidates":
        from vitruvius.config import is_kg_enabled
        from vitruvius.kg.candidate_store import CandidateStore
        from vitruvius.kg.extraction_engine import ExtractionEngine
        from vitruvius.kg.json_evidence_store import KgV2Snapshot
        from vitruvius.kg.query_engine import QueryEngine
        from vitruvius.llm.structured_client import StructuredLLMClient
        from vitruvius.paths import get_repo_root

        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.config import is_kg_structured_extraction
        if not is_kg_structured_extraction():
            print("ERROR: kg_transition.structured_extraction is false. Set it to true to extract candidates.")
            return 1

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_snapshot.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        snapshot = KgV2Snapshot.read(Path(snap_path))
        unit_types = [t.strip() for t in args.unit_types.split(",") if t.strip()]
        run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        llm = StructuredLLMClient(
            backend="ollama",
            ollama_model="qwen2.5:3b",
            max_retries=2,
            timeout_seconds=120,
        )
        engine = ExtractionEngine(llm=llm)
        results = engine.extract_from_snapshot(
            snapshot=snapshot,
            unit_types=unit_types,
            run_id=run_id,
        )

        store = CandidateStore(
            base_dir=Path(args.out_dir) if args.out_dir else None
        )
        path = store.save(results, run_id=run_id)
        print(f"Wrote {len(results)} extraction results to {path}")
        total_candidates = sum(len(r.candidates) for r in results)
        print(f"Total candidates extracted: {total_candidates}")
        return 0

    if args.command == "kg-canonicalize-candidates":
        from vitruvius.config import is_kg_enabled
        from vitruvius.kg.canonical_store import CanonicalStore
        from vitruvius.kg.canonicalizer import Canonicalizer
        from vitruvius.kg.candidate_store import CandidateStore
        from vitruvius.kg.merge_adjudicator import MergeAdjudicator
        from vitruvius.kg.placement_engine import PlacementEngine
        from vitruvius.paths import get_repo_root

        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1

        cand_path = args.candidates
        if cand_path is None:
            cand_dir = get_repo_root() / "006_System-Manifests" / "runs" / "kg_candidates"
            candidates = sorted(cand_dir.glob("*_kg_candidates.jsonl"), reverse=True)
            if not candidates:
                print(f"ERROR: No candidate file found in {cand_dir}")
                return 1
            cand_path = candidates[0]

        run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        # Load all candidates
        cand_store = CandidateStore()
        all_results = cand_store.load(Path(cand_path))
        all_candidates = []
        for result in all_results:
            all_candidates.extend(result.candidates)

        if not all_candidates:
            print("WARNING: No candidates found in input file.")
            return 0

        # Phase 3a: Canonicalize
        canonicalizer = Canonicalizer()
        nodes = canonicalizer.canonicalize(all_candidates)
        print(f"Canonicalized {len(all_candidates)} candidates into {len(nodes)} nodes")

        # Phase 3b: Placement
        # Build taxonomy nodes from existing snapshot (if available)
        from vitruvius.kg.json_evidence_store import KgV2Snapshot
        from vitruvius.kg.schemas import TaxonomyNode

        tax_nodes: list[TaxonomyNode] = []
        snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
        snap_candidates = sorted(snap_dir.glob("*_kg_v2_taxonomy.json"), reverse=True)
        if snap_candidates:
            tax_snapshot = KgV2Snapshot.read(snap_candidates[0])
            for cn in tax_snapshot.canonical_nodes:
                if cn.type.value == "taxonomy":
                    tax_nodes.append(
                        TaxonomyNode(
                            id=cn.id,
                            path=cn.taxonomy_path or [cn.slug],
                            label=cn.label,
                            embedding=None,
                        )
                    )

        placement_engine = PlacementEngine(tax_nodes)
        placements: list[PlacementAssertion] = []
        from vitruvius.kg.schemas import PlacementAssertion
        from vitruvius.kg.enums import ValidationState

        for node in nodes:
            paths = placement_engine.place(node)
            for path in paths:
                parent_id = None
                for tn in tax_nodes:
                    if "/".join(tn.path) == path:
                        parent_id = tn.id
                        break
                if parent_id is None:
                    print(f"WARN: Could not resolve taxonomy parent for node {node.id} path '{path}' — skipping placement")
                    continue
                # Propagate node evidence into placement assertion
                node_evidence = [
                    eid for eid in (node.primary_assertion_id or "").split(",")
                    if eid
                ] or []
                placements.append(
                    PlacementAssertion(
                        id=f"assert-placement-{node.id}-to-{parent_id}",
                        node_id=node.id,
                        parent_node_id=parent_id,
                        reasoning_summary=f"Placed via {'rule' if node.type in placement_engine.RULE_PATHS else 'embedding'} strategy",
                        confidence=node.confidence,
                        validation_status=ValidationState.CANDIDATE,
                        evidence_ids=node_evidence,
                        created_at=datetime.now(timezone.utc).isoformat(),
                        version=1,
                    )
                )

        # Phase 3c: Merge adjudication
        merge_adjudicator = MergeAdjudicator()
        merges = merge_adjudicator.propose(nodes)
        print(f"Proposed {len(merges)} merge assertions")

        # Write output
        canonical_store = CanonicalStore(
            base_dir=Path(args.out_dir) if args.out_dir else None
        )
        out_path = canonical_store.save(nodes, placements, merges, run_id=run_id)
        print(f"Wrote canonicalization artifacts to {out_path}")
        return 0

    if args.command == "kg-materialize-canonical":
        from vitruvius.config import is_kg_enabled
        from vitruvius.kg.canonical_graph_builder import CanonicalGraphBuilder
        from vitruvius.paths import get_repo_root

        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.config import is_kg_assertion_layer
        if not is_kg_assertion_layer():
            print("ERROR: kg_transition.assertion_layer is false. Set it to true to materialize canonical graph.")
            return 1

        # Resolve taxonomy snapshot
        tax_path = args.taxonomy_snapshot
        if tax_path is None:
            tax_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            tax_candidates = sorted(tax_dir.glob("*_kg_v2_taxonomy.json"), reverse=True)
            if not tax_candidates:
                print(f"ERROR: No taxonomy snapshot found in {tax_dir}")
                return 1
            tax_path = tax_candidates[0]

        # Resolve canonical JSONL
        canonical_path = args.canonical_jsonl
        if canonical_path is None:
            canonical_dir = get_repo_root() / "006_System-Manifests" / "runs" / "kg_canonical"
            canonical_candidates = sorted(canonical_dir.glob("*_kg_canonical.jsonl"), reverse=True)
            if not canonical_candidates:
                print(f"ERROR: No canonical JSONL found in {canonical_dir}")
                return 1
            canonical_path = canonical_candidates[0]

        builder = CanonicalGraphBuilder()
        builder.load_taxonomy_snapshot(Path(tax_path))
        builder.load_canonical_jsonl(Path(canonical_path))
        snapshot = builder.build()

        out_path = builder.write_snapshot(Path(args.out_path) if args.out_path else None)
        print(f"Wrote unified canonical snapshot to {out_path}")
        counts = snapshot.entity_counts()
        for key, count in counts.items():
            print(f"  {key}: {count}")
        if builder._warnings:
            print(f"Warnings ({len(builder._warnings)}):")
            for w in builder._warnings[:10]:
                print(f"  - {w}")
        return 0

    if args.command == "kg-dematerialize-edge":
        from vitruvius.config import is_kg_assertion_layer, is_kg_enabled
        from vitruvius.kg.json_evidence_store import KgV2Snapshot
        from vitruvius.paths import get_repo_root

        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false.")
            return 1
        if not is_kg_assertion_layer():
            print("ERROR: kg_transition.assertion_layer is false.")
            return 1

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        snapshot = KgV2Snapshot.read(Path(snap_path))
        original_count = len(snapshot.fast_edges)
        snapshot.fast_edges = [
            e for e in snapshot.fast_edges
            if e.get("assertion_id") != args.assertion_id
        ]
        removed = original_count - len(snapshot.fast_edges)

        out_path = Path(args.out_path) if args.out_path else Path(snap_path)
        snapshot.write(out_path)
        print(f"Dematerialized {removed} edge(s) for assertion {args.assertion_id}")
        print(f"Wrote snapshot ({len(snapshot.fast_edges)} edges) to {out_path}")
        return 0

    if args.command == "kg-validate-assertions":
        from vitruvius.config import is_kg_assertion_layer, is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        if not is_kg_assertion_layer():
            print("ERROR: kg_transition.assertion_layer is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.assertion_validator import AssertionValidator
        from vitruvius.kg.json_evidence_store import KgV2Snapshot
        from vitruvius.paths import get_repo_root

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        snap = KgV2Snapshot.read(Path(snap_path))

        # Build indexes for validation
        canonical_index = {
            n.id: {"type": n.type.value, "status": n.status.value}
            for n in snap.canonical_nodes
        }
        evidence_index = {e.id: {"id": e.id} for e in snap.evidence_spans}
        placement_index = {
            p.node_id: p.parent_node_id for p in snap.placement_assertions
        }
        merge_index = {
            m.from_node_id: m.to_node_id for m in snap.merge_assertions
        }

        validator = AssertionValidator(
            canonical_index=canonical_index,
            evidence_index=evidence_index,
            placement_index=placement_index,
            merge_index=merge_index,
        )

        total = 0
        passed = 0
        for assertion in snap.relationship_assertions:
            result = validator.validate_relationship(assertion)
            total += 1
            if result.passed:
                passed += 1
            else:
                print(f"FAIL {assertion.id}: {'; '.join(result.errors)}")

        for assertion in snap.placement_assertions:
            result = validator.validate_placement(assertion)
            total += 1
            if result.passed:
                passed += 1
            else:
                print(f"FAIL {assertion.id}: {'; '.join(result.errors)}")

        for assertion in snap.merge_assertions:
            result = validator.validate_merge(assertion)
            total += 1
            if result.passed:
                passed += 1
            else:
                print(f"FAIL {assertion.id}: {'; '.join(result.errors)}")

        print(f"Validated {total} assertions: {passed} passed, {total - passed} failed")
        return 0

    if args.command == "kg-detect-contradictions":
        from vitruvius.config import is_kg_assertion_layer, is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        if not is_kg_assertion_layer():
            print("ERROR: kg_transition.assertion_layer is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.contradiction_detector import ContradictionDetector
        from vitruvius.kg.json_evidence_store import KgV2Snapshot
        from vitruvius.paths import get_repo_root

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        snap = KgV2Snapshot.read(Path(snap_path))
        detector = ContradictionDetector()
        issues = detector.detect(snap.relationship_assertions)

        if not issues:
            print("No contradictions detected.")
            return 0

        critical = sum(1 for i in issues if i.severity == "critical")
        warning = sum(1 for i in issues if i.severity == "warning")
        print(f"Detected {len(issues)} issues ({critical} critical, {warning} warning):")
        for issue in issues:
            print(f"  [{issue.severity.upper()}] {issue.pattern}: {issue.description}")
            print(f"    Assertions: {', '.join(issue.assertion_ids)}")
            print(f"    Suggested action: {issue.suggested_action}")
        return 0

    if args.command == "kg-build-unified":
        from vitruvius.config import is_kg_enabled
        from vitruvius.kg.unified_snapshot_builder import UnifiedSnapshotBuilder
        from vitruvius.paths import get_repo_root

        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1

        builder = UnifiedSnapshotBuilder(repo_root=get_repo_root())
        snapshot = builder.build()
        out_path = builder.write_snapshot(
            snapshot=snapshot,
            out_path=Path(args.out_path) if args.out_path else None,
        )
        print(f"Wrote unified snapshot to {out_path}")
        counts = snapshot.entity_counts()
        for key, count in counts.items():
            print(f"  {key}: {count}")
        if builder._warnings:
            print(f"Warnings ({len(builder._warnings)}):")
            for w in builder._warnings[:10]:
                print(f"  - {w}")
        return 0

    if args.command == "kg-enrich-relationships":
        from datetime import datetime, timezone

        from vitruvius.config import (
            get_kg_neo4j_password,
            get_kg_neo4j_uri,
            get_kg_neo4j_user,
            is_kg_enabled,
        )
        from vitruvius.kg.json_evidence_store import KgV2Snapshot
        from vitruvius.kg.neo4j_client import Neo4jClient
        from vitruvius.kg.neo4j_loader import Neo4jLoader
        from vitruvius.kg.relationship_enricher import enrich_snapshot
        from vitruvius.paths import get_repo_root

        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1

        repo_root = get_repo_root()
        snap_dir = repo_root / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
        snap_path = Path(args.snapshot) if args.snapshot else None
        if snap_path is None:
            candidates = sorted(snap_dir.glob("*_kg_v2_unified*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No unified snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        snapshot = KgV2Snapshot.read(snap_path)
        report = enrich_snapshot(
            snapshot,
            max_new_assertions=args.max_new_assertions,
            repo_root=repo_root,
        )

        print("Relationship enrichment report:")
        print(f"  input snapshot: {snap_path}")
        print(f"  rule-evidence candidate pairs: {report.candidate_pair_count}")
        print(f"  source-reference candidate pairs: {report.source_pair_count}")
        print(f"  added assertions: {report.added_assertion_count}")
        print(f"  added source support: {report.added_source_support_count}")
        print(f"  semantic assertions: {report.semantic_assertion_count}")
        print(f"  skipped existing: {report.skipped_existing_count}")
        print(f"  added by type: {report.added_by_type}")

        if args.dry_run:
            print("[DRY-RUN] Enriched snapshot not written.")
            return 0

        if args.out_path:
            out_path = Path(args.out_path)
        else:
            run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            out_path = snap_dir / f"{run_id}_kg_v2_unified_enriched.json"
        snapshot.write(out_path)
        print(f"Wrote enriched snapshot to {out_path}")

        if not args.load_neo4j:
            return 0

        client = Neo4jClient(
            uri=get_kg_neo4j_uri(),
            user=get_kg_neo4j_user(),
            password=get_kg_neo4j_password(),
        )
        try:
            if not client.verify_connectivity() and args.ensure_neo4j:
                from vitruvius.kg.neo4j_manager import ensure_neo4j_running

                ensure_neo4j_running(wait_seconds=30)
            if not client.verify_connectivity():
                print("ERROR: Neo4j is not reachable.")
                return 1
            if args.clear_neo4j:
                client.run("MATCH (n) DETACH DELETE n")
                print("Cleared Neo4j before enriched snapshot load.")
            client.init_schema()
            load_result = Neo4jLoader(snapshot).load(client)
            print(f"Neo4j load result: {load_result}")
            return 0 if load_result.get("error_count", 0) == 0 else 1
        finally:
            client.close()

    if args.command == "kg-review-queue":
        from vitruvius.config import is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.query_engine import QueryEngine
        from vitruvius.paths import get_repo_root

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        engine = QueryEngine.from_path(snap_path)
        target_status = args.status.lower()
        rows: list[tuple[str, str, str, float, str]] = []

        # Relationship assertions
        for assertion in engine.snapshot.relationship_assertions:
            if assertion.validation_status.value.lower() == target_status:
                rows.append(
                    (
                        assertion.id,
                        assertion.from_node_id,
                        assertion.to_node_id,
                        assertion.confidence,
                        assertion.reasoning_summary.replace("\n", " ")[:60],
                    )
                )
        # Placement assertions
        for assertion in engine.snapshot.placement_assertions:
            if assertion.validation_status.value.lower() == target_status:
                rows.append(
                    (
                        assertion.id,
                        assertion.node_id,
                        assertion.parent_node_id,
                        assertion.confidence,
                        assertion.reasoning_summary.replace("\n", " ")[:60],
                    )
                )
        # Merge assertions
        for assertion in engine.snapshot.merge_assertions:
            if assertion.validation_status.value.lower() == target_status:
                rows.append(
                    (
                        assertion.id,
                        assertion.from_node_id,
                        assertion.to_node_id,
                        assertion.confidence,
                        assertion.reasoning_summary.replace("\n", " ")[:60],
                    )
                )
        if not rows:
            print(f"No assertions with status '{args.status}'.")
            return 0
        print(f"{'ID':<40} {'From/Node':<30} {'To/Parent':<30} {'Conf':>6} {'Reasoning'}")
        print("-" * 130)
        for rid, from_n, to_n, conf, reason in rows:
            print(f"{rid:<40} {from_n:<30} {to_n:<30} {conf:>6.2f} {reason}")
        print(f"\nTotal: {len(rows)} assertion(s)")
        return 0

    if args.command == "kg-review-action":
        from vitruvius.config import is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.enums import ValidationState
        from vitruvius.kg.json_evidence_store import KgV2Snapshot
        from vitruvius.paths import get_repo_root

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        snap = KgV2Snapshot.read(Path(snap_path))
        matched = False
        all_assertions = (
            snap.relationship_assertions
            + snap.placement_assertions
            + snap.merge_assertions
        )
        for assertion in all_assertions:
            if assertion.id == args.assertion_id:
                matched = True
                if args.action == "approve":
                    assertion.validation_status = ValidationState.VALIDATED
                elif args.action == "reject":
                    assertion.validation_status = ValidationState.REJECTED
                else:  # escalate
                    assertion.validation_status = ValidationState.REVIEW_REQUIRED
                # Add reasoning detail if RelationshipAssertion supports it
                if hasattr(assertion, "reasoning_detail") and args.reason:
                    assertion.reasoning_detail.append(f"[{args.action}] {args.reason}")
                break

        if not matched:
            print(f"ERROR: Assertion '{args.assertion_id}' not found in snapshot.")
            return 1

        snap.write(Path(snap_path))
        print(f"Updated {args.assertion_id} -> {args.action}")
        return 0

    if args.command == "kg-inspect-node":
        from vitruvius.config import is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.query_engine import QueryEngine
        from vitruvius.paths import get_repo_root

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        engine = QueryEngine.from_path(snap_path)
        node = engine.get_node_by_id(args.node_id)
        if node is None:
            print(f"ERROR: Node '{args.node_id}' not found.")
            return 1

        print(f"Node: {node.id}")
        print(f"  Type: {node.type.value}")
        print(f"  Label: {node.label}")
        print(f"  Slug: {node.slug}")
        print(f"  Summary: {node.summary[:200]}..." if len(node.summary) > 200 else f"  Summary: {node.summary}")
        print(f"  Taxonomy path: {' / '.join(node.taxonomy_path) if node.taxonomy_path else '(none)'}")
        print(f"  Status: {node.status.value}")
        print(f"  Confidence: {node.confidence}")
        print(f"  Aliases: {', '.join(node.aliases) if node.aliases else '(none)'}")

        placements = engine.get_placement_for_node(node.id)
        if placements:
            print(f"\n  Placements ({len(placements)}):")
            for p in placements:
                print(f"    -> {p.parent_node_id} ({p.validation_status.value}, conf={p.confidence})")

        neighbors = engine.get_node_neighborhood(node.id)
        if neighbors:
            print(f"\n  Related nodes ({len(neighbors)}):")
            for other, assertion in neighbors:
                print(f"    -> {other.id} [{assertion.edge_type.value if hasattr(assertion, 'edge_type') else 'BELONGS_TO'}] {assertion.reasoning_summary[:60]}")

        evidence = engine.get_evidence_for_node(node.id)
        if evidence:
            print(f"\n  Evidence spans ({len(evidence)}):")
            for span in evidence:
                print(f"\n    ── [{span.id}] ──")
                print(f"       Document: {span.document_id}")
                print(f"       Quote:    {span.quote[:100]}...")
                print(f"       Deep link: {span.deep_link or '(none)'}")
                sel = span.selector
                if hasattr(sel, "kind"):
                    print(f"       Selector: {sel.kind}")
                    if sel.kind == "markdown_range" and hasattr(sel, "heading_path"):
                        print(f"         Heading path: {' > '.join(sel.heading_path)}")
                    if sel.kind == "pdf_page" and hasattr(sel, "page"):
                        print(f"         Page: {sel.page}")

        merges = engine.get_merge_assertions_for_node(node.id)
        if merges:
            print(f"\n  Merge proposals ({len(merges)}):")
            for m in merges:
                direction = "->" if m.from_node_id == node.id else "<-"
                other = m.to_node_id if m.from_node_id == node.id else m.from_node_id
                print(f"    {direction} {other} ({m.validation_status.value})")
        return 0

    if args.command == "kg-inspect-assertion":
        from vitruvius.config import is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.query_engine import QueryEngine
        from vitruvius.paths import get_repo_root

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        engine = QueryEngine.from_path(snap_path)
        assertion = engine.get_assertion_by_id(args.assertion_id)
        if assertion is None:
            print(f"ERROR: Assertion '{args.assertion_id}' not found.")
            return 1

        print(f"Assertion: {assertion.id}")
        print(f"  Type: {type(assertion).__name__}")
        print(f"  Confidence: {assertion.confidence}")
        print(f"  Status: {assertion.validation_status.value}")
        print(f"  Reasoning: {assertion.reasoning_summary}")

        if hasattr(assertion, "edge_type"):
            print(f"  Edge type: {assertion.edge_type.value}")
        if hasattr(assertion, "inference_type"):
            print(f"  Inference type: {assertion.inference_type.value}")
            print(f"    -> {'Direct citation' if assertion.inference_type.value == 'direct_citation' else 'Multi-hop inference' if assertion.inference_type.value == 'multi_hop_inference' else 'Human authored' if assertion.inference_type.value == 'human_authored' else assertion.inference_type.value}")
        if hasattr(assertion, "from_node_id"):
            print(f"  From: {assertion.from_node_id}")
        if hasattr(assertion, "to_node_id"):
            print(f"  To: {assertion.to_node_id}")
        if hasattr(assertion, "node_id"):
            print(f"  Node: {assertion.node_id}")
        if hasattr(assertion, "parent_node_id"):
            print(f"  Parent: {assertion.parent_node_id}")
        if hasattr(assertion, "created_by"):
            cb = assertion.created_by
            print(f"  Created by:")
            print(f"    Mode: {cb.mode}")
            print(f"    Model: {cb.model or '(none)'}")
            print(f"    Pipeline stage: {cb.pipeline_stage}")
            print(f"    Run ID: {cb.run_id or '(none)'}")
        if hasattr(assertion, "review_state"):
            print(f"  Review state: {assertion.review_state}")

        evidence = engine.get_evidence_for_assertion(assertion.id)
        if evidence:
            print(f"\n  Evidence spans ({len(evidence)}):")
            for span in evidence:
                print(f"\n    ── [{span.id}] ──")
                print(f"       Document: {span.document_id}")
                print(f"       Version:  {span.document_version_id}")
                print(f"       Quote:    {span.quote[:120]}...")
                print(f"       Deep link: {span.deep_link or '(none)'}")
                print(f"       Parser:   {span.parser} {span.parser_version or ''}")
                print(f"       Checksum: {span.checksum[:16]}...")
                sel = span.selector
                if hasattr(sel, "kind"):
                    print(f"       Selector: {sel.kind}")
                    if sel.kind == "markdown_range" and hasattr(sel, "heading_path"):
                        print(f"         Heading path: {' > '.join(sel.heading_path)}")
                    if sel.kind == "pdf_page" and hasattr(sel, "page"):
                        print(f"         Page: {sel.page}")
                    if sel.kind == "pdf_bbox" and hasattr(sel, "page"):
                        print(f"         Page: {sel.page}, BBox: {sel.bbox}")
                    if hasattr(sel, "char_start"):
                        print(f"         Char range: {sel.char_start}-{sel.char_end}")
        else:
            print("\n  Evidence spans: none")
        return 0

    if args.command == "kg-query-nodes":
        from vitruvius.config import is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.query_engine import QueryEngine
        from vitruvius.paths import get_repo_root

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        engine = QueryEngine.from_path(snap_path)
        results = engine.search_nodes_by_label(args.query, limit=args.limit)
        if not results:
            print(f"No nodes matching '{args.query}'")
            return 0

        for node in results:
            print(f"{node.id} [{node.type.value}] {node.label}")
            if node.summary:
                print(f"  Summary: {node.summary[:120]}...")
        return 0

    if args.command == "kg-query-neighborhood":
        from vitruvius.config import is_kg_enabled
        if not is_kg_enabled():
            print("ERROR: kg_transition.enabled is false. Set it to true in config/vitruvius.yaml")
            return 1
        from vitruvius.kg.query_engine import QueryEngine
        from vitruvius.paths import get_repo_root

        snap_path = args.snapshot
        if snap_path is None:
            snap_dir = get_repo_root() / "005_Operational-Intelligence-Layer" / "graph" / "kg-v2"
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if not candidates:
                print(f"ERROR: No snapshot found in {snap_dir}")
                return 1
            snap_path = candidates[0]

        engine = QueryEngine.from_path(snap_path)
        neighbors = engine.get_node_neighborhood(args.node_id)
        if not neighbors:
            print(f"No neighbors found for '{args.node_id}'")
            return 0

        print(f"Neighborhood of {args.node_id}:")
        for node, assertion in neighbors:
            print(f"  -> {node.id} [{node.type.value}] {node.label}")
            print(f"    Assertion: {assertion.id} ({assertion.edge_type.value})")
            print(f"    Reason: {assertion.reasoning_summary[:120]}...")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
