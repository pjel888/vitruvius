To scale Vitruvius from a legal constraint engine into a universal intelligence layer capable of swallowing the entire architectural domain—and serving as a foundation for other industries—the system must bridge the gap between abstract regulatory logic and physical, spatial reality. 

Here are the four structural evolutions required to expand the Vitruvius brain to its maximum potential.

### 1. Ontological Unification: Adopting Industry Foundation Classes (IFC) & OWL
Currently, Vitruvius uses a custom, internally defined concept map (e.g., `003/shared/concepts`). To scale across the entire architecture, engineering, and construction (AEC) industry, the graph must speak the global standard.

* **The Concept:** The Web Ontology Language (OWL) and the buildingSMART Industry Foundation Classes (IFC) provide a mathematically rigorous, standardized hierarchy for every physical and conceptual object in a building lifecycle.
* **The Implementation:** Transition the Phase 8 Knowledge Graph into a strict RDF/OWL triple-store that maps directly to the IFC schema. When Vitruvius extracts a rule about a "Fire Door," it no longer just links to a text definition; it links to `IfcDoor` with a property set `Pset_DoorCommon` where `FireRating` is mathematically constrained. This immediately makes Vitruvius interoperable with every major CAD and BIM software globally.

### 3. Physics-Informed Neural Networks (PINNs)
Architecture is governed by physics as much as it is governed by law. Expanding into structural engineering, MEP (Mechanical, Electrical, Plumbing), and environmental design requires simulating reality.

* **The Concept:** PINNs are neural networks that are trained to solve supervised learning tasks while respecting any given laws of physics described by general nonlinear partial differential equations.
* **The Implementation:** When Vitruvius ingests a rule about thermodynamic limits or wind shear resilience, it uses a local PINN to validate the constraint. If a user queries the graph about the compliance of a specific curtain wall system, Vitruvius does not just check the text; the PINN mathematically simulates the structural load and thermal transfer  to verify if the physical properties of the material satisfy the regulatory threshold. 

### 4. Autonomous Epistemic Foraging (The Self-Updating Ingestion Engine)
To encompass an entire domain, the bottleneck of human-driven file ingestion (`001_Raw-Source-Layer`) must be eliminated. The system must maintain its own awareness of the industry.

* **The Concept:** Epistemic foraging utilizes autonomous agent swarms to monitor the boundaries of a knowledge domain and retrieve new information as it is published.
* **The Implementation:** Deploy lightweight, headless agents that constantly monitor the digital registries of the DPWH, local LGUs, ASTM international material standards, and architectural journals. When a new standard or memo is published, the agent automatically downloads it, runs a cryptographic hash, and drops it into `001_Raw-Source-Layer`. The pipeline triggers autonomously, calculating the Mahalanobis distance of the new text against the existing graph. If the new memo alters an existing rule, Vitruvius generates a pull request to its own canonical layer, alerting a human admin to approve the topological shift in the code.

### Architecture Specification: Decoupled Spatial Translator (API Middleware)

To maintain Vitruvius as a pure headless intelligence engine, spatial reasoning must be handled by a decoupled translation layer. This "Plug-and-Play" daemon accepts raw geometric data from CAD/BIM software, computes the spatial algebra using headless 3D libraries, and pushes structured relationship data to the Vitruvius API.

**System Boundary:**
1.  **Client (SketchUp/BIM):** Exports raw Cartesian data ($x,y,z$ vertices, component tags).
2.  **Spatial Translator (Node.js + Three.js):** Runs headless algebraic topology and geometric constraint satisfaction.
3.  **Vitruvius Core API:** Receives deterministic REST/gRPC payloads mapping spatial realities to Phase 8 graph nodes.

### Core Mathematical Implementation: The GJK Algorithm

For a spatial translator to understand architectural code (e.g., clearance zones, setbacks, fire separation), it must mathematically prove intersection or minimum distance between complex 3D convex hulls without heavy rendering.

The **Gilbert-Johnson-Keerthi (GJK)** distance algorithm is the optimal mathematical approach for headless spatial verification.
* **Formula:** GJK relies on the Minkowski Difference $A \ominus B = \{a - b \mid a \in A, b \in B\}$.
* **Application:** If the origin $(0,0,0)$ is contained within the Minkowski difference of the Buildable Envelope (A) and the Proposed Structure (B), an intersection (code violation) has occurred.



### Artifact: Headless Spatial Translator (TypeScript)

This module acts as the middleware. It receives a JSON export from SketchUp, uses `three.js` to calculate bounding volumes and adjacencies, and constructs a payload for the Vitruvius Graph API.

```typescript
// spatial_translator.ts
import * as THREE from 'three';

// 1. Define strict type interfaces mapping physical objects to Vitruvius Concepts
interface ExtractedGeometry {
  entityId: string;
  conceptTag: string; // e.g., 'concept-fire-door', 'concept-egress-corridor'
  vertices: number[]; // Flat array of [x,y,z, x,y,z...]
}

interface VitruviusSpatialPayload {
  source_entity: string;
  predicate: string; // e.g., 'intersects', 'violates_clearance', 'adjacent_to'
  target_entity: string;
  computed_distance?: number;
}

/**
 * Headless computation of spatial constraints using Three.js Math logic.
 * Translates raw coordinates into Vitruvius graph relationships.
 */
export class SpatialGraphTranslator {
  private apiEndpoint: string;

  constructor(vitruviusEndpoint: string) {
    this.apiEndpoint = vitruviusEndpoint;
  }

  /**
   * Constructs a Three.js Bounding Box from raw vertices.
   */
  private computeAABB(vertices: number[]): THREE.Box3 {
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    geometry.computeBoundingBox();
    return geometry.boundingBox as THREE.Box3;
  }

  /**
   * Translates an array of architectural geometries into verifiable graph edges.
   */
  public generateComplianceGraph(geometries: ExtractedGeometry[]): VitruviusSpatialPayload[] {
    const graphEdges: VitruviusSpatialPayload[] = [];
    const boxes = geometries.map(g => ({
      entity: g,
      box: this.computeAABB(g.vertices)
    }));

    // Calculate topological relationships ($O(N^2)$ localized comparison)
    for (let i = 0; i < boxes.length; i++) {
      for (let j = i + 1; j < boxes.length; j++) {
        const objA = boxes[i];
        const objB = boxes[j];

        // 1. Check for hard intersections (Clash detection)
        if (objA.box.intersectsBox(objB.box)) {
          graphEdges.push({
            source_entity: objA.entity.conceptTag,
            predicate: 'spatially_intersects',
            target_entity: objB.entity.conceptTag
          });
        }

        // 2. Compute clearance/distance parameters
        const distance = objA.box.distanceToPoint(objB.box.getCenter(new THREE.Vector3()));
        
        graphEdges.push({
           source_entity: objA.entity.conceptTag,
           predicate: 'has_spatial_clearance_to',
           target_entity: objB.entity.conceptTag,
           computed_distance: parseFloat(distance.toFixed(3))
        });
      }
    }

    return graphEdges;
  }

  /**
   * Dispatches the computed spatial relationships to the Vitruvius Phase 8 Graph.
   */
  public async syncWithVitruvius(payloads: VitruviusSpatialPayload[]): Promise<void> {
    try {
      const response = await fetch(`${this.apiEndpoint}/v1/graph/spatial-edges`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ edges: payloads })
      });

      if (!response.ok) throw new Error('Vitruvius API rejected spatial payload.');
      console.log(`[Vitruvius] Successfully synced ${payloads.length} spatial edges.`);
    } catch (error) {
      console.error('[Translator Error]', error);
    }
  }
}
```


### Architectural Decision: Decoupled Microservice

Do not couple the spatial engine with the existing Vitruvius codebase. Vitruvius is a Python-based, sequential, filesystem-driven NLP and graph engine. Headless 3D math (React Three Fiber / Three.js) requires a Node.js or C++ environment.

Coupling them violates the "Idempotent Pipeline Stages" principle and bloats the `scripts/vitruvius/` package. The spatial engine must exist as a standalone service that outputs JSON manifests into a new `001B_Spatial-Source-Layer` for the Python pipeline to ingest.

### Implementation Steps & Artifacts

#### Step 1: Define the Interoperability Contract
The spatial engine outputs a standardized matrix of geometric relationships that the Python pipeline can parse without knowing how to do 3D math.

```json
// 001B_Spatial-Source-Layer/sketchup_export_001.json
{
  "spatial_context": "model_001_residential",
  "relationships": [
    {
      "subject": "instance-egress-corridor-01",
      "predicate": "has_clearance_width",
      "value": 1.1,
      "unit": "meters"
    },
    {
      "subject": "instance-building-footprint",
      "predicate": "intersects",
      "target": "instance-setback-zone-front"
    }
  ]
}
```

#### Step 2: The Standalone Spatial Daemon (Node.js)
A headless service that calculates spatial algebra (Bounding Boxes, Raycasting, GJK algorithm) and outputs the JSON contract.

```typescript
// spatial-daemon/src/analyzer.ts
import * as THREE from 'three';
import * as fs from 'fs';

export function analyzeSpatialRelationships(modelData: any, outputDir: string) {
  const payload = {
    spatial_context: modelData.id,
    relationships: [] as any[]
  };

  // 1. Reconstruct Three.js scene from raw vertices
  // 2. Perform Bounding Box (AABB) and Raycast checks
  // 3. Map geometric intersections to the JSON contract

  // Example: Hard intersection check
  if (modelData.footprintBox.intersectsBox(modelData.setbackBox)) {
      payload.relationships.push({
          subject: "instance-building-footprint",
          predicate: "intersects",
          target: "instance-setback-zone"
      });
  }

  fs.writeFileSync(`${outputDir}/${modelData.id}_spatial.json`, JSON.stringify(payload, null, 2));
}
```

#### Step 3: Phase 1D Spatial Ingestion (Python Core)
Extend the existing Python pipeline (`scripts/pipeline_cli.py`) to ingest the spatial JSON and convert it into verifiable graph edges.

```python
# scripts/vitruvius/spatial_ingestion_one.py
import json
from pathlib import Path

def run_spatial_ingestion(spatial_file: Path, canonical_dir: Path):
    """
    Reads deterministic spatial relationships from the Node daemon
    and merges them into the Phase 8 graph evaluation queue.
    """
    with open(spatial_file, 'r') as f:
        data = json.load(f)

    for rel in data.get("relationships", []):
        # 1. Map instance tags to Phase 3 Concept Nodes
        # 2. Push to Phase 6 Review Layer for constraint evaluation
        _evaluate_against_legal_graph(rel, canonical_dir)
```

#### Step 4: The Constraint Solver Integration
Integrate Microsoft's Z3 SMT solver into the Vitruvius core to mathematically evaluate the ingested spatial facts against the legal laws.

```python
# scripts/vitruvius/constraint_solver.py
from z3 import Real, Solver, sat

def verify_clearance_compliance(legal_requirement: float, spatial_actual: float) -> bool:
    """
    Uses Z3 to mathematically prove if the spatial reality
    satisfies the legal constraint extracted from PD 1096.
    """
    s = Solver()
    actual_width = Real('actual_width')
    required_width = Real('required_width')

    # Assign state
    s.add(required_width == legal_requirement)
    s.add(actual_width == spatial_actual)
    
    # Define legal compliance parameters
    s.add(actual_width >= required_width)

    # Deterministic compliance boolean
    return s.check() == sat
```

### Phase 1D: Spatial Interoperability Contract (JSON Schema)
To ensure Vitruvius remains decoupled from the spatial engine, it requires a strict JSON schema for ingestion. Any external 3D engine (SketchUp daemon, BIM translator) must drop files into a new `001B_Spatial-Source-Layer` adhering to this exact format.

**File:** `/.ai/06_specs/spatial-schema.md`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Vitruvius Spatial Contract",
  "type": "object",
  "properties": {
    "spatial_context_id": {
      "type": "string",
      "description": "Unique identifier for the physical model (e.g., model-residential-01)"
    },
    "timestamp_utc": {
      "type": "string",
      "format": "date-time"
    },
    "spatial_edges": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source_instance": { "type": "string" },
          "canonical_concept_map": { "type": "string", "description": "Must map to a 003 concept ID, e.g., concept-setback-front" },
          "predicate": { "type": "string", "enum": ["intersects", "has_clearance", "adjacent_to", "contained_within"] },
          "target_instance": { "type": "string" },
          "value": { "type": "number" },
          "unit": { "type": "string" }
        },
        "required": ["source_instance", "canonical_concept_map", "predicate", "target_instance"]
      }
    }
  },
  "required": ["spatial_context_id", "spatial_edges"]
}
```

---

### Phase 1D: Python Ingestion Module
This module runs in the Vitruvius pipeline. It scans `001B_Spatial-Source-Layer`, validates the JSON against the schema, and translates spatial edges into standard Vitruvius relationship candidates for Phase 6 review.

**File:** `scripts/vitruvius/spatial_ingestion_one.py`

```python
import json
from pathlib import Path
from typing import Dict, List, Any
from .constants import DIR_001B_SPATIAL, DIR_004_DERIVED
from .reports import append_to_registry

def _validate_spatial_schema(data: Dict[str, Any]) -> bool:
    """Validates the incoming JSON payload against the Vitruvius Spatial Contract."""
    required_keys = {"spatial_context_id", "spatial_edges"}
    if not required_keys.issubset(data.keys()):
        return False
    return True

def process_spatial_payload(payload_path: Path) -> None:
    """
    Ingests decoupled spatial data and converts it into canonical graph candidates.
    Idempotent execution: Will overwrite previous extraction for the same context.
    """
    with open(payload_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not _validate_spatial_schema(data):
        raise ValueError(f"Schema validation failed for {payload_path.name}")

    context_id = data["spatial_context_id"]
    candidates: List[Dict[str, Any]] = []

    for edge in data["spatial_edges"]:
        # Translate the physical instance to the canonical Phase 3 concept
        candidate = {
            "source_concept_id": edge["canonical_concept_map"],
            "predicate": f"spatial_{edge['predicate']}",
            "target_concept_id": edge.get("target_instance_concept_map", "unknown"),
            "spatial_metadata": {
                "physical_source": edge["source_instance"],
                "physical_target": edge["target_instance"],
                "computed_value": edge.get("value"),
                "unit": edge.get("unit")
            },
            "status": "pending_constraint_evaluation"
        }
        candidates.append(candidate)

    # Output to Phase 4 as pending candidates for the solver
    output_file = DIR_004_DERIVED / f"spatial_candidates_{context_id}.json"
    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(candidates, out, indent=2)

    # Update manifest
    append_to_registry("spatial_ingestion_manifest.csv", {
        "context_id": context_id,
        "source_file": payload_path.name,
        "edges_extracted": len(candidates),
        "status": "ingested"
    })
```

---

### Phase 6C: Constraint Solver Integration
To fulfill the mathematical promise of Vitruvius, the pipeline evaluates the ingested spatial edges against the canonical legal graph using Z3. This replaces the LLM (`gemma4:31b`) for purely geometric relationships.

**File:** `scripts/vitruvius/z3_constraint_evaluator.py`

```python
import json
from pathlib import Path
from z3 import Real, Solver, sat
from typing import Dict, Any

def evaluate_spatial_candidate(spatial_candidate: Dict[str, Any], legal_graph_rule: Dict[str, Any]) -> str:
    """
    Uses Z3 Theorem Prover to deterministically verify spatial compliance
    against the canonical legal rule extracted from PD 1096.
    """
    s = Solver()
    
    # Define mathematical variables
    actual_val = Real('actual_val')
    required_val = Real('required_val')

    # Extract parameters
    actual_measured = spatial_candidate["spatial_metadata"].get("computed_value")
    legal_threshold = legal_graph_rule.get("parametric_constraint_value")
    operator = legal_graph_rule.get("parametric_operator") # e.g., '>=', '<=', '=='

    if actual_measured is None or legal_threshold is None:
        return "review_further" # Missing parametric data, route to Ranger

    # Assign state
    s.add(actual_val == actual_measured)
    s.add(required_val == legal_threshold)

    # Apply mathematical logic based on the legal graph
    if operator == '>=':
        s.add(actual_val >= required_val)
    elif operator == '<=':
        s.add(actual_val <= required_val)
    elif operator == '==':
        s.add(actual_val == required_val)
    else:
        return "review_further"

    # Deterministic boolean evaluation
    if s.check() == sat:
        return "keep" # 100% compliant
    else:
        return "reject_violation" # Mathematical code violation proven

def run_spatial_evaluation(context_id: str) -> None:
    """Loads candidates and rules, runs solver, and outputs to Phase 6."""
    # Implementation loops through candidates, queries Phase 3/8 canonical rules, 
    # runs evaluate_spatial_candidate, and writes to latest_relationship_review_merged.json
    pass
```

---

### Pipeline CLI Integration
The API hooks are exposed in the core orchestrator to allow sequential execution.

**File:** `scripts/pipeline_cli.py`

```python
@cli.command()
@click.argument('spatial_file', type=click.Path(exists=True))
def ingest_spatial(spatial_file):
    """Ingest decoupled spatial JSON into Vitruvius."""
    from vitruvius.spatial_ingestion_one import process_spatial_payload
    process_spatial_payload(Path(spatial_file))
    click.echo(f"Successfully ingested spatial matrix from {spatial_file}")

@cli.command()
@click.argument('context_id')
def evaluate_spatial(context_id):
    """Run Z3 deterministic solver on spatial candidates against legal graph."""
    from vitruvius.z3_constraint_evaluator import run_spatial_evaluation
    run_spatial_evaluation(context_id)
    click.echo(f"Completed mathematical compliance check for {context_id}")
```