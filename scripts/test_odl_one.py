from pathlib import Path
import opendataloader_pdf

repo_root = Path(__file__).resolve().parent.parent

input_pdf = repo_root / "001_Raw-Source-Layer" / "001-Laws" / "PD-1096" / "PD 1096 - National Building Code.pdf"
output_dir = repo_root / "002_Raw-Conversion-Layer" / "001-Laws"

print(f"Input PDF: {input_pdf}")
print(f"Output dir: {output_dir}")

output_dir.mkdir(parents=True, exist_ok=True)

opendataloader_pdf.convert(
    input_path=[str(input_pdf)],
    output_dir=str(output_dir),
    format="markdown,json"
)

print("Done.")