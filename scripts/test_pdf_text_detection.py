from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    print("ERROR: pypdf is not installed.")
    print("Run: pip install pypdf")
    raise SystemExit(1)


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def detect_pdf_text(pdf_path: Path, sample_pages: int = 5) -> int:
    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        return 1

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    pages_to_check = min(sample_pages, total_pages)

    total_chars = 0
    pages_with_text = 0

    print(f"PDF: {pdf_path}")
    print(f"Total pages: {total_pages}")
    print(f"Pages sampled: {pages_to_check}")
    print()

    for i in range(pages_to_check):
        raw = reader.pages[i].extract_text() or ""
        text = normalize_text(raw)
        char_count = len(text)

        if char_count >= 50:
            pages_with_text += 1

        total_chars += char_count

        print(f"Page {i + 1}: {char_count} extracted characters")

    print()
    print(f"Pages with usable text: {pages_with_text}/{pages_to_check}")
    print(f"Total extracted characters in sample: {total_chars}")

    likely_text_pdf = (
        pages_with_text >= max(1, pages_to_check // 2)
        and total_chars >= 300
    )

    print()

    if likely_text_pdf:
        print("RESULT: TEXT_PDF")
        print("This PDF likely already has extractable text.")
        print("Route: OpenDataLoader directly.")
    else:
        print("RESULT: LIKELY_SCANNED_PDF")
        print("This PDF likely needs OCR first.")
        print("Route: OCR first, then OpenDataLoader.")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect whether a PDF already has extractable text")
    parser.add_argument("relative_pdf_path", help="Path relative to 001_Raw-Source-Layer")
    parser.add_argument("--sample-pages", type=int, default=5, help="How many pages to sample")
    args = parser.parse_args()

    repo_root = get_repo_root()
    pdf_path = repo_root / "001_Raw-Source-Layer" / args.relative_pdf_path

    return detect_pdf_text(pdf_path, sample_pages=args.sample_pages)


if __name__ == "__main__":
    raise SystemExit(main())