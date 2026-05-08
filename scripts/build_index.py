import argparse
import json
import re
from pathlib import Path

import chromadb
import yaml

from app.core.llm import embed_text
from app.core.text_utils import extract_text

SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}


def should_skip_chunk(chunk: str) -> tuple[bool, str]:
    chunk = chunk.strip()

    if not chunk:
        return True, "leer"

    if len(chunk) < 40:
        return True, "zu kurz"

    dot_count = chunk.count(".")
    digit_count = sum(c.isdigit() for c in chunk)

    if dot_count > 80:
        return True, "zu viele punkte"

    if digit_count > len(chunk) * 0.20:
        return True, "zu viele ziffern"

    weird_count = sum(
        not (ch.isalnum() or ch.isspace() or ch in '.,;:!?()[]{}"\'-_/`')
        for ch in chunk
    )
    if weird_count > len(chunk) * 0.03:
        return True, "zu viele sonderzeichen"

    lowered = chunk.lower()

    toc_markers = [
        "inhaltsverzeichnis",
        "methodik . . .",
        "praxis . . .",
    ]
    if any(marker in lowered for marker in toc_markers) and dot_count > 20:
        return True, "vermutlich inhaltsverzeichnis/layout"

    if "zitiert nach:" in lowered:
        return True, "literaturfragment"

    if " hg." in lowered and " in:" in lowered:
        return True, "literaturverweis"

    return False, ""


def clean_chunk(chunk: str) -> str:
    chunk = chunk.replace("\x00", " ")
    chunk = " ".join(chunk.split())
    return chunk.strip()


def extract_source_pdf_from_text(text: str) -> str:
    head = text[:4000]

    patterns = [
        r"Originalquelle:\s*`([^`]+)`",
        r"\*\*Originalquelle:\*\*\s*`([^`]+)`",
        r"Originalquelle:\s*([^\n\r]+\.pdf)",
    ]

    for pattern in patterns:
        match = re.search(pattern, head, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return ""


def chunk_plain_text_with_meta(text: str, chunk_size: int, overlap: int) -> list[dict]:
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
            chunks.append(
                {
                    "text": chunk,
                    "page_start": -1,
                    "page_end": -1,
                }
            )
        start += step

    return chunks


def chunk_markdown_with_pages(text: str, chunk_size: int, overlap: int) -> list[dict]:
    parts = re.split(r"(<!-- PAGE:\d+ -->)", text)
    page_sections = []

    current_page = None

    for part in parts:
        part = part or ""
        marker_match = re.match(r"<!-- PAGE:(\d+) -->", part.strip())
        if marker_match:
            current_page = int(marker_match.group(1))
            continue

        if current_page is not None and part.strip():
            page_sections.append(
                {
                    "page": current_page,
                    "text": part.strip(),
                }
            )

    if not page_sections:
        return chunk_plain_text_with_meta(text, chunk_size, overlap)

    chunks = []
    current_text = ""
    current_start_page = None
    current_end_page = None

    for section in page_sections:
        page = section["page"]
        section_text = clean_chunk(section["text"])

        if not section_text:
            continue

        if current_start_page is None:
            current_start_page = page
            current_end_page = page
            current_text = section_text
            continue

        candidate = f"{current_text}\n\n{section_text}"

        if len(candidate) <= chunk_size:
            current_text = candidate
            current_end_page = page
        else:
            chunks.append(
                {
                    "text": current_text.strip(),
                    "page_start": current_start_page if current_start_page is not None else -1,
                    "page_end": current_end_page if current_end_page is not None else -1,
                }
            )

            overlap_text = current_text[-overlap:] if overlap > 0 else ""
            current_text = (overlap_text + "\n\n" + section_text).strip()
            current_start_page = page
            current_end_page = page

    if current_text.strip():
        chunks.append(
            {
                "text": current_text.strip(),
                "page_start": current_start_page if current_start_page is not None else -1,
                "page_end": current_end_page if current_end_page is not None else -1,
            }
        )

    return chunks


def iter_content_files(base: Path):
    folders = [
        ("materials", "material"),
        ("critical", "critical"),
    ]

    for folder_name, content_type in folders:
        folder = base / folder_name
        if not folder.exists():
            continue

        for file_path in sorted(folder.glob("*")):
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield file_path, content_type


def build_index(course_id: str):
    base = Path("courses") / course_id
    cfg_file = base / "config.yaml"
    if not cfg_file.exists():
        raise FileNotFoundError(f"Keine Konfiguration gefunden: {cfg_file}")

    cfg = yaml.safe_load(cfg_file.read_text(encoding="utf-8"))
    processed_dir = base / "processed"
    db_dir = base / "chroma_db"

    processed_dir.mkdir(parents=True, exist_ok=True)
    db_dir.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_or_create_collection(name="course_materials")

    count = collection.count()
    if count > 0:
        existing = collection.get(include=[])
        ids = existing.get("ids", [])
        if ids:
            collection.delete(ids=ids)

    all_rows = []
    skipped = []

    for file_path, content_type in iter_content_files(base):
        print(f"\nVerarbeite Datei: {file_path.name} [{content_type}]")

        text = extract_text(file_path)
        source_pdf = ""

        if file_path.suffix.lower() in {".md", ".txt"}:
            source_pdf = extract_source_pdf_from_text(text)

        if file_path.suffix.lower() == ".md":
            chunks = chunk_markdown_with_pages(
                text,
                chunk_size=cfg["retrieval"]["chunk_size"],
                overlap=cfg["retrieval"]["chunk_overlap"],
            )
        else:
            chunks = chunk_plain_text_with_meta(
                text,
                chunk_size=cfg["retrieval"]["chunk_size"],
                overlap=cfg["retrieval"]["chunk_overlap"],
            )

        print(f"  Anzahl Chunks: {len(chunks)}")

        for i, item in enumerate(chunks):
            raw_chunk = item["text"]

            skip, reason = should_skip_chunk(raw_chunk)
            if skip:
                skipped.append((file_path.name, i, reason))
                continue

            chunk = clean_chunk(raw_chunk)
            chunk_id = f"{content_type}_{file_path.stem}_{i:04d}"

            try:
                embedding = embed_text(chunk, cfg["llm"]["embedding_model"])
            except Exception as e:
                print(f"  FEHLER bei Datei {file_path.name}, Chunk {i}")
                print(f"  Grund: {e}")
                print(f"  Chunk-Vorschau: {chunk[:300]!r}")
                skipped.append((file_path.name, i, str(e)))
                continue

            metadata = {
                "document": file_path.name,
                "chunk_id": chunk_id,
                "file_type": file_path.suffix.lower().lstrip("."),
                "source_pdf": source_pdf or "",
                "page_start": int(item["page_start"]) if item.get("page_start", -1) != -1 else -1,
                "page_end": int(item["page_end"]) if item.get("page_end", -1) != -1 else -1,
                "content_type": content_type,
            }

            collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[metadata],
            )

            all_rows.append(
                {
                    "id": chunk_id,
                    "document": file_path.name,
                    "text": chunk,
                    "source_pdf": source_pdf or "",
                    "page_start": metadata["page_start"],
                    "page_end": metadata["page_end"],
                    "content_type": content_type,
                }
            )

    manifest = {
        "course_id": course_id,
        "chunk_count": len(all_rows),
        "skipped_count": len(skipped),
    }

    (processed_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with open(processed_dir / "chunks.jsonl", "w", encoding="utf-8") as f:
        for row in all_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"\nFertig. {len(all_rows)} Chunks für Kurs '{course_id}' indexiert.")
    print(f"Übersprungene/problematische Chunks: {len(skipped)}")

    if skipped:
        print("\nEinige übersprungene/problematische Chunks:")
        for item in skipped[:20]:
            print(" -", item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", required=True, help="Kurs-ID, z. B. demo_kurs")
    args = parser.parse_args()
    build_index(args.course)