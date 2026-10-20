
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    chunk_size: int = 800
    chunk_overlap: int = 150
    top_k: int = 4

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen2.5:3b"

    upload_dir: Path = BASE_DIR / "data" / "uploads"
    vector_db_dir: Path = BASE_DIR / "data" / "vectordb"
    collection_name: str = "document_chunks"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.vector_db_dir.mkdir(parents=True, exist_ok=True)