
from pathlib import Path

import fitz  # PyMuPDF
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def load_document(file_path: str | Path) -> list[dict]:
    """Extract text and metadata from a PDF, DOCX, or TXT file."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    pages = []

    if path.suffix.lower() == ".pdf":
        with fitz.open(path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                if text:
                    pages.append({
                        "text": text,
                        "metadata": {
                            "source": path.name,
                            "page": page_number,
                        },
                    })

        if not pages:
            raise ValueError(
                "No extractable text found. This may be a scanned PDF; "
                "OCR support is not implemented yet."
            )

    elif path.suffix.lower() == ".docx":
        doc = Document(path)
        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
            if paragraph.text.strip()
        ).strip()

        if text:
            pages.append({
                "text": text,
                "metadata": {"source": path.name, "page": 1},
            })

    else:
        text = path.read_text(encoding="utf-8-sig").strip()

        if text:
            pages.append({
                "text": text,
                "metadata": {"source": path.name, "page": 1},
            })

    if not pages:
        raise ValueError("The document contains no extractable text.")

    return pages
