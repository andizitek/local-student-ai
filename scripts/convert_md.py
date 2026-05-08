import os
import re
from markitdown import MarkItDown

folder = os.path.dirname(os.path.abspath(__file__))
out_folder = os.path.join(folder, "_md")
os.makedirs(out_folder, exist_ok=True)

md = MarkItDown()  # kein llm_client → ohne KI

skip_ext = {".py", ".md"}
skip_dirs = {"_md"}

URL_RE = re.compile(r'https?://[^\s\]\)>"\']+')


def extract_first_url(text: str) -> str:
    """Erste URL im Markdown-Text finden."""
    match = URL_RE.search(text)
    return match.group(0) if match else ""


for filename in os.listdir(folder):
    if filename.startswith("."):
        continue
    ext = os.path.splitext(filename)[1].lower()
    if ext in skip_ext:
        continue
    src = os.path.join(folder, filename)
    if not os.path.isfile(src):
        continue
    if filename in skip_dirs:
        continue

    out_name = os.path.splitext(filename)[0] + ".md"
    dst = os.path.join(out_folder, out_name)

    try:
        result = md.convert(src)
        content = result.text_content

        first_url = extract_first_url(content)

        header = f"<!-- URL:  {first_url} -->\n\n<!-- Folder:  -->\n\n"
        with open(dst, "w", encoding="utf-8") as f:
            f.write(header + content)
        print(f"OK:    {filename}  →  _md/{out_name}  (URL: {first_url or '–'})")
    except Exception as e:
        print(f"FEHLER: {filename}  —  {e}")

print("Fertig.")
