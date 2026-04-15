//! Sprint RUST-PDF-1 — audit crate.
//!
//! Minimal Rust → Python bridge that extracts text from a PDF byte
//! buffer using `lopdf`. The goal is to measure peak RAM + wall-time
//! vs the Python `docling` and `opendataloader_pdf` stacks, not to
//! ship a production parser.

use lopdf::Document;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

/// Extract text from a PDF byte buffer.
///
/// Returns the extracted text as a single string. Pages are separated
/// by form-feed characters (\x0c) which the Python caller can split on.
/// Empty input returns an empty string. Unparseable PDFs raise ValueError.
#[pyfunction]
fn extract_pdf_text(pdf_bytes: &[u8]) -> PyResult<String> {
    if pdf_bytes.is_empty() {
        return Ok(String::new());
    }

    let doc = match Document::load_mem(pdf_bytes) {
        Ok(d) => d,
        Err(e) => {
            return Err(PyValueError::new_err(format!(
                "lopdf failed to parse PDF: {}",
                e
            )))
        }
    };

    let mut out = String::new();
    for (page_num, _page_id) in doc.get_pages() {
        match doc.extract_text(&[page_num]) {
            Ok(text) => {
                out.push_str(&text);
                out.push('\x0c');
            }
            Err(_) => {
                // Skip pages that lopdf can't decode; don't fail the whole doc.
                out.push('\x0c');
            }
        }
    }

    Ok(out)
}

/// Sprint CLEANUP-1 Stream C3.1 — surface per-page decode errors.
///
/// Returns a tuple of ``(concatenated_text, failed_page_numbers)``
/// where ``failed_page_numbers`` is a ``Vec<i64>`` of 1-indexed page
/// positions for which ``lopdf`` raised during ``extract_text``.
///
/// Unlike [`extract_pdf_text`], this function does NOT swallow the
/// per-page errors silently — it records the page index and keeps
/// going. The caller (Python) gets both the concatenated text (same
/// form-feed-separated layout as [`extract_pdf_text`], so existing
/// markdown post-processing stays byte-identical on the happy path)
/// and the list of failed pages for surfacing in telemetry.
///
/// Empty input returns ``("", [])``. A PDF that ``lopdf`` cannot even
/// open still raises ``PyValueError`` — per-page isolation kicks in
/// only after the document parses.
#[pyfunction]
fn extract_pdf_text_with_errors(pdf_bytes: &[u8]) -> PyResult<(String, Vec<i64>)> {
    if pdf_bytes.is_empty() {
        return Ok((String::new(), Vec::new()));
    }

    let doc = match Document::load_mem(pdf_bytes) {
        Ok(d) => d,
        Err(e) => {
            return Err(PyValueError::new_err(format!(
                "lopdf failed to parse PDF: {}",
                e
            )))
        }
    };

    let mut out = String::new();
    let mut failed_pages: Vec<i64> = Vec::new();

    // `doc.get_pages()` returns a map keyed by 1-indexed page numbers.
    // We iterate in insertion order (matching `extract_pdf_text` above)
    // and report the 1-indexed page number on error.
    for (page_num, _page_id) in doc.get_pages() {
        match doc.extract_text(&[page_num]) {
            Ok(text) => {
                out.push_str(&text);
                out.push('\x0c');
            }
            Err(_) => {
                // Record the page number and emit the separator so
                // the caller's form-feed-split page alignment is
                // preserved (blank page in the output stream stands
                // in for the failed decode).
                failed_pages.push(page_num as i64);
                out.push('\x0c');
            }
        }
    }

    Ok((out, failed_pages))
}

/// Version string for smoke-testing the Python binding.
#[pyfunction]
fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pymodule]
fn vitruvius_rust_pdf(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(extract_pdf_text, m)?)?;
    m.add_function(wrap_pyfunction!(extract_pdf_text_with_errors, m)?)?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    Ok(())
}
