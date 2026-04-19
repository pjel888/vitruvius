"""Evidence graph materializer — file-native v2-alpha snapshot builder.

Builds ``DocumentVersion → Section → Chunk → EvidenceSpan`` chains from the
existing canonical layer (``003_Canonical-Knowledge-Layer/shared/``) and writes
a deterministic JSON snapshot.

No Neo4j or PostgreSQL is required.  When those are provisioned, this snapshot
becomes the rebuild source of truth.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError as PydanticValidationError

from vitruvius.normalization.ast_chunker import split_into_chunks

from .assertion_validator import AssertionValidator
from .edge_materializer import EdgeMaterializer
from .enums import EdgeType, InferenceType, ValidationState
from .json_evidence_store import KgV2Snapshot
from .pdf_evidence_locator import PdfEvidenceLocator
from .schemas import (
    CanonicalNode,
    Chunk,
    CreatedBy,
    DocumentVersion,
    EvidenceSpan,
    MarkdownRangeSelector,
    PdfBboxSelector,
    PdfPageSelector,
    PlacementAssertion,
    RelationshipAssertion,
    Section,
    TextRangeSelector,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _to_iso_string(value: Any) -> str:
    if value is None:
        return _now_utc()
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return str(value)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _serialize_yaml_dates(obj: Any) -> Any:
    """Recursively convert datetime objects to ISO-8601 strings."""
    from datetime import date, datetime

    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _serialize_yaml_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize_yaml_dates(v) for v in obj]
    return obj


def _load_frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    try:
        data = yaml.safe_load(text[3:end].strip())
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return _serialize_yaml_dates(data)


def _load_markdown_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4 :].lstrip("\n")


def _slug_from_id(entity_id: str) -> str:
    """Strip known prefixes to produce a slug."""
    for prefix in ("law-", "irr-", "source-", "handout-", "concept-", "rel-", "taxonomy-"):
        if entity_id.startswith(prefix):
            return entity_id[len(prefix) :]
    return entity_id


def _edge_type_from_string(value: str) -> EdgeType:
    """Map legacy relationship_type strings to EdgeType enum.

    The legacy registry allows: governs, requires, defines, depends_on,
    limits, affects, supersedes.
    """
    mapping = {
        "governs": EdgeType.APPLIES_TO,
        "requires": EdgeType.REQUIRES,
        "defines": EdgeType.DEFINED_BY,
        "depends_on": EdgeType.DEPENDS_ON,
        "limits": EdgeType.REQUIRES,
        "affects": EdgeType.RELATED_TO,
        "supersedes": EdgeType.OVERRIDES,
    }
    return mapping.get(value.lower(), EdgeType.RELATED_TO)


def _infer_inference_type(rel_type: str, evidence_list: list[dict]) -> InferenceType:
    """Classify how an assertion was derived from its relationship type and evidence."""
    rel = rel_type.lower()
    # Direct definitional language → direct citation
    if rel == "defines":
        return InferenceType.DIRECT_CITATION
    # Governance/requirement language with explicit section anchors → direct citation
    if rel in ("governs", "requires", "limits") and evidence_list:
        for ev in evidence_list:
            snippet = ev.get("evidence_snippet", "")
            if any(keyword in snippet.lower() for keyword in ("shall", "must", "shall not", "required")):
                return InferenceType.DIRECT_CITATION
    # Taxonomic hierarchy → taxonomy placement
    if rel in ("depends_on", "part_of"):
        return InferenceType.TAXONOMY_PLACEMENT
    # Multi-hop or inferred relationships
    if rel == "affects":
        return InferenceType.MULTI_HOP_INFERENCE
    # Default: if it came through the promotion pipeline with reviewer evidence, treat as human authored
    if evidence_list:
        return InferenceType.HUMAN_AUTHORED
    return InferenceType.RULE_BASED_DERIVATION


def _validation_state_from_string(value: str | None) -> ValidationState:
    if value in ("verified", "validated"):
        return ValidationState.VALIDATED
    if value == "promoted":
        return ValidationState.CANDIDATE
    if value == "draft":
        return ValidationState.REVIEW_REQUIRED
    if value == "rejected":
        return ValidationState.REJECTED
    return ValidationState.CANDIDATE


# ---------------------------------------------------------------------------
# Materializer
# ---------------------------------------------------------------------------

class EvidenceMaterializer:
    """Builds a v2-alpha evidence graph from the canonical file layer."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root)
        self.canonical_root = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared"
        self.snapshot = KgV2Snapshot()
        self._warnings: list[str] = []
        self._pdf_locator = PdfEvidenceLocator(self.repo_root)

    # -- public API ---------------------------------------------------------

    def materialize_all(self) -> KgV2Snapshot:
        """Run the full materialization pipeline."""
        self._materialize_sources()
        self._materialize_relationships()
        self._materialize_fast_edges()
        self.snapshot.metadata = {
            "generator": "evidence_materializer",
            "version": "2.0.0-alpha",
            "warnings": self._warnings,
            "entity_counts": self.snapshot.entity_counts(),
        }
        return self.snapshot

    def write_snapshot(self, out_dir: Path | None = None) -> Path:
        """Write snapshot to disk and return the path."""
        if out_dir is None:
            out_dir = (
                self.repo_root
                / "005_Operational-Intelligence-Layer"
                / "graph"
                / "kg-v2"
            )
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = out_dir / f"{ts}_kg_v2_snapshot.json"
        self.snapshot.write(path)
        return path

    # -- source → DocumentVersion + Section + Chunk -------------------------

    def _materialize_sources(self) -> None:
        sources_dir = self.canonical_root / "sources"
        if not sources_dir.exists():
            self._warnings.append(f"Sources directory not found: {sources_dir}")
            return

        for md_path in sorted(sources_dir.rglob("*.md")):
            fm = _load_frontmatter(md_path)
            if not fm:
                self._warnings.append(f"No frontmatter: {md_path}")
                continue
            entity_id = fm.get("id")
            if not entity_id:
                self._warnings.append(f"Missing id in frontmatter: {md_path}")
                continue

            slug = _slug_from_id(entity_id)
            docv_id = f"docv-{slug}-v1"
            doc_id = f"doc-{slug}"

            # SHA-256 from canonical file content (raw source may not be available)
            body_text = _load_markdown_body(md_path)
            sha = _sha256_text(body_text)

            dv = DocumentVersion(
                id=docv_id,
                document_id=doc_id,
                title=fm.get("title", md_path.stem.replace("-", " ").title()),
                source_uri=str(md_path.relative_to(self.repo_root)),
                mime_type="text/markdown",
                sha256=sha,
                created_at=_now_utc(),
                supersedes=None,
            )
            self.snapshot.document_versions.append(dv)

            # Derive sections + chunks via ast_chunker
            full_text = md_path.read_text(encoding="utf-8")
            chunks = split_into_chunks(full_text, source_path=str(md_path), max_tokens=512)

            # Build sections from unique headings seen in chunks
            seen_sections: dict[str, Section] = {}
            for chunk in chunks:
                sec_key = chunk.heading or "__body__"
                if sec_key not in seen_sections:
                    sec_id = f"sec-{slug}-{len(seen_sections)}"
                    seen_sections[sec_key] = Section(
                        id=sec_id,
                        document_version_id=docv_id,
                        title=chunk.heading or "(body)",
                        level=2 if chunk.heading else 1,
                    )

            self.snapshot.sections.extend(seen_sections.values())

            # Map each chunk to a section
            section_lookup = {s.title: s for s in seen_sections.values()}
            for idx, chunk in enumerate(chunks):
                if not chunk.body.strip():
                    continue
                sec = section_lookup.get(chunk.heading or "(body)", seen_sections.get("__body__"))
                if sec is None:
                    sec = next(iter(seen_sections.values()))  # fallback
                self.snapshot.chunks.append(
                    Chunk(
                        id=f"chk-{slug}-{idx:04d}",
                        section_id=sec.id,
                        document_version_id=docv_id,
                        text=chunk.body,
                        char_start=0,
                        char_end=len(chunk.body),
                        token_count=max(1, chunk.token_count),
                    )
                )

    # -- relationships → EvidenceSpan + RelationshipAssertion ---------------

    def _materialize_relationships(self) -> None:
        rels_dir = self.canonical_root / "relationships"
        if not rels_dir.exists():
            self._warnings.append(f"Relationships directory not found: {rels_dir}")
            return

        for md_path in sorted(rels_dir.rglob("*.md")):
            fm = _load_frontmatter(md_path)
            if not fm:
                self._warnings.append(f"No frontmatter: {md_path}")
                continue

            rel_id = fm.get("id")
            if not rel_id or not rel_id.startswith("rel-"):
                self._warnings.append(f"Invalid relationship id: {md_path}")
                continue

            # Only materialize promoted/verified relationships
            status = fm.get("canonical_status", "")
            if status not in ("promoted", "verified"):
                continue

            from_entity = fm.get("from_entity") or fm.get("from_id")
            to_entity = fm.get("to_entity") or fm.get("to_id")
            rel_type = fm.get("relationship_type") or fm.get("predicate")
            if not from_entity or not to_entity or not rel_type:
                self._warnings.append(f"Incomplete relationship: {rel_id}")
                continue

            evidence_list = fm.get("evidence", [])
            if not isinstance(evidence_list, list):
                evidence_list = []

            # Pick primary evidence (highest confidence, longest snippet)
            primary_ev = None
            if evidence_list:
                scored = []
                for ev in evidence_list:
                    conf = float(ev.get("reviewer_confidence", 0.0))
                    snippet_len = len(ev.get("evidence_snippet", ""))
                    scored.append((conf, snippet_len, ev))
                scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
                primary_ev = scored[0][2]

            # Create EvidenceSpan for each evidence entry
            evidence_span_ids: list[str] = []
            for ev_idx, ev in enumerate(evidence_list):
                snippet = ev.get("evidence_snippet", "")
                if not snippet:
                    continue
                source_id = ev.get("source_id", from_entity)
                source_slug = _slug_from_id(source_id)
                span_id = f"span-{rel_id}-{ev_idx:03d}"
                evidence_span_ids.append(span_id)

                # Build selector: try PDF bbox first, then PDF page only,
                # then MarkdownRangeSelector, then fall back to TextRangeSelector.
                section_id = ev.get("source_section_id", "")
                pdf_bbox = self._pdf_locator.find_bbox_with_fallback(
                    source_slug, snippet, section_id
                )
                if pdf_bbox is not None:
                    page_num, bbox = pdf_bbox
                    selector = PdfBboxSelector(
                        kind="pdf_bbox",
                        page=page_num,
                        bbox=bbox,
                        quote=snippet,
                    )
                    deep_link = f"/viewer/{source_slug}?page={page_num}&bbox={','.join(str(c) for c in bbox)}"
                else:
                    pdf_page = self._pdf_locator.find_page_with_fallback(
                        source_slug, snippet, section_id
                    )
                    if pdf_page is not None:
                        selector = PdfPageSelector(
                            kind="pdf_page",
                            page=pdf_page,
                            quote=snippet,
                        )
                        deep_link = f"/viewer/{source_slug}?page={pdf_page}"
                    elif section_id:
                        selector = MarkdownRangeSelector(
                            kind="markdown_range",
                            heading_path=[section_id],
                            char_start=0,
                            char_end=len(snippet),
                        )
                        deep_link = f"/viewer/{source_slug}?section={section_id}"
                    else:
                        selector = TextRangeSelector(
                            kind="text_range",
                            quote=snippet,
                            char_start=0,
                            char_end=len(snippet),
                        )
                        deep_link = f"/viewer/{source_slug}"

                self.snapshot.evidence_spans.append(
                    EvidenceSpan(
                        id=span_id,
                        document_id=f"doc-{source_slug}",
                        document_version_id=f"docv-{source_slug}-v1",
                        selector=selector,
                        quote=snippet,
                        normalized_text=snippet,
                        deep_link=deep_link,
                        parser="legacy_promotion_pipeline",
                        parser_version="1.0.0",
                        ingestion_run_id=None,
                        checksum=_sha256_text(snippet),
                        created_at=_now_utc(),
                    )
                )

            # Confidence from frontmatter or primary evidence
            confidence = float(fm.get("confidence_score", 0.0))
            if confidence == 0.0 and primary_ev:
                confidence = float(primary_ev.get("reviewer_confidence", 0.0))

            reviewer_model = ""
            if primary_ev:
                reviewer_model = primary_ev.get("reviewer_model", "")

            self.snapshot.relationship_assertions.append(
                RelationshipAssertion(
                    id=f"assert-{rel_id}",
                    edge_type=_edge_type_from_string(rel_type),
                    from_node_id=from_entity,
                    to_node_id=to_entity,
                    reasoning_summary=fm.get("reviewer_reason", "")
                    or (primary_ev.get("reviewer_reason", "") if primary_ev else "")
                    or "Legacy promotion pipeline assertion",
                    reasoning_detail=[],
                    inference_type=_infer_inference_type(rel_type, evidence_list),
                    confidence=confidence,
                    validation_status=_validation_state_from_string(status),
                    created_by=CreatedBy(
                        mode="hybrid",
                        model=reviewer_model or None,
                        pipeline_stage="promotion",
                        run_id=fm.get("promotion_batch_id") or None,
                    ),
                    review_state="approved" if status == "verified" else "pending",
                    evidence_ids=evidence_span_ids,
                    document_version_ids=[],
                    created_at=_to_iso_string(fm.get("last_promoted_utc", _now_utc())),
                    updated_at=_now_utc(),
                    version=1,
                )
            )

    def _materialize_fast_edges(self) -> None:
        """Validate relationship assertions and materialize fast edges."""
        if not self.snapshot.relationship_assertions:
            return

        # Build indices from the snapshot for validation
        canonical_index: dict[str, dict[str, Any]] = {
            node.id: {"type": node.type, "status": node.status}
            for node in self.snapshot.canonical_nodes
        }
        # Also include document versions as valid endpoints (sources)
        for dv in self.snapshot.document_versions:
            canonical_index[dv.id] = {"type": "document_version", "status": "validated"}
            canonical_index[dv.document_id] = {"type": "document", "status": "validated"}
        # Also include concept files on disk (they may not be in snapshot.canonical_nodes yet)
        concepts_dir = self.canonical_root / "concepts"
        if concepts_dir.exists():
            for md_path in sorted(concepts_dir.rglob("*.md")):
                fm = _load_frontmatter(md_path)
                if fm:
                    entity_id = fm.get("id")
                    if entity_id:
                        canonical_index[entity_id] = {
                            "type": "concept",
                            "status": _validation_state_from_string(fm.get("canonical_status")),
                        }

        evidence_index: dict[str, dict[str, Any]] = {
            span.id: {"id": span.id}
            for span in self.snapshot.evidence_spans
        }

        validator = AssertionValidator(
            canonical_index=canonical_index,
            evidence_index=evidence_index,
        )

        passed_assertions: list[RelationshipAssertion] = []
        for assertion in self.snapshot.relationship_assertions:
            result = validator.validate_relationship(assertion)
            if result.passed:
                passed_assertions.append(assertion)

        if passed_assertions:
            materializer = EdgeMaterializer(snapshot=self.snapshot)
            materializer.materialize(passed_assertions, skip_unvalidated=False)
            self.snapshot.fast_edges = materializer.write_snapshot(out_path=None)["edges"]


# ---------------------------------------------------------------------------
# Taxonomy loader
# ---------------------------------------------------------------------------

class TaxonomyLoader:
    """Builds CanonicalNode records from existing concept files."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root)
        self.canonical_root = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared"
        self.snapshot = KgV2Snapshot()
        self._warnings: list[str] = []

    def load_all(self) -> KgV2Snapshot:
        """Walk concepts and taxonomy roots and create CanonicalNode records."""
        self._load_concepts()
        self._load_taxonomy_roots()

        self.snapshot.metadata = {
            "generator": "taxonomy_loader",
            "version": "2.0.0-alpha",
            "warnings": self._warnings,
            "entity_counts": self.snapshot.entity_counts(),
        }
        return self.snapshot

    def _load_concepts(self) -> None:
        concepts_dir = self.canonical_root / "concepts"
        if not concepts_dir.exists():
            self._warnings.append(f"Concepts directory not found: {concepts_dir}")
            return

        for md_path in sorted(concepts_dir.rglob("*.md")):
            fm = _load_frontmatter(md_path)
            if not fm:
                self._warnings.append(f"No frontmatter: {md_path}")
                continue

            entity_id = fm.get("id")
            if not entity_id:
                self._warnings.append(f"Missing id: {md_path}")
                continue

            # Derive taxonomy path: prefer explicit taxonomy_path field,
            # then fall back to legacy topic_tags / category for backward compatibility.
            taxonomy_path: list[str] = []
            explicit_path = fm.get("taxonomy_path", [])
            if isinstance(explicit_path, list) and explicit_path:
                taxonomy_path = [str(t) for t in explicit_path]
            else:
                topic_tags = fm.get("topic_tags", [])
                if isinstance(topic_tags, list):
                    taxonomy_path.extend(str(t) for t in topic_tags)
                category = fm.get("category", "")
                if category and str(category) not in taxonomy_path:
                    taxonomy_path.insert(0, str(category))
                if not taxonomy_path:
                    taxonomy_path = ["concepts"]

            # Aliases
            aliases = fm.get("aliases", [])
            if not isinstance(aliases, list):
                aliases = []

            # Summary: use definition if present, else placeholder
            body = _load_markdown_body(md_path)
            summary = ""
            def_match = re.search(r"^## Definition\s*\n(.*?)(?=^## |\Z)", body, re.MULTILINE | re.DOTALL)
            if def_match:
                summary = def_match.group(1).strip().replace("\n", " ")[:500]
            if not summary:
                summary = fm.get("definition", "")

            try:
                self.snapshot.canonical_nodes.append(
                    CanonicalNode(
                        id=entity_id,
                        type="concept",
                        label=fm.get("title", entity_id.replace("concept-", "").replace("-", " ").title()),
                        slug=_slug_from_id(entity_id),
                        summary=summary,
                        taxonomy_path=taxonomy_path,
                        aliases=[str(a) for a in aliases],
                        status=_validation_state_from_string(fm.get("canonical_status")),
                        confidence=float(fm.get("confidence_score", 0.0)),
                        version=1,
                        created_at=fm.get("last_canonicalized_utc", _now_utc()),
                        updated_at=fm.get("enriched_at_utc", _now_utc()),
                    )
                )
            except PydanticValidationError as exc:
                self._warnings.append(f"Invalid concept {entity_id}: {exc}")

    def _load_taxonomy_roots(self) -> None:
        taxonomy_dir = self.canonical_root / "taxonomy"
        if not taxonomy_dir.exists():
            self._warnings.append(f"Taxonomy directory not found: {taxonomy_dir}")
            return

        for md_path in sorted(taxonomy_dir.rglob("*.md")):
            fm = _load_frontmatter(md_path)
            if not fm:
                self._warnings.append(f"No frontmatter: {md_path}")
                continue

            entity_id = fm.get("id")
            if not entity_id:
                self._warnings.append(f"Missing id: {md_path}")
                continue

            # Taxonomy roots are their own path
            taxonomy_path = [entity_id.replace("taxonomy-", "")]

            try:
                self.snapshot.canonical_nodes.append(
                    CanonicalNode(
                        id=entity_id,
                        type="taxonomy",
                        label=fm.get("title", entity_id.replace("taxonomy-", "").replace("-", " ").title()),
                        slug=_slug_from_id(entity_id),
                        summary=fm.get("title", ""),
                        taxonomy_path=taxonomy_path,
                        aliases=[],
                        status=_validation_state_from_string(fm.get("canonical_status")),
                        confidence=1.0,
                        version=1,
                        created_at=_now_utc(),
                        updated_at=_now_utc(),
                    )
                )
            except PydanticValidationError as exc:
                self._warnings.append(f"Invalid taxonomy {entity_id}: {exc}")

    def write_snapshot(self, out_dir: Path | None = None) -> Path:
        if out_dir is None:
            out_dir = (
                self.repo_root
                / "005_Operational-Intelligence-Layer"
                / "graph"
                / "kg-v2"
            )
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = out_dir / f"{ts}_kg_v2_taxonomy.json"
        self.snapshot.write(path)
        return path
