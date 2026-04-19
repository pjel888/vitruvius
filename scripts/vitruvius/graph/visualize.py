from __future__ import annotations

import html
import json
import os
from pathlib import Path
from typing import Any, Literal

from .snapshot import read_snapshot
from ..utils import assert_windows_safe_path


_DEFAULT_SNAPSHOT_RELPATH = (
    Path("005_Operational-Intelligence-Layer") / "graph" / "latest_graph_snapshot.json"
)
_DEFAULT_SNAPSHOT_RELPATH_V2 = (
    Path("005_Operational-Intelligence-Layer") / "graph" / "kg-v2"
)
_DEFAULT_VIS_ROOT = Path("004_Derived-Content-Layer") / "graph-visualizations"
_CYTOSCAPE_ASSET = Path("scripts") / "vitruvius" / "graph" / "assets" / "cytoscape.min.js"
_MODULE_CYTOSCAPE_ASSET = Path(__file__).resolve().parent / "assets" / "cytoscape.min.js"


def _resolve_snapshot_path(snapshot_path: str | None) -> tuple[Path, str]:
    if snapshot_path is None:
        path = Path.cwd() / _DEFAULT_SNAPSHOT_RELPATH
        return path, str(_DEFAULT_SNAPSHOT_RELPATH)
    path = Path(snapshot_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    try:
        display = str(path.relative_to(Path.cwd()))
    except ValueError:
        display = str(path)
    return path, display


def _resolve_snapshot_path_v2(snapshot_path: str | None) -> tuple[Path, str]:
    if snapshot_path is None:
        snap_dir = Path.cwd() / _DEFAULT_SNAPSHOT_RELPATH_V2
        if snap_dir.exists():
            candidates = sorted(snap_dir.glob("*_kg_v2_*.json"), reverse=True)
            if candidates:
                path = candidates[0]
                try:
                    display = str(path.relative_to(Path.cwd()))
                except ValueError:
                    display = str(path)
                return path, display
        path = snap_dir
        return path, str(_DEFAULT_SNAPSHOT_RELPATH_V2)
    path = Path(snapshot_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    try:
        display = str(path.relative_to(Path.cwd()))
    except ValueError:
        display = str(path)
    return path, display


def _default_output_path(snapshot_file: Path, metadata: dict[str, Any]) -> Path:
    dataset_id = metadata.get("dataset_id")
    run_id = metadata.get("run_id")
    if isinstance(dataset_id, str) and dataset_id.strip():
        folder = Path.cwd() / _DEFAULT_VIS_ROOT / dataset_id
        stem = f"{run_id}_graph_snapshot" if isinstance(run_id, str) and run_id.strip() else snapshot_file.stem
        return assert_windows_safe_path(
            folder / f"{stem}.html",
            what="graph visualization output path",
        )
    return assert_windows_safe_path(
        Path.cwd() / _DEFAULT_VIS_ROOT / "global" / f"{snapshot_file.stem}.html",
        what="graph visualization output path",
    )


def _asset_script_path(out_path: Path) -> str:
    asset_path = Path.cwd() / _CYTOSCAPE_ASSET
    relative = os.path.relpath(asset_path, out_path.parent)
    return relative.replace(os.sep, "/")


def _inline_asset_script() -> str | None:
    asset_path = _MODULE_CYTOSCAPE_ASSET
    if not asset_path.exists():
        return None
    return asset_path.read_text(encoding="utf-8").replace("</script", "<\\/script")


def _inline_json_script(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False).replace("</script", "<\\/script")


def _detect_snapshot_version(snapshot_dict: dict[str, Any]) -> Literal["v1", "v2", "unknown"]:
    if "nodes" in snapshot_dict and "edges" in snapshot_dict:
        return "v1"
    if "canonical_nodes" in snapshot_dict and "fast_edges" in snapshot_dict:
        return "v2"
    return "unknown"


# ---------------------------------------------------------------------------
# V1 rendering (legacy)
# ---------------------------------------------------------------------------

def _render_html_v1(snapshot_dict: dict[str, Any], *, snapshot_display_path: str, out_path: Path) -> str:
    metadata = snapshot_dict.get("metadata") or {}
    edge_types = sorted({edge["type"] for edge in snapshot_dict["edges"]})
    law_ids = metadata.get("contributing_law_ids") or []
    script_src = html.escape(_asset_script_path(out_path))
    inline_cytoscape = _inline_asset_script()
    script_tag = (
        "<script>/* bundled cytoscape.min.js */\n"
        + inline_cytoscape
        + "\n</script>"
        if inline_cytoscape
        else f'<script src="{script_src}"></script>'
    )
    snapshot_label = html.escape(snapshot_display_path)
    dataset_label = html.escape(str(metadata.get("dataset_id", "global/latest")))
    run_label = html.escape(str(metadata.get("run_id", "n/a")))
    out_label = html.escape(str(out_path))
    elements = {
        "nodes": [
            {
                "data": {
                    "id": node["id"],
                    "label": node.get("title") or node["id"],
                    "id_label": node["id"],
                    "type": node["type"],
                    "trust_level": node["trust_level"],
                    "last_updated_utc": node["last_updated_utc"],
                    "title": node.get("title"),
                }
            }
            for node in snapshot_dict["nodes"]
        ],
        "edges": [
            {
                "data": {
                    "id": edge["evidence_id"],
                    "source": edge["from_id"],
                    "target": edge["to_id"],
                    "label": edge["type"],
                    "type": edge["type"],
                    "status": edge["status"],
                    "evidence_source_id": edge.get("evidence_source_id"),
                    "evidence_source_section_id": edge.get("evidence_source_section_id"),
                }
            }
            for edge in snapshot_dict["edges"]
        ],
    }
    snapshot_json = _inline_json_script(snapshot_dict)
    elements_json = _inline_json_script(elements)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Vitruvius Graph Visualization</title>
  {script_tag}
  <style>
    body {{ font-family: Inter, system-ui, sans-serif; margin: 0; background: #0b1020; color: #e5e7eb; }}
    .layout {{ display: grid; grid-template-columns: 1fr 360px; min-height: 100vh; }}
    .canvas-wrap {{ position: relative; overflow: hidden; background:
      radial-gradient(circle at top, rgba(59,130,246,0.12), transparent 25%),
      radial-gradient(circle at bottom right, rgba(16,185,129,0.12), transparent 25%),
      linear-gradient(180deg, #0b1020 0%, #111827 100%); }}
    #cy {{ width: 100%; height: 100vh; display: block; }}
    .panel {{ border-left: 1px solid #1f2937; padding: 16px; background: #111827; overflow-y: auto; }}
    h1 {{ font-size: 18px; margin: 0 0 8px; }}
    h2 {{ font-size: 14px; margin: 18px 0 8px; color: #93c5fd; }}
    .meta, .details, .legend {{ font-size: 13px; line-height: 1.45; }}
    .pill {{ display: inline-block; padding: 2px 8px; border-radius: 999px; background: #1f2937; margin: 0 6px 6px 0; }}
    .search {{ width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 10px; border: 1px solid #334155; background: #0f172a; color: #e5e7eb; }}
    .hint {{ color: #9ca3af; font-size: 12px; margin-top: 8px; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
  </style>
</head>
<body>
<div class="layout">
  <div class="canvas-wrap">
    <div id="cy"></div>
  </div>
  <aside class="panel">
    <h1>Knowledge Graph Viewer</h1>
    <div class="meta">
      <div><strong>Snapshot:</strong> <code>{snapshot_label}</code></div>
      <div><strong>Dataset:</strong> {dataset_label}</div>
      <div><strong>Run:</strong> {run_label}</div>
      <div><strong>Nodes:</strong> {snapshot_dict["node_count"]}</div>
      <div><strong>Edges:</strong> {snapshot_dict["edge_count"]}</div>
      <div><strong>Law units:</strong> {", ".join(law_ids) if law_ids else "n/a"}</div>
    </div>
    <h2>Search</h2>
    <input id="search" class="search" placeholder="Search node title or id..." />
    <div class="hint">Type part of a node id, then press Enter.</div>
    <h2>Explorer Controls</h2>
    <div class="details">
      <div style="margin-bottom:8px;">
        <label><input type="checkbox" id="toggle-sources" checked /> Show source/law nodes</label><br/>
        <label><input type="checkbox" id="toggle-concepts" checked /> Show concept nodes</label>
      </div>
      <div style="margin-bottom:8px;">
        <label>Layout:
          <select id="layout-select">
            <option value="cose">cose</option>
            <option value="breadthfirst">breadthfirst</option>
            <option value="circle">circle</option>
            <option value="concentric">concentric</option>
          </select>
        </label>
      </div>
      <div>
        <label>Labels:
          <select id="label-mode">
            <option value="human">human title</option>
            <option value="compact">compact id</option>
            <option value="full">full id</option>
            <option value="none">none</option>
          </select>
        </label>
      </div>
    </div>
    <h2>Legend</h2>
    <div class="legend">
      <span class="pill">Blue = source / law / IRR</span>
      <span class="pill">Green = concept</span>
      <span class="pill">Amber edge = selected neighborhood</span>
    </div>
    <h2>Edge types</h2>
    <div class="legend">{"".join(f'<span class="pill">{edge_type}</span>' for edge_type in edge_types)}</div>
    <h2>Selection</h2>
    <div id="details" class="details">Nothing selected yet.</div>
    <div class="hint">Generated by <code>visualize-graph</code> into <code>{out_label}</code></div>
  </aside>
</div>
<script type="application/json" id="snapshot-data">{snapshot_json}</script>
<script type="application/json" id="elements-data">{elements_json}</script>
<script>
const snapshot = JSON.parse(document.getElementById('snapshot-data').textContent);
const elements = JSON.parse(document.getElementById('elements-data').textContent);
const details = document.getElementById('details');
const search = document.getElementById('search');
const toggleSources = document.getElementById('toggle-sources');
const toggleConcepts = document.getElementById('toggle-concepts');
const layoutSelect = document.getElementById('layout-select');
const labelMode = document.getElementById('label-mode');
const cy = cytoscape({{
  container: document.getElementById('cy'),
  elements: [...elements.nodes, ...elements.edges],
  style: [
    {{
      selector: 'node',
      style: {{
        'background-color': '#34d399',
        'label': 'data(label)',
        'font-size': '10px',
        'text-wrap': 'wrap',
        'text-max-width': '120px',
        'text-valign': 'bottom',
        'text-margin-y': 8,
        'color': '#dbeafe',
        'border-color': '#020617',
        'border-width': 1.5,
        'width': 22,
        'height': 22,
      }},
    }},
    {{
      selector: 'node[type = "source"]',
      style: {{
        'background-color': '#60a5fa',
        'width': 30,
        'height': 30,
      }},
    }},
    {{
      selector: 'edge',
      style: {{
        'curve-style': 'bezier',
        'line-color': '#475569',
        'target-arrow-color': '#475569',
        'target-arrow-shape': 'triangle',
        'arrow-scale': 0.8,
        'width': 1.5,
        'opacity': 0.55,
      }},
    }},
    {{
      selector: '.faded',
      style: {{
        'opacity': 0.12,
      }},
    }},
    {{
      selector: '.highlighted',
      style: {{
        'background-color': '#f59e0b',
        'line-color': '#f59e0b',
        'target-arrow-color': '#f59e0b',
        'opacity': 1,
        'width': 3,
      }},
    }},
    {{
      selector: '.hidden',
      style: {{
        'display': 'none',
      }},
    }},
  ],
  layout: {{
    name: 'cose',
    animate: false,
    fit: true,
    padding: 36,
    idealEdgeLength: 120,
    nodeRepulsion: 120000,
  }},
}});

function compactLabel(id) {{
  return id.length > 36 ? id.slice(0, 34) + '…' : id;
}}

function applyLabelMode() {{
  const mode = labelMode.value;
  cy.nodes().forEach(node => {{
    if (mode === 'none') node.style('label', '');
    else if (mode === 'full') node.style('label', node.id());
    else node.style('label', compactLabel(node.id()));
  }});
}}

function relayout() {{
  cy.layout({{
    name: layoutSelect.value,
    animate: true,
    fit: true,
    padding: 36,
    idealEdgeLength: 120,
    nodeRepulsion: 120000,
  }}).run();
}}

function applyVisibilityFilters() {{
  cy.nodes('[type = "source"]').toggleClass('hidden', !toggleSources.checked);
  cy.nodes('[type = "concept"]').toggleClass('hidden', !toggleConcepts.checked);
  cy.edges().forEach(edge => {{
    const hide = edge.source().hasClass('hidden') || edge.target().hasClass('hidden');
    edge.toggleClass('hidden', hide);
  }});
}}

function renderSelection(node) {{
  const related = node.connectedEdges();
  details.innerHTML = `
    <div><strong>ID:</strong> <code>${{node.id()}}</code></div>
    <div><strong>Type:</strong> ${{node.data('type')}}</div>
    <div><strong>Trust:</strong> ${{node.data('trust_level')}}</div>
    <div><strong>Last updated:</strong> ${{node.data('last_updated_utc')}}</div>
    <div style="margin-top:10px;"><strong>Connected edges:</strong> ${{related.length}}</div>
    <ul>${{related.slice(0, 12).map(edge => {{
      const other = edge.source().id() === node.id() ? edge.target().id() : edge.source().id();
      return `<li><code>${{edge.data('type')}}</code> → <code>${{other}}</code></li>`;
    }}).join('')}}</ul>
  `;
}}

function focusNode(node) {{
  cy.elements().addClass('faded');
  node.removeClass('faded').addClass('highlighted');
  node.connectedEdges().removeClass('faded').addClass('highlighted');
  node.neighborhood().removeClass('faded').addClass('highlighted');
  renderSelection(node);
  cy.animate({{
    fit: {{
      eles: node.closedNeighborhood(),
      padding: 80,
    }},
    duration: 300,
  }});
}}

cy.on('tap', 'node', (event) => {{
  focusNode(event.target);
}});

cy.on('tap', (event) => {{
  if (event.target !== cy) return;
  cy.elements().removeClass('faded highlighted');
  details.textContent = 'Nothing selected yet.';
}});

toggleSources.addEventListener('change', applyVisibilityFilters);
toggleConcepts.addEventListener('change', applyVisibilityFilters);
layoutSelect.addEventListener('change', relayout);
labelMode.addEventListener('change', applyLabelMode);
search.addEventListener('keydown', event => {{
  if (event.key !== 'Enter') return;
  const query = search.value.trim().toLowerCase();
  const match = cy.nodes().toArray().find(node => node.id().toLowerCase().includes(query) || (node.data('title') || '').toLowerCase().includes(query));
  if (match) {{
    focusNode(match);
  }}
}});
applyLabelMode();
applyVisibilityFilters();
if (cy.nodes().length) {{
  focusNode(cy.nodes()[0]);
}}
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# V2 rendering
# ---------------------------------------------------------------------------

_NODE_COLORS: dict[str, str] = {
    "taxonomy": "#a78bfa",   # purple
    "topic": "#818cf8",      # indigo
    "subtopic": "#60a5fa",   # blue
    "concept": "#34d399",    # emerald
    "term": "#2dd4bf",       # teal
    "definition": "#facc15", # yellow
    "rule": "#4ade80",       # green
    "procedure": "#fb923c",  # orange
    "exception": "#f87171",  # red
    "constraint": "#f472b6", # pink
    "example": "#c084fc",    # violet
}

_EDGE_COLORS: dict[str, str] = {
    "BELONGS_TO": "#4ade80",
    "DEPENDS_ON": "#60a5fa",
    "CONTRADICTS": "#f87171",
    "RELATED_TO": "#94a3b8",
    "MERGE": "#fb923c",
}


def _node_size(confidence: float) -> float:
    return 20 + confidence * 30


def _render_html_v2(
    snapshot: "KgV2Snapshot",
    *,
    snapshot_display_path: str,
    out_path: Path,
) -> str:
    from ..kg.query_engine import QueryEngine

    engine = QueryEngine(snapshot)

    metadata = snapshot.metadata or {}
    entity_counts = snapshot.entity_counts()

    # Build enriched node data
    node_data: dict[str, dict[str, Any]] = {}
    for node in snapshot.canonical_nodes:
        evidence = engine.get_evidence_for_node(node.id)
        neighborhood = engine.get_node_neighborhood(node.id)
        node_data[node.id] = {
            "id": node.id,
            "label": node.label,
            "type": node.type.value,
            "summary": node.summary or "",
            "taxonomy_path": node.taxonomy_path or [],
            "status": node.status.value if hasattr(node.status, "value") else str(node.status),
            "confidence": node.confidence,
            "version": node.version,
            "aliases": node.aliases or [],
            "evidence": [e.model_dump(mode="json") for e in evidence],
            "neighbors": [
                {
                    "id": n.id,
                    "label": n.label,
                    "type": n.type.value,
                    "assertion_id": a.id,
                    "edge_type": a.edge_type.value if hasattr(a, "edge_type") else "BELONGS_TO",
                    "reasoning_summary": a.reasoning_summary,
                }
                for n, a in neighborhood
            ],
        }

    # Build enriched edge data
    edge_data: dict[str, dict[str, Any]] = {}
    for edge in snapshot.fast_edges:
        eid = edge.get("id") or f"edge-{edge['from_node_id']}-{edge['to_node_id']}"
        assertion_id = edge.get("assertion_id")
        assertion = engine.get_assertion_by_id(assertion_id) if assertion_id else None
        evidence = engine.get_evidence_for_assertion(assertion_id) if assertion_id else []
        edge_data[eid] = {
            "id": eid,
            "source": edge["from_node_id"],
            "target": edge["to_node_id"],
            "edge_type": edge.get("edge_type", "RELATED_TO"),
            "confidence": edge.get("confidence", 0.5),
            "assertion_id": assertion_id,
            "reasoning_summary": getattr(assertion, "reasoning_summary", "") if assertion else "",
            "inference_type": (
                getattr(assertion, "inference_type", "").value
                if assertion and hasattr(getattr(assertion, "inference_type", None), "value")
                else str(getattr(assertion, "inference_type", ""))
            ) if assertion else "",
            "evidence": [e.model_dump(mode="json") for e in evidence],
        }

    # Also add placement assertions as dashed edges
    for placement in snapshot.placement_assertions:
        eid = f"edge-{placement.id}"
        evidence = engine.get_evidence_for_assertion(placement.id)
        edge_data[eid] = {
            "id": eid,
            "source": placement.node_id,
            "target": placement.parent_node_id,
            "edge_type": "BELONGS_TO",
            "confidence": placement.confidence,
            "assertion_id": placement.id,
            "reasoning_summary": placement.reasoning_summary,
            "inference_type": "",
            "evidence": [e.model_dump(mode="json") for e in evidence],
            "dashed": True,
        }

    # Also add merge assertions as dashed edges
    for merge in snapshot.merge_assertions:
        eid = f"edge-{merge.id}"
        evidence = engine.get_evidence_for_assertion(merge.id)
        edge_data[eid] = {
            "id": eid,
            "source": merge.from_node_id,
            "target": merge.to_node_id,
            "edge_type": "MERGE",
            "confidence": merge.confidence,
            "assertion_id": merge.id,
            "reasoning_summary": merge.reasoning_summary,
            "inference_type": "",
            "evidence": [e.model_dump(mode="json") for e in evidence],
            "dashed": True,
        }

    elements = {
        "nodes": [
            {
                "data": {
                    "id": node.id,
                    "label": node.label,
                    "type": node.type.value,
                }
            }
            for node in snapshot.canonical_nodes
        ],
        "edges": [
            {
                "data": {
                    "id": eid,
                    "source": ed["source"],
                    "target": ed["target"],
                    "label": ed["edge_type"],
                    "type": ed["edge_type"],
                    "assertion_id": ed.get("assertion_id"),
                }
            }
            for eid, ed in edge_data.items()
        ],
    }

    script_src = html.escape(_asset_script_path(out_path))
    inline_cytoscape = _inline_asset_script()
    script_tag = (
        "<script>/* bundled cytoscape.min.js */\n"
        + inline_cytoscape
        + "\n</script>"
        if inline_cytoscape
        else f'<script src="{script_src}"></script>'
    )
    snapshot_label = html.escape(snapshot_display_path)
    out_label = html.escape(str(out_path))
    node_data_json = _inline_json_script(node_data)
    edge_data_json = _inline_json_script(edge_data)
    elements_json = _inline_json_script(elements)

    edge_types = sorted({ed["edge_type"] for ed in edge_data.values()})

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Vitruvius KG v2 Viewer</title>
  {script_tag}
  <style>
    body {{ font-family: Inter, system-ui, sans-serif; margin: 0; background: #0b1020; color: #e5e7eb; }}
    .layout {{ display: grid; grid-template-columns: 1fr 420px; min-height: 100vh; }}
    .canvas-wrap {{ position: relative; overflow: hidden; background:
      radial-gradient(circle at top, rgba(59,130,246,0.12), transparent 25%),
      radial-gradient(circle at bottom right, rgba(16,185,129,0.12), transparent 25%),
      linear-gradient(180deg, #0b1020 0%, #111827 100%); }}
    #cy {{ width: 100%; height: 100vh; display: block; }}
    .panel {{ border-left: 1px solid #1f2937; padding: 16px; background: #111827; overflow-y: auto; }}
    h1 {{ font-size: 18px; margin: 0 0 8px; }}
    h2 {{ font-size: 14px; margin: 18px 0 8px; color: #93c5fd; }}
    h3 {{ font-size: 12px; margin: 12px 0 6px; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.05em; }}
    .meta, .details, .legend {{ font-size: 13px; line-height: 1.45; }}
    .pill {{ display: inline-block; padding: 2px 8px; border-radius: 999px; background: #1f2937; margin: 0 6px 6px 0; font-size: 11px; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; background: #1e3a8a; color: #bfdbfe; font-size: 11px; font-weight: 600; }}
    .badge-inference-direct {{ background: #064e3b; color: #a7f3d0; }}
    .badge-inference-multihop {{ background: #7c2d12; color: #fed7aa; }}
    .badge-inference-human {{ background: #581c87; color: #e9d5ff; }}
    .search {{ width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 10px; border: 1px solid #334155; background: #0f172a; color: #e5e7eb; }}
    .hint {{ color: #9ca3af; font-size: 12px; margin-top: 8px; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; }}
    .evidence-item {{ background: #0f172a; border: 1px solid #1f2937; border-radius: 8px; padding: 8px; margin-bottom: 8px; }}
    .evidence-quote {{ color: #e2e8f0; font-style: italic; margin: 4px 0; }}
    .evidence-meta {{ color: #94a3b8; font-size: 11px; }}
    .neighbor-item {{ cursor: pointer; padding: 4px 0; border-bottom: 1px solid #1f2937; }}
    .neighbor-item:hover {{ color: #93c5fd; }}
  </style>
</head>
<body>
<div class="layout">
  <div class="canvas-wrap">
    <div id="cy"></div>
  </div>
  <aside class="panel">
    <h1>KG v2 Viewer</h1>
    <div class="meta">
      <div><strong>Snapshot:</strong> <code>{snapshot_label}</code></div>
      <div><strong>Nodes:</strong> {entity_counts.get('canonical_nodes', 0)}</div>
      <div><strong>Edges:</strong> {entity_counts.get('fast_edges', 0)}</div>
      <div><strong>Assertions:</strong> {entity_counts.get('relationship_assertions', 0)} rel + {entity_counts.get('placement_assertions', 0)} place + {entity_counts.get('merge_assertions', 0)} merge</div>
      <div><strong>Evidence spans:</strong> {entity_counts.get('evidence_spans', 0)}</div>
    </div>
    <h2>Search</h2>
    <input id="search" class="search" placeholder="Search node label..." />
    <div class="hint">Type and press Enter to focus the first match.</div>
    <h2>Legend</h2>
    <div class="legend">
      <span class="pill" style="background:#a78bfa">taxonomy</span>
      <span class="pill" style="background:#60a5fa">subtopic</span>
      <span class="pill" style="background:#34d399">concept</span>
      <span class="pill" style="background:#4ade80">rule</span>
      <span class="pill" style="background:#facc15;color:#000">definition</span>
      <span class="pill" style="background:#fb923c">procedure</span>
      <span class="pill" style="background:#f87171">exception</span>
    </div>
    <h2>Edge types</h2>
    <div class="legend">{"".join(f'<span class="pill">{edge_type}</span>' for edge_type in edge_types)}</div>
    <h2>Selection</h2>
    <div id="details" class="details">Nothing selected yet.</div>
    <div class="hint">Generated by <code>visualize-graph</code> into <code>{out_label}</code></div>
  </aside>
</div>
<script type="application/json" id="node-data">{node_data_json}</script>
<script type="application/json" id="edge-data">{edge_data_json}</script>
<script type="application/json" id="elements-data">{elements_json}</script>
<script>
const nodeData = JSON.parse(document.getElementById('node-data').textContent);
const edgeData = JSON.parse(document.getElementById('edge-data').textContent);
const elements = JSON.parse(document.getElementById('elements-data').textContent);
const details = document.getElementById('details');
const search = document.getElementById('search');

const nodeColors = {{
  taxonomy: '#a78bfa',
  topic: '#818cf8',
  subtopic: '#60a5fa',
  concept: '#34d399',
  term: '#2dd4bf',
  definition: '#facc15',
  rule: '#4ade80',
  procedure: '#fb923c',
  exception: '#f87171',
  constraint: '#f472b6',
  example: '#c084fc',
}};

const edgeColors = {{
  BELONGS_TO: '#4ade80',
  DEPENDS_ON: '#60a5fa',
  CONTRADICTS: '#f87171',
  RELATED_TO: '#94a3b8',
  MERGE: '#fb923c',
}};

function nodeSize(confidence) {{
  return 20 + (confidence || 0.5) * 30;
}}

const cy = cytoscape({{
  container: document.getElementById('cy'),
  elements: [...elements.nodes, ...elements.edges],
  style: [
    {{
      selector: 'node',
      style: {{
        'background-color': ele => nodeColors[ele.data('type')] || '#94a3b8',
        'label': 'data(label)',
        'font-size': '10px',
        'text-wrap': 'wrap',
        'text-max-width': '120px',
        'text-valign': 'bottom',
        'text-margin-y': 8,
        'color': '#dbeafe',
        'border-color': '#020617',
        'border-width': 1.5,
        'width': ele => nodeSize(nodeData[ele.id()]?.confidence),
        'height': ele => nodeSize(nodeData[ele.id()]?.confidence),
      }},
    }},
    {{
      selector: 'edge',
      style: {{
        'curve-style': 'bezier',
        'line-color': ele => edgeColors[ele.data('type')] || '#475569',
        'target-arrow-color': ele => edgeColors[ele.data('type')] || '#475569',
        'target-arrow-shape': 'triangle',
        'arrow-scale': 0.8,
        'width': ele => 1 + (edgeData[ele.id()]?.confidence || 0.5) * 3,
        'opacity': 0.65,
        'line-style': ele => edgeData[ele.id()]?.dashed ? 'dashed' : 'solid',
      }},
    }},
    {{
      selector: '.faded',
      style: {{ 'opacity': 0.1 }},
    }},
    {{
      selector: '.highlighted',
      style: {{
        'background-color': '#f59e0b',
        'line-color': '#f59e0b',
        'target-arrow-color': '#f59e0b',
        'opacity': 1,
        'width': 4,
      }},
    }},
  ],
  layout: {{
    name: 'cose',
    animate: false,
    fit: true,
    padding: 36,
    idealEdgeLength: 120,
    nodeRepulsion: 80000,
  }},
}});

function escapeHtml(str) {{
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}}

function renderNodeDetails(nodeId) {{
  const info = nodeData[nodeId];
  if (!info) return;
  let html = `<div><strong>${{escapeHtml(info.label)}}</strong> <code>${{nodeId}}</code></div>`;
  html += `<div><span class="pill">${{info.type}}</span> <span class="pill">${{info.status}}</span> <span class="pill">conf=${{info.confidence?.toFixed(2)}}</span></div>`;
  if (info.summary) html += `<div style="margin-top:8px;">${{escapeHtml(info.summary)}}</div>`;
  if (info.taxonomy_path?.length) html += `<div style="margin-top:4px;color:#94a3b8;">Path: ${{info.taxonomy_path.join(' / ')}}</div>`;
  if (info.aliases?.length) html += `<div style="margin-top:4px;color:#94a3b8;">Aliases: ${{info.aliases.join(', ')}}</div>`;

  if (info.evidence?.length) {{
    html += `<h3>Evidence (${{info.evidence.length}})</h3>`;
    for (const span of info.evidence.slice(0, 5)) {{
      html += `<div class="evidence-item">`;
      html += `<div class="evidence-quote">"${{escapeHtml(span.quote?.slice(0, 200) || '')}}"</div>`;
      html += `<div class="evidence-meta">${{span.selector?.kind || ''}} | doc: ${{span.document_id || ''}}</div>`;
      if (span.deep_link) html += `<div class="evidence-meta"><a href="${{span.deep_link}}" target="_blank" style="color:#93c5fd;">${{span.deep_link}}</a></div>`;
      html += `</div>`;
    }}
    if (info.evidence.length > 5) html += `<div class="hint">+ ${{info.evidence.length - 5}} more evidence spans</div>`;
  }}

  if (info.neighbors?.length) {{
    html += `<h3>Related nodes (${{info.neighbors.length}})</h3>`;
    for (const n of info.neighbors.slice(0, 8)) {{
      html += `<div class="neighbor-item" data-node-id="${{n.id}}">
        <code>${{n.edge_type}}</code> → <strong>${{escapeHtml(n.label)}}</strong> <span style="color:#94a3b8;">(${{n.type}})</span>
        <div style="color:#9ca3af;font-size:11px;">${{escapeHtml(n.reasoning_summary?.slice(0, 80) || '')}}</div>
      </div>`;
    }}
  }}

  details.innerHTML = html;
  details.querySelectorAll('.neighbor-item').forEach(el => {{
    el.addEventListener('click', () => {{
      const targetId = el.getAttribute('data-node-id');
      const target = cy.getElementById(targetId);
      if (target.length) focusNode(target);
    }});
  }});
}}

function renderEdgeDetails(edgeId) {{
  const info = edgeData[edgeId];
  if (!info) return;
  let html = `<div><strong>${{info.edge_type}}</strong> <code>${{edgeId}}</code></div>`;
  html += `<div><code>${{info.source}}</code> → <code>${{info.target}}</code></div>`;
  html += `<div style="margin-top:4px;"><span class="pill">conf=${{info.confidence?.toFixed(2)}}</span></div>`;

  if (info.inference_type) {{
    const badgeClass = info.inference_type === 'direct_citation' ? 'badge-inference-direct'
      : info.inference_type === 'multi_hop_inference' ? 'badge-inference-multihop'
      : 'badge-inference-human';
    const label = info.inference_type === 'direct_citation' ? 'Direct citation'
      : info.inference_type === 'multi_hop_inference' ? 'Multi-hop inference'
      : info.inference_type === 'human_authored' ? 'Human authored'
      : info.inference_type;
    html += `<div style="margin-top:8px;"><span class="badge ${{badgeClass}}">${{label}}</span></div>`;
  }}

  if (info.reasoning_summary) {{
    html += `<div style="margin-top:12px;"><strong>Reasoning:</strong></div>`;
    html += `<div style="color:#cbd5e1;">${{escapeHtml(info.reasoning_summary)}}</div>`;
  }}

  if (info.evidence?.length) {{
    html += `<h3>Evidence (${{info.evidence.length}})</h3>`;
    for (const span of info.evidence.slice(0, 5)) {{
      html += `<div class="evidence-item">`;
      html += `<div class="evidence-quote">"${{escapeHtml(span.quote?.slice(0, 200) || '')}}"</div>`;
      html += `<div class="evidence-meta">${{span.selector?.kind || ''}} | doc: ${{span.document_id || ''}}</div>`;
      if (span.deep_link) html += `<div class="evidence-meta"><a href="${{span.deep_link}}" target="_blank" style="color:#93c5fd;">${{span.deep_link}}</a></div>`;
      html += `</div>`;
    }}
    if (info.evidence.length > 5) html += `<div class="hint">+ ${{info.evidence.length - 5}} more evidence spans</div>`;
  }}

  details.innerHTML = html;
}}

function focusNode(node) {{
  cy.elements().addClass('faded');
  node.removeClass('faded').addClass('highlighted');
  node.connectedEdges().removeClass('faded').addClass('highlighted');
  node.neighborhood().removeClass('faded').addClass('highlighted');
  renderNodeDetails(node.id());
  cy.animate({{
    fit: {{ eles: node.closedNeighborhood(), padding: 80 }},
    duration: 300,
  }});
}}

function focusEdge(edge) {{
  cy.elements().addClass('faded');
  edge.removeClass('faded').addClass('highlighted');
  edge.source().removeClass('faded').addClass('highlighted');
  edge.target().removeClass('faded').addClass('highlighted');
  renderEdgeDetails(edge.id());
}}

cy.on('tap', 'node', (event) => {{
  focusNode(event.target);
}});

cy.on('tap', 'edge', (event) => {{
  focusEdge(event.target);
}});

cy.on('tap', (event) => {{
  if (event.target !== cy) return;
  cy.elements().removeClass('faded highlighted');
  details.textContent = 'Nothing selected yet.';
}});

search.addEventListener('keydown', event => {{
  if (event.key !== 'Enter') return;
  const query = search.value.trim().toLowerCase();
  const match = cy.nodes().toArray().find(node =>
    (nodeData[node.id()]?.label || '').toLowerCase().includes(query) ||
    node.id().toLowerCase().includes(query)
  );
  if (match) focusNode(match);
}});

if (cy.nodes().length) {{
  focusNode(cy.nodes()[0]);
}}
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def generate_html(
    snapshot_path: str | None = None,
    out_path: str | None = None,
    *,
    version: Literal["auto", "v1", "v2"] = "auto",
) -> tuple[str, Path]:
    """Generate an HTML visualization from a snapshot.

    Returns (html_content, output_path).
    """
    if version == "v2":
        resolved_snapshot_path, snapshot_display_path = _resolve_snapshot_path_v2(snapshot_path)
    else:
        resolved_snapshot_path, snapshot_display_path = _resolve_snapshot_path(snapshot_path)

    if not resolved_snapshot_path.exists():
        raise FileNotFoundError(f"Snapshot not found: {snapshot_display_path}")

    snapshot_dict = json.loads(resolved_snapshot_path.read_text(encoding="utf-8"))
    detected = _detect_snapshot_version(snapshot_dict)

    if version == "auto":
        version = detected  # type: ignore[assignment]
    elif version == "v1" and detected != "v1":
        raise ValueError(f"Requested v1 but snapshot appears to be {detected}")
    elif version == "v2" and detected != "v2":
        raise ValueError(f"Requested v2 but snapshot appears to be {detected}")

    metadata = snapshot_dict.get("metadata") or {}
    rendered_out_path = (
        Path(out_path)
        if out_path is not None
        else _default_output_path(resolved_snapshot_path, metadata)
    )
    if not rendered_out_path.is_absolute():
        rendered_out_path = Path.cwd() / rendered_out_path
    rendered_out_path = assert_windows_safe_path(
        rendered_out_path,
        what="graph visualization output path",
    )

    if version == "v2":
        from ..kg.json_evidence_store import KgV2Snapshot
        snapshot = KgV2Snapshot.read(resolved_snapshot_path)
        html = _render_html_v2(
            snapshot,
            snapshot_display_path=snapshot_display_path,
            out_path=rendered_out_path,
        )
    else:
        html = _render_html_v1(
            snapshot_dict,
            snapshot_display_path=snapshot_display_path,
            out_path=rendered_out_path,
        )

    return html, rendered_out_path


def run_visualize_graph(
    *,
    snapshot_path: str | None = None,
    out_path: str | None = None,
    version: Literal["auto", "v1", "v2"] = "auto",
) -> int:
    """CLI entry point for visualize-graph."""
    try:
        html, rendered_out_path = generate_html(
            snapshot_path=snapshot_path,
            out_path=out_path,
            version=version,
        )
    except FileNotFoundError as exc:
        print(json.dumps({
            "error": "no snapshot found",
            "expected_path": str(exc),
            "hint": "run `build-graph` or `run-dataset-graph` first",
        }, indent=2))
        return 2
    except ValueError as exc:
        print(json.dumps({
            "error": "version mismatch",
            "message": str(exc),
        }, indent=2))
        return 2

    rendered_out_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_out_path.write_text(html, encoding="utf-8")

    try:
        out_display = str(rendered_out_path.relative_to(Path.cwd()))
    except ValueError:
        out_display = str(rendered_out_path)

    summary = {
        "action": "visualize-graph",
        "snapshot_path": snapshot_path or str(_DEFAULT_SNAPSHOT_RELPATH),
        "out_path": out_display,
        "version": version,
    }
    print(json.dumps(summary, indent=2))
    return 0
