from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .snapshot import read_snapshot


_DEFAULT_SNAPSHOT_RELPATH = (
    Path("005_Operational-Intelligence-Layer") / "graph" / "latest_graph_snapshot.json"
)
_DEFAULT_VIS_ROOT = Path("004_Derived-Content-Layer") / "graph-visualizations"


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


def _default_output_path(snapshot_file: Path, metadata: dict[str, Any]) -> Path:
    dataset_id = metadata.get("dataset_id")
    run_id = metadata.get("run_id")
    if isinstance(dataset_id, str) and dataset_id.strip():
        folder = Path.cwd() / _DEFAULT_VIS_ROOT / dataset_id
        stem = f"{run_id}_graph_snapshot" if isinstance(run_id, str) and run_id.strip() else snapshot_file.stem
        return folder / f"{stem}.html"
    return Path.cwd() / _DEFAULT_VIS_ROOT / "global" / f"{snapshot_file.stem}.html"


def _render_html(snapshot_dict: dict[str, Any], *, snapshot_display_path: str, out_path: Path) -> str:
    metadata = snapshot_dict.get("metadata") or {}
    edge_types = sorted({edge["type"] for edge in snapshot_dict["edges"]})
    law_ids = metadata.get("contributing_law_ids") or []
    elements = {
        "nodes": [
            {
                "data": {
                    "id": node["id"],
                    "label": node["id"],
                    "type": node["type"],
                    "trust_level": node["trust_level"],
                    "last_updated_utc": node["last_updated_utc"],
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
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Vitruvius Graph Visualization</title>
  <script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
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
      <div><strong>Snapshot:</strong> <code>{snapshot_display_path}</code></div>
      <div><strong>Dataset:</strong> {metadata.get("dataset_id", "global/latest")}</div>
      <div><strong>Run:</strong> {metadata.get("run_id", "n/a")}</div>
      <div><strong>Nodes:</strong> {snapshot_dict["node_count"]}</div>
      <div><strong>Edges:</strong> {snapshot_dict["edge_count"]}</div>
      <div><strong>Law units:</strong> {", ".join(law_ids) if law_ids else "n/a"}</div>
    </div>
    <h2>Search</h2>
    <input id="search" class="search" placeholder="Search node id..." />
    <div class="hint">Type part of a node id, then press Enter.</div>
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
    <div class="hint">Generated by <code>visualize-graph</code> into <code>{out_path}</code></div>
  </aside>
</div>
<script>
const snapshot = {json.dumps(snapshot_dict, ensure_ascii=False)};
const elements = {json.dumps(elements, ensure_ascii=False)};
const details = document.getElementById('details');
const search = document.getElementById('search');
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

search.addEventListener('keydown', event => {{
  if (event.key !== 'Enter') return;
  const query = search.value.trim().toLowerCase();
  const match = cy.nodes().toArray().find(node => node.id().toLowerCase().includes(query));
  if (match) {{
    focusNode(match);
  }}
}});
if (cy.nodes().length) {{
  focusNode(cy.nodes()[0]);
}}
</script>
</body>
</html>
"""


def run_visualize_graph(*, snapshot_path: str | None = None, out_path: str | None = None) -> int:
    resolved_snapshot_path, snapshot_display_path = _resolve_snapshot_path(snapshot_path)
    if not resolved_snapshot_path.exists():
        print(json.dumps({
            "error": "no snapshot found",
            "expected_path": snapshot_display_path,
            "hint": "run `build-graph` or `run-dataset-graph` first",
        }, indent=2))
        return 2

    snapshot = read_snapshot(resolved_snapshot_path)
    metadata = snapshot.metadata or {}
    rendered_out_path = (
        Path(out_path)
        if out_path is not None
        else _default_output_path(resolved_snapshot_path, metadata)
    )
    if not rendered_out_path.is_absolute():
        rendered_out_path = Path.cwd() / rendered_out_path

    snapshot_dict = json.loads(resolved_snapshot_path.read_text(encoding="utf-8"))
    html = _render_html(
        snapshot_dict,
        snapshot_display_path=snapshot_display_path,
        out_path=rendered_out_path,
    )
    rendered_out_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_out_path.write_text(html, encoding="utf-8")

    try:
        out_display = str(rendered_out_path.relative_to(Path.cwd()))
    except ValueError:
        out_display = str(rendered_out_path)

    summary = {
        "action": "visualize-graph",
        "snapshot_path": snapshot_display_path,
        "out_path": out_display,
        "dataset_id": metadata.get("dataset_id"),
        "run_id": metadata.get("run_id"),
        "node_count": snapshot.node_count,
        "edge_count": snapshot.edge_count,
    }
    print(json.dumps(summary, indent=2))
    return 0
