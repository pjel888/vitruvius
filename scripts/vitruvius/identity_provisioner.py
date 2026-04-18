import json
import os
import re
import sys
import argparse
import yaml
from pathlib import Path
from typing import Any, List, Dict, Optional
import pypdf

# Add scripts directory to path for robust imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from vitruvius.ollama_review import call_ollama
    from vitruvius.config import get_ollama_default_model, get_ollama_url
    from vitruvius.paths import get_repo_root
    from vitruvius.utils import utc_now_stamp
except ImportError:
    def get_repo_root(): return Path.cwd()
    def get_ollama_default_model(): return "llama3.1:8b"
    def get_ollama_url(): return "http://localhost:11434"
    def utc_now_stamp(): return "2026-04-18T00:00:00Z"
    def call_ollama(prompt: str, model: str, timeout_seconds: int) -> str: return "{}"

class IdentityProvisioner:
    """The Architect that determines the formal identity of raw documents."""
    
    def __init__(self, model: str = None, dry_run: bool = True):
        self.repo_root = get_repo_root()
        self.model = model or get_ollama_default_model()
        self.dry_run = dry_run
        self.raw_dir = self.repo_root / "001_Raw-Source-Layer"
        self.manifest_path = self.repo_root / "006_System-Manifests" / "registries" / "authoritative_identities.yaml"
        self.identities = self._load_manifest()

    def _load_manifest(self) -> Dict:
        if self.manifest_path.exists():
            return yaml.safe_load(self.manifest_path.read_text(encoding="utf-8")) or {}
        return {"version": 1, "identities": {}}

    def _save_manifest(self):
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(yaml.dump(self.identities, sort_keys=False), encoding="utf-8")

    def _get_pdf_text(self, pdf_path: Path, max_chars: int = 4000) -> str:
        """Extracts the beginning of a PDF to identify its content."""
        try:
            with open(pdf_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                text = ""
                for page in reader.pages[:3]: # Check first 3 pages
                    text += page.extract_text() or ""
                    if len(text) > max_chars: break
                return text[:max_chars]
        except Exception as e:
            print(f"      ⚠️ PDF Read Error: {e}")
            return ""

    def provision_all(self, limit: int = 20):
        print(f"🚀 Starting Identity Provisioning Pass (Model: {self.model})")
        pdfs = sorted(list(self.raw_dir.rglob("*.pdf")))
        
        count = 0
        for pdf in pdfs:
            if count >= limit: break
            
            rel_path = str(pdf.relative_to(self.raw_dir)).replace("\\", "/")
            if rel_path in self.identities["identities"]:
                continue

            print(f"🔍 Identifying: {pdf.name}...")
            context = self._get_pdf_text(pdf)
            
            prompt = f"""Role: Senior Archivist & Knowledge Architect.
Task: Identify the authoritative identity and legal lineage of this document.

Document Content Snippet:
{context}

Original Filename: {pdf.name}

Instructions:
1. Provide a formal, human-readable Title.
2. Propose a Canonical ID format: <type>-<slug>.
3. Determine Trust Level (1=Law, 2=Official Manual, 3=Textbook, 4=Handout).
4. LEGAL LINEAGE: If this is an IRR (Implementing Rules and Regulations), identify the specific LAW it implements and provide its ID.

Return ONLY valid JSON:
{{
  "title": "string",
  "canonical_id": "string",
  "trust_level": int,
  "page_type": "string",
  "implements_law_id": "string or null",
  "aliases": ["string"],
  "summary": "1-sentence summary"
}}
"""
            try:
                response = call_ollama(prompt, self.model, 120)
                match = re.search(r'\{.*\}', response, re.DOTALL)
                if not match: continue
                data = json.loads(match.group(0))
                
                print(f"    ✅ PROVISIONED: {data['title']}")
                if data.get('implements_law_id'):
                    print(f"       🔗 IMPLEMENTS: {data['implements_law_id']}")
                
                self.identities["identities"][rel_path] = {
                    "authoritative_title": data["title"],
                    "canonical_id": data["canonical_id"],
                    "trust_level": data["trust_level"],
                    "page_type": data["page_type"],
                    "implements_law_id": data.get("implements_law_id"),
                    "aliases": data["aliases"],
                    "summary": data["summary"],
                    "provisioned_at": utc_now_stamp(),
                    "model": self.model
                }
                count += 1
                
                if not self.dry_run:
                    self._save_manifest()
                    
            except Exception as e:
                print(f"    ❌ Error provisioning {pdf.name}: {e}")

        print(f"\n✨ Provisioning pass complete. {count} new identities added.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vitruvius Identity Provisioner")
    parser.add_argument("--execute", action="store_true", help="Commit identities to manifest")
    parser.add_argument("--limit", type=int, default=20, help="Max PDFs to provision")
    parser.add_argument("--model", type=str, default="llama3.1:8b")
    args = parser.parse_args()
    
    provisioner = IdentityProvisioner(model=args.model, dry_run=not args.execute)
    provisioner.provision_all(limit=args.limit)
