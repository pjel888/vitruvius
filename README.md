# Vitruvius

## 🚀 Quick Start (Clean Build: 341 Sources)

To build your expansive, interconnected knowledge graph locally using Llama 3.1:8b with our **Clean UX** (no terminal spam):

```powershell
# 1. Provision Identities (Distills 341 PDFs into Beautiful Titles & IDs)
$env:PYTHONPATH="scripts"; python scripts/vitruvius/identity_provisioner.py --limit 400 --execute

# 2. Master Clean Build (Convert, Extract, Weave, and Visualize)
$env:PYTHONPATH="scripts"; python scripts/vitruvius/discovery_weaver.py --limit 400 --model "llama3.1:8b" --execute
```

The resulting interactive graph will be saved to:
`004_Derived-Content-Layer/graph-visualizations/expansive-brain-mvp.html`

---

```
 ██╗   ██╗██╗████████╗██████╗ ██╗   ██╗██╗   ██╗██╗██╗   ██╗███████╗
 ██║   ██║██║╚══██╔══╝██╔══██╗██║   ██║██║   ██║██║██║   ██║██╔════╝
 ██║   ██║██║   ██║   ██████╔╝██║   ██║██║   ██║██║██║   ██║███████╗
 ╚██╗ ██╔╝██║   ██║   ██╔══██╗██║   ██║╚██╗ ██╔╝██║██║   ██║╚════██║
  ╚████╔╝ ██║   ██║   ██║  ██║╚██████╔╝ ╚████╔╝ ██║╚██████╔╝███████║
   ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚═╝ ╚═════╝ ╚══════╝

   ─────────────────────────────────────────────────────────────────
     An auditable document-to-knowledge engine for technical rule systems.
         Building toward compliance-grade reasoning and AEC decision support.
                    Firmitas · Utilitas · Venustas
   ─────────────────────────────────────────────────────────────────
```

### 🧠 The "Clean Build" Intelligence System
The Vitruvius build process is designed for a **Professional-Grade UX**, separating high-level progress from technical engine noise.

- **Silenced Engine Noise:** All Java, Unicode, and PDF parser warnings are automatically redirected to `006_System-Manifests/logs/engine_trace.log`.
- **Live Dashboard:** Your terminal only shows high-level, numbered progress (e.g., `[5/341] Processing "The Architecture Act"...`).
- **Automated Visualization:** The interactive HTML graph is automatically updated at the end of every run.
- **Audit Ledger:** A detailed JSON record of every document's success or failure is saved to `006_System-Manifests/runs/` for audit checks.

---

**Vitruvius is, today, an auditable document-to-knowledge pipeline for complex
technical and regulatory corpora** — with the built environment as its primary
target domain in this repository. It ingests messy source material, converts it
into machine-readable text, refines and canonicalizes that text into structured
knowledge, and builds governed relationships, graph artifacts, and traceable
query surfaces on top of it.

> **Current product posture:** Vitruvius is still **pre-launch**. The goal
> right now is to build the most effective, accurate, and truthful MVP.

### Local-First Operation (No Cloud AI Required)
Vitruvius is a **self-contained intelligence system**. Once the orchestration scripts are written, it runs entirely on your local hardware using your GPU (RTX 4070) and does not require Cloud AI (like Gemini/OpenAI).

#### Prerequisites for Local Build
- **Ollama:** Installed and running locally (`llama3.1:8b`).
- **Java:** OpenJDK 21+ (Required for PDF-to-Markdown conversion).

### Knowledge Graph Persistence
All discovered knowledge is **hardcoded** into the `003_Canonical-Knowledge-Layer/` as permanent Markdown files. This ensures your "Digital Brain" is stable, auditable, and yours to keep forever without monthly API bills.

---

## Filesystem layers

| Layer | Folder | Role |
|---|---|---|
| 1 | `001_Raw-Source-Layer/` | Immutable input. Original PDFs, Office docs. |
| 2 | `002_Raw-Conversion-Layer/` | Machine extracts. (Git-ignored) |
| 3 | `003_Canonical-Knowledge-Layer/` | **The Brain.** Hardcoded trusted knowledge. |
| 4 | `004_Derived-Content-Layer/` | HTML Visualizations. (Git-ignored) |
| 5 | `005_Operational-Intelligence-Layer/` | Graph Snapshots. (Git-ignored) |
| 6 | `006_System-Manifests/` | Registries, Identities, and Audit Logs. |

---

## License & attribution
Vitruvius is a **headless, mathematically rigorous AEC physics and compliance engine**. Public-domain Philippine law (PD 1096, etc.) serves as the reference development corpus. Vertical specialization into AEC is deliberate: it lets every line of optimization work target spatial geometry, clash detection, and building code compliance.
