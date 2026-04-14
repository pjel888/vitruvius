"""AST-based semantic chunker — deterministic, idempotent, parent-aware."""

from __future__ import annotations

import textwrap

from vitruvius.normalization.ast_chunker import (
    DEFAULT_MAX_TOKENS,
    Chunk,
    split_into_chunks,
)


SMALL_DOC = textwrap.dedent("""\
    # NATIONAL BUILDING CODE

    Preamble paragraph about the code.

    ## CHAPTER 1: GENERAL PROVISIONS

    This chapter covers general provisions.

    ### SECTION 101. Title

    This Decree shall be known as the National Building Code.

    ### SECTION 102. Declaration of Policy

    It is hereby declared to be the policy of the State to safeguard life.
""")


def test_small_document_fits_in_one_chunk_per_section() -> None:
    chunks = split_into_chunks(SMALL_DOC, source_path="pd1096.md")
    section_chunks = [c for c in chunks if "SECTION" in c.heading]
    assert len(section_chunks) == 2


def test_parent_title_injected_as_metadata() -> None:
    chunks = split_into_chunks(SMALL_DOC, source_path="pd1096.md")
    section_chunks = [c for c in chunks if "SECTION 101" in c.heading]
    assert section_chunks
    titles = section_chunks[0].parent_titles
    assert any("NATIONAL BUILDING CODE" in t for t in titles)
    assert any("CHAPTER 1" in t for t in titles)


def test_parent_chain_order_title_to_immediate_parent() -> None:
    chunks = split_into_chunks(SMALL_DOC, source_path="pd1096.md")
    section_chunks = [c for c in chunks if "SECTION 102" in c.heading]
    assert section_chunks
    titles = section_chunks[0].parent_titles
    assert len(titles) == 2
    assert "NATIONAL BUILDING CODE" in titles[0]
    assert "CHAPTER 1" in titles[1]


def test_preserves_source_section_id_from_frontmatter() -> None:
    md_with_fm = textwrap.dedent("""\
        ---
        id: law-pd-1096
        title: PD 1096
        ---

        # Title

        Body.
    """)
    chunks = split_into_chunks(md_with_fm, source_path="pd1096.md")
    assert chunks
    assert all(c.source_section_id == "law-pd-1096" for c in chunks)


def test_frontmatter_absent_yields_empty_section_id() -> None:
    md = "# Title\n\nBody.\n"
    chunks = split_into_chunks(md, source_path="x.md")
    assert chunks
    assert all(c.source_section_id == "" for c in chunks)


def test_oversize_section_splits_at_paragraph() -> None:
    long_paragraph = ("word " * 300).strip()
    md = (
        "# Title\n\n## Chapter\n\n### Section\n\n"
        f"{long_paragraph}\n\n{long_paragraph}\n\n{long_paragraph}\n"
    )
    chunks = split_into_chunks(md, source_path="big.md", max_tokens=400)
    section_chunks = [c for c in chunks if "Section" in c.heading]
    assert len(section_chunks) >= 2
    for c in section_chunks:
        assert c.token_count <= 400


def test_never_splits_mid_paragraph() -> None:
    para = "the " * 100
    md = f"# T\n\n## C\n\n### S\n\n{para.strip()}\n\n{para.strip()}\n\n{para.strip()}\n"
    chunks = split_into_chunks(md, source_path="p.md", max_tokens=150)
    for c in chunks:
        if c.body.strip():
            assert c.body.strip().split()[-1] == "the"


def test_idempotent_on_reruns() -> None:
    chunks1 = split_into_chunks(SMALL_DOC, source_path="x.md")
    chunks2 = split_into_chunks(SMALL_DOC, source_path="x.md")
    assert len(chunks1) == len(chunks2)
    for a, b in zip(chunks1, chunks2):
        assert a == b


def test_determinism_of_chunk_ids() -> None:
    chunks = split_into_chunks(SMALL_DOC, source_path="pd1096.md")
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids)), "chunk IDs must be unique"
    for i, chunk_id in enumerate(ids):
        assert chunk_id.endswith(f"::{i:04d}")


def test_chunk_id_uses_source_slug() -> None:
    chunks = split_into_chunks(SMALL_DOC, source_path="pd1096.md")
    assert chunks
    for chunk in chunks:
        assert chunk.chunk_id.startswith("pd1096::")


def test_chunk_id_slug_handles_path_separators() -> None:
    chunks = split_into_chunks(SMALL_DOC, source_path="docs/laws/pd1096.md")
    assert chunks
    for chunk in chunks:
        assert "/" not in chunk.chunk_id.split("::")[0]
        assert chunk.chunk_id.split("::")[0] == "pd1096"


def test_empty_markdown_returns_empty_list() -> None:
    assert split_into_chunks("", source_path="empty.md") == []


def test_markdown_with_only_frontmatter_returns_empty_list() -> None:
    md = "---\nid: x\n---\n"
    assert split_into_chunks(md, source_path="fm.md") == []


def test_body_preserves_original_newlines() -> None:
    md = "# T\n\nFirst paragraph.\n\nSecond paragraph.\n"
    chunks = split_into_chunks(md, source_path="x.md")
    title_chunk = next(c for c in chunks if c.heading == "T")
    assert "First paragraph." in title_chunk.body
    assert "Second paragraph." in title_chunk.body


def test_token_count_matches_body_split() -> None:
    chunks = split_into_chunks(SMALL_DOC, source_path="x.md")
    for c in chunks:
        assert c.token_count == len(c.body.split())


def test_default_max_tokens_constant_is_512() -> None:
    assert DEFAULT_MAX_TOKENS == 512


def test_chunk_is_frozen_dataclass() -> None:
    chunks = split_into_chunks("# Title\n\nBody.\n", source_path="x.md")
    assert chunks
    try:
        chunks[0].heading = "mutated"  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("Chunk should be frozen (immutable)")


def test_roundtrip_reconstructed_markdown_yields_same_chunks() -> None:
    original = split_into_chunks(SMALL_DOC, source_path="x.md")
    reconstructed_parts: list[str] = []
    for chunk in original:
        if chunk.heading:
            hashes = "#" * (len(chunk.parent_titles) + 1)
            reconstructed_parts.append(f"{hashes} {chunk.heading}")
        if chunk.body:
            reconstructed_parts.append(chunk.body)
    reconstructed = "\n\n".join(p for p in reconstructed_parts if p.strip())
    rechunked = split_into_chunks(reconstructed + "\n", source_path="x.md")
    assert len(rechunked) == len(original)
    for a, b in zip(original, rechunked):
        assert a.heading == b.heading
        assert a.parent_titles == b.parent_titles


def test_section_heading_with_no_body_is_handled() -> None:
    md = "# Title\n\n## Empty Section\n\n## Section With Body\n\nHere.\n"
    chunks = split_into_chunks(md, source_path="x.md")
    headings = [c.heading for c in chunks]
    assert "Section With Body" in headings


def test_mixed_heading_depths_build_correct_chain() -> None:
    md = textwrap.dedent("""\
        # Book

        Preamble.

        ## Chapter A

        Alpha chapter.

        ### Section A.1

        First section body.

        ## Chapter B

        Beta chapter.

        ### Section B.1

        B one body.

        #### Subsection B.1.a

        Deep body.
    """)
    chunks = split_into_chunks(md, source_path="m.md")
    subs = [c for c in chunks if c.heading == "Subsection B.1.a"]
    assert subs
    chain = subs[0].parent_titles
    assert chain[0] == "Book"
    assert chain[1] == "Chapter B"
    assert chain[2] == "Section B.1"
    assert "Chapter A" not in chain


def test_chapter_b_does_not_inherit_chapter_a_context() -> None:
    md = textwrap.dedent("""\
        # Book

        ## Chapter A

        Alpha.

        ### Section A.1

        A1 body.

        ## Chapter B

        Beta chapter body.
    """)
    chunks = split_into_chunks(md, source_path="m.md")
    chap_b = [c for c in chunks if c.heading == "Chapter B"]
    assert chap_b
    assert chap_b[0].parent_titles == ("Book",)


def test_source_path_stored_on_chunks() -> None:
    chunks = split_into_chunks(SMALL_DOC, source_path="docs/laws/pd1096.md")
    assert chunks
    assert all(c.source_path == "docs/laws/pd1096.md" for c in chunks)
