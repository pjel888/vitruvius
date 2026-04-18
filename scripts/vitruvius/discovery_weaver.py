import json
import os
import re
import sys
import argparse
import random
import yaml
import subprocess
from pathlib import Path
from typing import Any, List, Dict, Optional
from datetime import datetime, timezone
from contextlib import redirect_stdout, redirect_stderr

# Add scripts directory to path for robust imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from vitruvius.ollama_review import call_ollama
    from vitruvius.config import get_ollama_default_model, get_ollama_url
    from vitruvius.paths import get_repo_root
    from vitruvius.utils import utc_now_stamp
    from vitruvius.conversion import run_convert_one
except ImportError:
    def get_repo_root(): return Path.cwd()
    def get_ollama_default_model(): return "llama3.1:8b"
    def get_ollama_url(): return "http://localhost:11434"
    def utc_now_stamp(): return "2026-04-18T00:00:00Z"
    def call_ollama(prompt: str, model: str, timeout_seconds: int) -> str: return "{}"
    def run_convert_one(path: str): return 0

class DiscoveryWeaver:
    """The Autonomous Architect with Professional UX/UI and Audit Logging."""
    
    def __init__(self, model: str = None, dry_run: bool = True):
        self.repo_root = get_repo_root()
        self.model = model or get_ollama_default_model()
        self.dry_run = dry_run
        
        # Directories
        self.raw_dir = self.repo_root / "001_Raw-Source-Layer"
        self.conv_dir = self.repo_root / "002_Raw-Conversion-Layer"
        self.concepts_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
        self.sources_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
        self.relationships_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
        self.log_dir = self.repo_root / "006_System-Manifests" / "logs"
        self.run_dir = self.repo_root / "006_System-Manifests" / "runs"
        
        # Data
        self.identity_manifest_path = self.repo_root / "006_System-Manifests" / "registries" / "authoritative_identities.yaml"
        self.identities = self._load_identities()
        self.noise_filters = ["index", "log", "README", "sidecar_json", "raw_markdown", "refined_markdown"]
        
        # Audit Tracker
        self.audit_ledger = {
            "run_id": utc_now_stamp(),
            "model": self.model,
            "status": "in-progress",
            "counts": {"success": 0, "failed": 0, "ocr_required": 0, "skipped": 0},
            "events": []
        }
        
        # Setup paths and Java
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self._setup_java_env()

    def _setup_java_env(self):
        common_paths = [
            r"C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin",
            r"C:\Program Files\Java\jdk-21\bin"
        ]
        for p in common_paths:
            if Path(p).exists() and p not in os.environ["PATH"]:
                os.environ["PATH"] = p + os.pathsep + os.environ["PATH"]

    def _load_identities(self) -> Dict:
        if self.identity_manifest_path.exists():
            data = yaml.safe_load(self.identity_manifest_path.read_text(encoding="utf-8"))
            return data.get("identities", {})
        return {}

    def _get_text_context(self, path: Path, max_chars: int = 3000) -> str:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            if "---" in content:
                parts = content.split("---")
                if len(parts) >= 3: content = parts[2]
            return re.sub(r'\s+', ' ', content).strip()[:max_chars]
        except Exception: return ""

    def _clean_json(self, text: str) -> str:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        return match.group(0) if match else text

    def log_event(self, level: str, message: str, details: Dict = None):
        """Adds a structured event to the audit ledger."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message,
            "details": details or {}
        }
        self.audit_ledger["events"].append(event)
        # Final status check will be written at the end

    def build_entire_graph(self, family_id: str, limit: int = 5):
        print(f"\n🏗️  BUILDING FAMILY: {family_id}")
        raw_family_dir = self.raw_dir / family_id
        if not raw_family_dir.exists(): return

        pdfs = sorted([p for p in raw_family_dir.rglob("*.pdf") if p.stem.lower() not in self.noise_filters])
        total = min(limit, len(pdfs))
        
        for idx, pdf in enumerate(pdfs):
            if idx >= limit: break
            
            rel_pdf_path = str(pdf.relative_to(self.raw_dir)).replace("\\", "/")
            identity = self.identities.get(rel_pdf_path)
            
            if not identity:
                self.audit_ledger["counts"]["skipped"] += 1
                continue

            print(f"  [{idx+1}/{total}] Processing: {identity['authoritative_title']}...")
            
            refined_md = self.conv_dir / family_id / "refined_markdown" / f"{pdf.stem}.md"
            
            # 1. Silenced Conversion
            if not refined_md.exists():
                engine_log = self.log_dir / "engine_trace.log"
                with open(engine_log, "a") as f:
                    with redirect_stdout(f), redirect_stderr(f):
                        try:
                            rc = run_convert_one(rel_pdf_path)
                            if rc != 0:
                                self.log_event("ERROR", f"Conversion failed for {pdf.name}")
                                self.audit_ledger["counts"]["failed"] += 1
                                continue
                        except Exception as e:
                            self.log_event("ERROR", f"Exception during conversion: {e}")
                            self.audit_ledger["counts"]["failed"] += 1
                            continue

            # 2. Admission & Discovery
            if refined_md.exists() or self.dry_run:
                self._save_source(identity, pdf.stem)
                concepts = self.discover_concepts_from_raw(refined_md if refined_md.exists() else pdf)
                
                if not self.dry_run:
                    for c in concepts:
                        self._save_concept(c['slug'], c['definition'], identity['authoritative_title'])
                    
                    if concepts:
                        self._weave_new_to_existing([c['slug'] for c in concepts if 'slug' in c])
                    
                    if identity.get("implements_law_id"):
                        self._bridge_law_irr(identity)
                
                self.audit_ledger["counts"]["success"] += 1
                self.log_event("SUCCESS", f"Fully processed {identity['authoritative_title']}")

    def discover_concepts_from_raw(self, path: Path):
        context = self._get_text_context(path)
        prompt = f"Propose 5 core concepts for this architectural doc. Return ONLY JSON. Content: {context}"
        try:
            data = json.loads(self._clean_json(call_ollama(prompt, self.model, 120)))
            return data.get("concepts", [])
        except Exception: return []

    def _save_source(self, identity: Dict, original_stem: str):
        out_path = self.sources_dir / f"{identity['canonical_id']}.md"
        content = f"---\nid: {identity['canonical_id']}\ntitle: \"{identity['authoritative_title']}\"\npage_type: source\ntrust_level: {identity['trust_level']}\nsummary: \"{identity['summary']}\"\noriginal_file: {original_stem}.pdf\n---"
        if not self.dry_run and not out_path.exists():
            out_path.write_text(content, encoding="utf-8")

    def _save_concept(self, slug, definition, source_title):
        content = f"---\nid: concept-{slug}\ntitle: {slug.replace('-', ' ').title()}\nsource_origin: \"{source_title}\"\n---\n# {slug}\n{definition}"
        out_path = self.concepts_dir / f"{slug}.md"
        if not out_path.exists(): out_path.write_text(content, encoding="utf-8")

    def _weave_new_to_existing(self, new_concept_ids: List[str]):
        laws_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
        laws = [{"id": p.stem, "path": p} for p in laws_dir.glob("*.md") if "law-" in p.stem]
        for new_id in new_concept_ids:
            if not laws: break
            for law in random.sample(laws, min(len(laws), 2)):
                prompt = f"Connect '{new_id}' and '{law['id']}'. Return JSON {{'connected': bool, 'type': 'string', 'reason': 'string'}}"
                try:
                    p = json.loads(self._clean_json(call_ollama(prompt, self.model, 90)))
                    if p.get("connected"): self._save_relationship(new_id, law['id'], p)
                except Exception: pass

    def _bridge_law_irr(self, identity: Dict):
        prop = {"type": "implements", "reason": f"Identity discovery confirmed implements {identity['implements_law_id']}."}
        self._save_relationship(identity['canonical_id'], identity['implements_law_id'], prop)

    def _save_relationship(self, a_id, b_id, prop):
        rel_id = f"rel-{a_id}-{prop['type']}-{b_id}"
        out_path = self.relationships_dir / f"{rel_id}.md"
        content = f"---\nid: {rel_id}\nfrom_entity: {a_id}\nto_entity: {b_id}\nrelationship_type: {prop['type']}\n---\n# {a_id} -> {b_id}\n{prop.get('reason','')}"
        if not self.dry_run and not out_path.exists(): out_path.write_text(content, encoding="utf-8")

    def autogenerate_visualization(self):
        print(f"\n🎨 Rendering Knowledge Graph...")
        try:
            # Rebuild graph silently
            log_path = self.log_dir / "graph_build.log"
            with open(log_path, "w") as f:
                with redirect_stdout(f), redirect_stderr(f):
                    subprocess.run([sys.executable, str(self.repo_root / "scripts" / "pipeline_cli.py"), "build-graph"], check=True)
            
            snapshot = self.repo_root / "005_Operational-Intelligence-Layer" / "graph" / "latest_graph_snapshot.json"
            out = self.repo_root / "004_Derived-Content-Layer" / "graph-visualizations" / "expansive-brain-mvp.html"
            subprocess.run([sys.executable, str(self.repo_root / "scripts" / "pipeline_cli.py"), "visualize-graph", "--snapshot", str(snapshot), "--out", str(out)], check=True, capture_output=True)
            print(f"✨ SUCCESS: Graph updated at {out}")
        except Exception as e: print(f"⚠️ Visualization Error: {e}")

    def finalize_audit(self):
        self.audit_ledger["status"] = "complete"
        audit_path = self.run_dir / f"discovery_audit_{utc_now_stamp()}.json"
        audit_path.write_text(json.dumps(self.audit_ledger, indent=2), encoding="utf-8")
        print(f"\n📝 Audit Ledger saved: {audit_path}")
        print(f"📊 Results: {self.audit_ledger['counts']['success']} success, {self.audit_ledger['counts']['failed']} failed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vitruvius Ultimate Discovery Weaver")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--model", type=str, default="llama3.1:8b")
    parser.add_argument("--families", nargs="+")
    args = parser.parse_args()
    
    weaver = DiscoveryWeaver(model=args.model, dry_run=not args.execute)
    targets = args.families or ["001-Laws", "002-History", "003-Theory", "004-Technology"]
    for t in targets: weaver.build_entire_graph(t, limit=args.limit)
    weaver.autogenerate_visualization()
    weaver.finalize_audit()
