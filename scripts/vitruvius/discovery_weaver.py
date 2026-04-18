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
    """The Autonomous Architect that builds the entire Knowledge Graph using Authoritative Identities."""
    
    def __init__(self, model: str = None, dry_run: bool = True):
        self.repo_root = get_repo_root()
        self.model = model or get_ollama_default_model()
        self.dry_run = dry_run
        self.raw_dir = self.repo_root / "001_Raw-Source-Layer"
        self.conv_dir = self.repo_root / "002_Raw-Conversion-Layer"
        self.concepts_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
        self.sources_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
        self.relationships_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
        self.identity_manifest_path = self.repo_root / "006_System-Manifests" / "registries" / "authoritative_identities.yaml"
        self.identities = self._load_identities()
        self.noise_filters = ["index", "log", "README", "sidecar_json", "raw_markdown", "refined_markdown"]
        
        # Robust Java Detection for Windows
        self._setup_java_env()

    def _setup_java_env(self):
        """Ensures Java is in the PATH for the current session."""
        common_paths = [
            r"C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin",
            r"C:\Program Files\Java\jdk-21\bin",
            r"C:\Program Files\Eclipse Adoptium\jdk-21.0.2.13-hotspot\bin"
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
            content = re.sub(r'\s+', ' ', content)
            return content.strip()[:max_chars]
        except Exception: return ""

    def _clean_json(self, text: str) -> str:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        return match.group(0) if match else text

    def build_entire_graph(self, family_id: str, limit: int = 5):
        print(f"\n🚀 BUILDING TOP-NOTCH GRAPH FOR: {family_id}")
        raw_family_dir = self.raw_dir / family_id
        if not raw_family_dir.exists(): return

        pdfs = sorted([p for p in raw_family_dir.rglob("*.pdf") if p.stem.lower() not in self.noise_filters])
        count = 0
        for pdf in pdfs:
            if count >= limit: break
            
            rel_pdf_path = str(pdf.relative_to(self.raw_dir)).replace("\\", "/")
            identity = self.identities.get(rel_pdf_path)
            
            if not identity: continue

            refined_md = self.conv_dir / family_id / "refined_markdown" / f"{pdf.stem}.md"
            
            # 1. Convert
            if not refined_md.exists():
                print(f"  📥 Step 1: Converting {identity['authoritative_title']}...")
                if not self.dry_run:
                    try:
                        run_convert_one(rel_pdf_path)
                    except Exception as e:
                        print(f"    ⚠️ Conversion Error: {e}")
                        continue
            
            # 2. Admit Source & Concepts
            if refined_md.exists() or self.dry_run:
                self._save_source(identity, pdf.stem)
                
                print(f"  🧠 Step 2: AI Discovery for {identity['authoritative_title']}...")
                concepts = self.discover_concepts_from_raw(refined_md if refined_md.exists() else pdf)
                
                new_ids = [c['slug'] for c in concepts if 'slug' in c]
                for c in concepts:
                    if not self.dry_run:
                        self._save_concept(c['slug'], c['definition'], identity['authoritative_title'])
                
                # 3. Weaving
                if new_ids:
                    print(f"  🕸️ Step 3: Weaving connections to Laws...")
                    self._weave_new_to_existing(new_ids)
                    
                # 4. Auto-bridge Law-IRR
                if identity.get("implements_law_id"):
                    self._bridge_law_irr(identity)
                
                count += 1

    def _save_source(self, identity: Dict, original_stem: str):
        out_path = self.sources_dir / f"{identity['canonical_id']}.md"
        content = f"""---
id: {identity['canonical_id']}
title: {identity['authoritative_title']}
page_type: source
trust_level: {identity['trust_level']}
summary: "{identity['summary']}"
original_file: {original_stem}.pdf
status: authoritative-discovery
generated_at: {utc_now_stamp()}
---

# {identity['authoritative_title']}

## Summary
{identity['summary']}
"""
        if not self.dry_run and not out_path.exists():
            out_path.write_text(content, encoding="utf-8")
            print(f"    💾 ADMITTED SOURCE: {identity['authoritative_title']}")

    def discover_concepts_from_raw(self, path: Path):
        context = self._get_text_context(path)
        prompt = f"Propose 5 core concepts for this architectural doc. Return ONLY JSON. Content: {context}"
        try:
            data = json.loads(self._clean_json(call_ollama(prompt, self.model, 120)))
            return data.get("concepts", [])
        except Exception: return []

    def _save_concept(self, slug, definition, source_title):
        content = f"---\nid: concept-{slug}\ntitle: {slug.replace('-', ' ').title()}\nstatus: autonomous-ai-admission\nsource_origin: \"{source_title}\"\n---\n# {slug}\n{definition}"
        out_path = self.concepts_dir / f"{slug}.md"
        if not out_path.exists():
            out_path.write_text(content, encoding="utf-8")

    def _weave_new_to_existing(self, new_concept_ids: List[str]):
        laws_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
        laws = [{"id": p.stem, "path": p} for p in laws_dir.glob("*.md") if "law-" in p.stem]
        for new_id in new_concept_ids:
            if not laws: break
            for law in random.sample(laws, min(len(laws), 2)):
                prompt = f"Connect '{new_id}' and '{law['id']}'. Return JSON {{'connected': bool, 'type': 'string', 'reason': 'string', 'confidence': float}}"
                try:
                    p = json.loads(self._clean_json(call_ollama(prompt, self.model, 90)))
                    if p.get("connected") and p.get("confidence", 0) > 0.8:
                        self._save_relationship(new_id, law['id'], p)
                except Exception: pass

    def _bridge_law_irr(self, identity: Dict):
        prop = {"type": "implements", "reason": f"Authoritative identity discovery confirmed this {identity['page_type']} implements {identity['implements_law_id']}."}
        self._save_relationship(identity['canonical_id'], identity['implements_law_id'], prop)

    def _save_relationship(self, a_id, b_id, prop):
        rel_id = f"rel-{a_id}-{prop['type']}-{b_id}"
        out_path = self.relationships_dir / f"{rel_id}.md"
        content = f"---\nid: {rel_id}\nfrom_entity: {a_id}\nto_entity: {b_id}\nrelationship_type: {prop['type']}\nmodel: {self.model}\n---\n# {a_id} -> {b_id}\n{prop['reason']}"
        if not self.dry_run and not out_path.exists():
            out_path.write_text(content, encoding="utf-8")
            print(f"    💾 SAVED RELATIONSHIP: {rel_id}")

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
