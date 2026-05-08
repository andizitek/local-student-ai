def render_markdown_export(course_id: str, question: str, answer: str, sources: list[dict], mode: str) -> str:
    lines = ["# Gruppenbeitrag / Export", "", f"- Kurs: `{course_id}`", f"- Modus: `{mode}`", "", "## Ausgangsfrage", "", question.strip(), "", "## Antwort", "", answer.strip(), "", "## Quellen", ""]
    if not sources:
        lines.append("- Keine lokalen Quellen gefunden")
    else:
        for src in sources:
            lines.append(f"- **{src.get('document','unbekannt')}** · `{src.get('chunk_id','ohne-id')}`")
    lines.append("")
    return "\n".join(lines)
