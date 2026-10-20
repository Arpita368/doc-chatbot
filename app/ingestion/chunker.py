
import hashlib

from app.config import settings


def chunk_documents(pages: list[dict]) -> list[dict]:
    """Split extracted page text into overlapping character chunks."""
    chunks = []
    size = settings.chunk_size
    overlap = settings.chunk_overlap

    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError(
            "chunk_size must be positive and "
            "chunk_overlap must be between 0 and chunk_size."
        )

    step = size - overlap

    for page in pages:
        text = page["text"].strip()
        metadata = page["metadata"]

        for start in range(0, len(text), step):
            chunk_text = text[start:start + size].strip()

            if not chunk_text:
                continue

            chunk_index = len(chunks)
            raw_id = (
                f"{metadata['source']}|"
                f"{metadata['page']}|{start}|{chunk_text}"
            )
            chunk_id = hashlib.sha256(
                raw_id.encode("utf-8")
            ).hexdigest()

            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    **metadata,
                    "chunk_index": chunk_index,
                    "start_char": start,
                },
            })

    return chunks
