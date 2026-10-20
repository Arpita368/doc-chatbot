
from app.ingestion.loader import load_document


def test_load_txt(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello document chatbot!", encoding="utf-8")

    pages = load_document(file_path)

    assert len(pages) == 1
    assert pages[0]["text"] == "Hello document chatbot!"
    assert pages[0]["metadata"]["source"] == "sample.txt"


def test_missing_file():
    import pytest

    with pytest.raises(FileNotFoundError):
        load_document("missing.txt")
