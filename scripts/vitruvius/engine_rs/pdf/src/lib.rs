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

/// Version string for smoke-testing the Python binding.
#[pyfunction]
fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pymodule]
fn vitruvius_rust_pdf(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(extract_pdf_text, m)?)?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    Ok(())
}
