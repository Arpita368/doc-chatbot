
from app.ingestion.chunker import chunk_documents


def test_chunker_preserves_metadata():
    pages = [{
        "text": "A" * 2000,
        "metadata": {"source": "sample.pdf", "page": 3},
    }]

    chunks = chunk_documents(pages)

    assert len(chunks) > 1
    assert all(c["metadata"]["page"] == 3 for c in chunks)
    assert all(c["metadata"]["source"] == "sample.pdf" for c in chunks)
    assert all(c["id"] for c in chunks)


def test_empty_document():
    assert chunk_documents([]) == []
