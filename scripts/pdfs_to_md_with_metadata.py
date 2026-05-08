from pathlib import Path
import csv
import re
import unicodedata
import argparse
from pypdf import PdfReader


COURSE_ID = "demo_kurs"

BASE_DIR = Path("courses") / COURSE_ID
INPUT_DIR = BASE_DIR / "source_pdfs"
OUTPUT_DIR = BASE_DIR / "materials"
METADATA_CSV = BASE_DIR / "metadata.csv"


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)

    text = text.replace("\x00", " ")
    text = text.replace("\ufeff", " ")
    text = text.replace("\xa0", " ")
    text = text.replace("\u00ad", "")

    text = text.replace("„", '"').replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("–", "-").replace("—", "-")

    # Zeilentrennungs-Silbentrennungen glätten
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)

    # Mehrfach-Whitespace reduzieren
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def load_metadata(csv_path: Path) -> dict[str, dict]:
    rows = {}

    if not csv_path.exists():
        print(f"Keine metadata.csv gefunden: {csv_path}")
        return rows

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = (row.get("filename") or "").strip()
            if filename:
                rows[filename] = row

    return rows


def build_markdown(pdf_path: Path, meta: dict) -> str:
    reader = PdfReader(str(pdf_path))
    page_blocks = []

    for i, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        cleaned = clean_text(raw)

        if not cleaned:
            continue

        page_blocks.append(
            f"<!-- PAGE:{i} -->\n\n### Seite {i}\n\n{cleaned}"
        )

    title = (meta.get("title") or "").strip() or pdf_path.stem
    author = (meta.get("author") or "").strip() or "-"
    year = (meta.get("year") or "").strip() or "-"
    doi = (meta.get("doi") or "").strip() or "-"
    url = (meta.get("url") or "").strip() or "-"
    source_type = (meta.get("source_type") or "").strip() or "PDF"

    original_source = f"source_pdfs/{pdf_path.name}"

    header = f"""# {title}

## Metadaten
- Originalquelle: `{original_source}`
- Quelle-Typ: {source_type}
- Autor: {author}
- Jahr: {year}
- DOI: {doi}
- URL: {url}

## Inhalt
"""

    body = "\n\n".join(page_blocks).strip()

    if not body:
        body = "_Kein extrahierbarer Text gefunden._"

    return header + "\n\n" + body + "\n"


def main(force: bool = False):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    metadata = load_metadata(METADATA_CSV)
    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"Keine PDFs gefunden in: {INPUT_DIR}")
        return

    print(f"Gefundene PDFs: {len(pdf_files)}")

    created = 0
    skipped_existing = 0
    failed = 0

    for pdf_file in pdf_files:
        md_file = OUTPUT_DIR / f"{pdf_file.stem}.md"

        if md_file.exists() and not force:
            print(f"Übersprungen (existiert schon): {md_file.name}")
            skipped_existing += 1
            continue

        meta = metadata.get(pdf_file.name, {})

        try:
            markdown = build_markdown(pdf_file, meta)
            md_file.write_text(markdown, encoding="utf-8")
            print(f"OK: {pdf_file.name} -> {md_file.name}")
            created += 1
        except Exception as e:
            print(f"FEHLER bei {pdf_file.name}: {e}")
            failed += 1

    print("\nFertig.")
    print(f"Neu erzeugt: {created}")
    print(f"Übersprungen (bereits vorhanden): {skipped_existing}")
    print(f"Fehler: {failed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="Vorhandene .md-Dateien überschreiben",
    )
    args = parser.parse_args()
    main(force=args.force)