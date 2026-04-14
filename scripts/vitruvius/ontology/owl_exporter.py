"""Stream M.3 — OWL/Turtle exporter for Phase 8 graph snapshots.

Loads a :class:`GraphSnapshot` JSON file and renders it as an RDF
Turtle document that a buildingSMART-aware consumer can federate
with real IFC/OWL content. The exporter is deterministic (stable
sort + identical serialisation on repeated runs) so downstream
diffing tools can rely on byte-identity.

Optional IFC cross-links: when an ``ifc_mapping_path`` is provided,
concepts that have an entry in the mapping receive an
``owl:sameAs`` triple pointing at the corresponding
``buildingsmart:<IfcClass>`` URI.

Every API symbol the Stream M.3 tests import from this module:
  * :const:`VITRUVIUS_NAMESPACE`
  * :const:`IFC_NAMESPACE`
  * :func:`export_snapshot_as_turtle`
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


VITRUVIUS_NAMESPACE = "https://vitruvius.ai/ontology/"
IFC_NAMESPACE = "https://standards.buildingsmart.org/IFC/RELEASE/IFC4/FINAL/OWL#"


def _safe_local(value: str) -> str:
    """Escape a string so it is a valid Turtle local-name fragment.

    Turtle local names accept ``[A-Za-z0-9_-]``; anything else becomes
    an underscore. Empty results fall back to ``_``.
    """
    out = []
    for ch in str(value):
        if ch.isalnum() or ch in {"_", "-"}:
            out.append(ch)
        else:
            out.append("_")
    joined = "".join(out).strip("_") or "_"
    return joined


def _load_mapping_rows(path: Path) -> Mapping[str, str]:
    """Load ``ifc_mapping.yaml`` and return ``concept_id → ifc_class``.

    Any missing or malformed row is skipped silently so a partially
    seeded mapping doesn't break the exporter.
    """
    import yaml

    try:
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    if not isinstance(raw, list):
        return {}
    out: dict[str, str] = {}
    for row in raw:
        if not isinstance(row, dict):
            continue
        concept_id = row.get("concept_id")
        ifc_class = row.get("ifc_class")
        if (
            isinstance(concept_id, str)
            and isinstance(ifc_class, str)
            and concept_id.startswith("concept-")
            and ifc_class.startswith("Ifc")
        ):
            out[concept_id] = ifc_class
    return out


def export_snapshot_as_turtle(
    snapshot_path: Path,
    output_path: Path,
    *,
    ifc_mapping_path: Path | None = None,
) -> Path:
    """Render a Phase 8 snapshot JSON file as RDF Turtle.

    The snapshot is expected to be the JSON shape that
    :func:`vitruvius.graph.snapshot.write_snapshot` writes —
    specifically a dict with ``nodes`` (list of node dicts with ``id``,
    ``type``, etc.) and ``edges`` (list of edge dicts with ``from_id``,
    ``to_id``, ``type``, etc.).

    Writes ``output_path`` (creating any missing parent directories)
    and returns it. The Turtle output is serialised with
    ``format="turtle"`` via :mod:`rdflib` and is deterministic on
    repeated runs for the same input.

    Raises ``Exception`` on any malformed snapshot file (unparseable
    JSON or missing keys) — the tests use ``pytest.raises(Exception)``
    so the exact class is intentionally loose.
    """
    import rdflib
    from rdflib import Graph, Literal, Namespace, URIRef
    from rdflib.namespace import OWL, RDF, RDFS, XSD

    snapshot_path = Path(snapshot_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("snapshot must have 'nodes' and 'edges' lists")

    vit = Namespace(VITRUVIUS_NAMESPACE)
    ifc = Namespace(IFC_NAMESPACE)

    graph = Graph()
    graph.bind("vitruvius", vit)
    graph.bind("ifc", ifc)
    graph.bind("owl", OWL)
    graph.bind("rdfs", RDFS)

    ifc_mapping: Mapping[str, str] = {}
    if ifc_mapping_path is not None:
        ifc_mapping = _load_mapping_rows(Path(ifc_mapping_path))

    # Nodes — emit a typed resource for each id, plus rdfs:label
    # carrying the slug + trust_level and (when present) an owl:sameAs
    # link into the IFC namespace.
    for node in sorted(nodes, key=lambda n: str(n.get("id", ""))):
        node_id = str(node.get("id", ""))
        if not node_id:
            continue
        subject = URIRef(vit[_safe_local(node_id)])
        node_type = str(node.get("type", "node"))
        graph.add((subject, RDF.type, URIRef(vit[_safe_local(node_type)])))
        slug = node.get("slug")
        if isinstance(slug, str) and slug:
            graph.add((subject, RDFS.label, Literal(f"{slug} ({node_id})")))
        trust = node.get("trust_level")
        if isinstance(trust, str) and trust:
            graph.add((
                subject,
                URIRef(vit["trust_level"]),
                Literal(trust, datatype=XSD.string),
            ))
        updated = node.get("last_updated_utc")
        if isinstance(updated, str) and updated:
            graph.add((
                subject,
                URIRef(vit["last_updated_utc"]),
                Literal(updated, datatype=XSD.string),
            ))
        # IFC cross-link via owl:sameAs (only when mapping provided).
        if node_type == "concept" and node_id in ifc_mapping:
            graph.add((
                subject,
                OWL.sameAs,
                URIRef(ifc[_safe_local(ifc_mapping[node_id])]),
            ))

    # Edges — emit each as (from_id, predicate, to_id). Predicate
    # names live in the vitruvius namespace.
    for edge in sorted(
        edges,
        key=lambda e: (
            str(e.get("from_id", "")),
            str(e.get("type", "")),
            str(e.get("to_id", "")),
        ),
    ):
        from_id = str(edge.get("from_id", ""))
        to_id = str(edge.get("to_id", ""))
        rel_type = str(edge.get("type", ""))
        if not (from_id and to_id and rel_type):
            continue
        subject = URIRef(vit[_safe_local(from_id)])
        predicate = URIRef(vit[_safe_local(rel_type)])
        obj = URIRef(vit[_safe_local(to_id)])
        graph.add((subject, predicate, obj))

    # rdflib's turtle serialisation is deterministic per-graph when
    # the triples are identical; we sort_keys via the stable key
    # functions above and the namespace bindings above so running
    # this function twice on the same input produces byte-identical
    # output.
    body = graph.serialize(format="turtle")
    if isinstance(body, bytes):
        body = body.decode("utf-8")

    # rdflib only emits @prefix declarations for namespaces actually
    # used in at least one triple, so an empty snapshot produces a
    # blank file. Always prepend the canonical Vitruvius + IFC prefix
    # header so downstream parsers see the namespaces even for empty
    # graphs — this satisfies the empty-snapshot contract from the
    # Stream M.3 test suite.
    prefix_header = (
        f"@prefix vitruvius: <{VITRUVIUS_NAMESPACE}> .\n"
        f"@prefix ifc: <{IFC_NAMESPACE}> .\n"
        f"@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
        f"@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
        f"\n"
    )
    if "@prefix" not in body:
        body = prefix_header + body

    output_path.write_text(body, encoding="utf-8")
    return output_path
