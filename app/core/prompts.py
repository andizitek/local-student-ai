def _format_hits(hits: list[dict], label_prefix: str = "Kontext") -> str:
    if not hits:
        return "Kein passender Kontext gefunden."

    blocks = []
    for i, hit in enumerate(hits, start=1):
        doc = hit["meta"].get("document", "unbekanntes_dokument")
        page_start = hit["meta"].get("page_start", -1)
        page_info = f", Seite {page_start}" if page_start != -1 else ""
        blocks.append(f"[{label_prefix} {i} | {doc}{page_info}]\n{hit['text']}")

    return "\n\n".join(blocks)


def build_user_prompt(
    question: str,
    hits: list[dict],
    mode: str,
    learning_context: str = "",
    critical_hits: list[dict] | None = None,
) -> str:
    context = _format_hits(hits, "Fachkontext")
    critical_context = _format_hits(critical_hits or [], "Reflexionskontext")
# Sonderfall: critical_ai_literacy mit getrenntem Fach- und Reflexionskontext
    if mode == "critical_ai_literacy":
        return f"""
{learning_context}

Konkrete Nutzerfrage:
{question}

Fachkontext:
{context}

Zusätzlicher Reflexionskontext:
{critical_context}

Arbeitsauftrag:
Beantworte zuerst präzise die konkrete Nutzerfrage auf Basis des Fachkontexts.
Nutze den Reflexionskontext nur als kritischen Deutungs- und Prüfrahmen, nicht als Ersatz für die eigentliche Antwort.
Bleibe strikt beim Fokus der Frage. Wenn einzelne Kontexte nur allgemein passen, aber für die konkrete Frage nicht relevant sind, ignoriere sie.

Antworte in genau 5 Teilen:
1. Welche Aussagen zur konkreten Frage sind im Material klar belegt?
2. Welche Teile wären eher Interpretation, Verallgemeinerung oder KI-Inferenz?
3. Was bleibt in Bezug auf genau diese Frage unklar oder offen?
4. Was sollte die Gruppe zu genau dieser Frage selbst prüfen oder diskutieren?
5. Wie sollte der KI-Einsatz bei der Bearbeitung genau dieser Frage transparent gemacht werden?

Wichtige Regeln:
- Nutze für die eigentliche Antwort primär den Fachkontext.
- Nutze den Reflexionskontext nur zur kritischen Rahmung.
- Halte den Fokus streng auf der konkreten Nutzerfrage.
- Verwende keine Platzhalter wie "Quelle 1" oder "Quelle 2".
- Nenne stattdessen direkt den Dokumentnamen.
- Wenn Seiten vorhanden sind, nenne sie als (Dokumentname, S. X).
- Keine erfundenen bibliografischen Angaben.
- Keine separate Literaturliste am Ende, wenn die Quellen im Text bereits genannt sind.
""".strip()

    mode_instruction = {
        "explain": "Erkläre die Antwort didaktisch und verständlich in klaren Schritten.",
        "summarize": "Gib eine knappe strukturierte Zusammenfassung.",
        "quiz": "Erkläre kurz und stelle danach 3 Quizfragen ohne sofortige Lösung.",
        "quiz_mc": "Erstelle ein Multiple-Choice-Quiz mit genau einer richtigen Antwort pro Frage. Nutze ausschließlich den bereitgestellten Kontext. Die richtige Antwort muss inhaltlich eindeutig mit dem Material übereinstimmen. Wenn eine Frage nicht eindeutig aus dem Material ableitbar ist, stelle sie nicht. Gib genau 4 Antwortoptionen pro Frage an. Antworte ausschließlich als gültiges JSON im folgenden Format: {\"topic\": \"...\", \"questions\": [{\"question\": \"...\", \"options\": [\"...\", \"...\", \"...\", \"...\"], \"correct_index\": 1, \"source\": {\"document\": \"...\", \"source_pdf\": \"source_pdfs/...pdf\", \"page\": 25}}]}. Verwende keine zusätzliche Einleitung und keinen Fließtext außerhalb des JSON.",
        "flashcards": "Erstelle Lernkarten mit Begriff und Erklärung.",
        "study_guide": "Erstelle einen Lernleitfaden mit den wichtigsten Punkten, Reihenfolge und typischen Missverständnissen.",
        "group_prep": "Erzeuge eine Unterstützung für eine Lerngruppe: Kernaussagen, Diskussionspunkte, offene Punkte und Arbeitsaufträge.",
        "discussion": "Erzeuge Material für eine Gruppendiskussion: Ausgangserklärung, zwei Perspektiven, zwei kritische Rückfragen und einen kontroversen Punkt.",
        "group_summary": "Formuliere einen kompakten Gruppenbeitrag mit Kernaussage, Begriffen, Relevanz und offener Rückfrage.",
        "collaborative_work": "Unterstütze die Gruppe bei einem kollaborativen Arbeitsprozess. Kläre das Ziel, zerlege die Aufgabe in sinnvolle Teilaufgaben, schlage mögliche Rollen und Zuständigkeiten vor, benenne Abhängigkeiten zwischen Teilaufgaben und erkläre, wie Zwischenergebnisse zusammengeführt und gemeinsam geprüft werden können. Wenn die Aufgabe mit Programmierung zu tun hat, gehe zusätzlich auf Module, Schnittstellen, Integration, Tests und gemeinsame Qualitätsprüfung ein. Gib nicht vorschnell nur fertige Ergebnisse aus, sondern unterstütze vor allem Strukturierung, Koordination und Reflexion.",
    }.get(mode, "Erkläre die Antwort didaktisch und verständlich in klaren Schritten.")

    return f"""
{learning_context}

Aufgabe:
{question}

Arbeitsmodus:
{mode_instruction}

Verfügbarer Kontext:
{context}

Wichtige Regeln:
- Nutze nur den bereitgestellten Kontext.
- Wenn etwas im Material nicht klar belegt ist, sage das offen.
- Verwende im Fließtext keine Platzhalter wie "Quelle 1" oder "Quelle 2".
- Nenne stattdessen direkt den Dokumentnamen, wenn du auf Kontext Bezug nimmst.
- Wenn Seiten vorhanden sind, nenne sie als (Dokumentname, S. X).
- Keine erfundenen bibliografischen Angaben.
- Keine separate Literaturliste am Ende, wenn die Quellen im Text bereits genannt sind.
- Beginne neue Nummerierungen immer wieder bei 1.
""".strip()


def build_peer_review_prompt(
    question: str,
    peer_text: str,
    hits: list[dict],
    learning_context: str = "",
) -> str:
    context = _format_hits(hits, "Kontext")

    return f"""
{learning_context}

Aufgabe:
{question}

Zu begutachtender Text:
{peer_text}

Verfügbarer Kontext:
{context}

Bitte gib konstruktives Peer-Feedback:
1. Was ist gelungen?
2. Was ist unklar oder ausbaufähig?
3. Wo fehlt Materialbezug?
4. Welche Verbesserungsvorschläge ergeben sich?

Wichtige Regeln:
- Nutze nur den bereitgestellten Kontext.
- Keine erfundenen Quellen.
- Nenne Dokumentnamen direkt statt "Quelle 1" usw.
""".strip()
