from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from vitruvius.conversion import convert_pdf_at_path
from vitruvius.wiki.docling_parser import DoclingParseResult


def test_convert_pdf_at_path_falls_back_to_docling_when_opendataloader_fails(tmp_path: Path):
    repo_root = tmp_path
    pdf = repo_root / 'sample.pdf'
    pdf.write_bytes(b'%PDF-1.4\n')

    conversion_root = repo_root / '002_Raw-Conversion-Layer'
    conversion_root.mkdir(parents=True)

    fake_docling = DoclingParseResult(
        markdown='# Title\n\nBody text.',
        heading_count=1,
        table_count=0,
        error=None,
    )

    with patch('vitruvius.conversion.get_repo_root', return_value=repo_root), \
         patch('vitruvius.conversion.opendataloader_pdf.convert', side_effect=RuntimeError('odl boom')), \
         patch('vitruvius.conversion.convert_pdf_to_markdown', return_value=fake_docling), \
         patch('vitruvius.conversion._write_conversion_registry_entry') as registry_write:
        result = convert_pdf_at_path(pdf, '001-Laws/sample.pdf')

    markdown_path = conversion_root / '001-Laws' / 'raw_markdown' / 'sample.md'
    json_path = conversion_root / '001-Laws' / 'sidecar_json' / 'sample.json'
    assert markdown_path.read_text(encoding='utf-8') == '# Title\n\nBody text.'
    payload = json.loads(json_path.read_text(encoding='utf-8'))
    assert payload['parser'] == 'docling_fallback'
    assert result['status'] == 'converted_via_docling_fallback'
    assert registry_write.call_args.kwargs['processing_route'] == 'DOCLING_FALLBACK'
