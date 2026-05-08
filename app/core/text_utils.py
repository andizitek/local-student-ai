from pathlib import Path
from pypdf import PdfReader

def extract_text(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return file_path.read_text(encoding="utf-8", errors="ignore")

def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 100) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    chunks = []
    start = 0
    step = max(1, chunk_size - overlap)
    while start < len(cleaned):
        end = start + chunk_size
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks
