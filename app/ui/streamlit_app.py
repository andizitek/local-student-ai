import json
from pathlib import Path
from urllib.parse import quote

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
USER_ID = "default_user"

st.set_page_config(page_title="Lokale Kurs-KI", layout="wide")
st.title("Lokale Kurs-KI")


def load_courses():
    try:
        response = requests.get(f"{API_URL}/courses", timeout=30)
        response.raise_for_status()
        return response.json()["courses"]
    except Exception as exc:
        st.error(f"Kurse konnten nicht geladen werden: {exc}")
        return []


def load_local_json(path: str, default):
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def load_profile():
    return load_local_json(
        f"student_data/{USER_ID}/profile.json",
        {
            "user_id": USER_ID,
            "language": "de",
            "preferred_style": "klar, strukturiert, fachlich",
            "level": "unbekannt",
            "preferred_term_mode": "de_with_en_in_brackets",
            "learning_goals": [],
        },
    )


def load_progress():
    return load_local_json(
        f"student_data/{USER_ID}/progress.json",
        {
            "seen_topics": [],
            "difficult_topics": [],
            "open_questions": [],
            "last_session_summary": "",
        },
    )


def reset_progress():
    progress_path = Path(f"student_data/{USER_ID}/progress.json")
    default_progress = {
        "seen_topics": [],
        "difficult_topics": [],
        "open_questions": [],
        "last_session_summary": "",
    }
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    progress_path.write_text(
        json.dumps(default_progress, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def reset_profile():
    profile_path = Path(f"student_data/{USER_ID}/profile.json")
    default_profile = {
        "user_id": USER_ID,
        "language": "de",
        "preferred_style": "klar, strukturiert, fachlich",
        "level": "unbekannt",
        "preferred_term_mode": "de_with_en_in_brackets",
        "learning_goals": [],
    }
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(
        json.dumps(default_profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def delete_history():
    history_path = Path(f"student_data/{USER_ID}/history.jsonl")
    if history_path.exists():
        history_path.unlink()


def build_pdf_http_url(course_id: str, source_pdf: str, page_start: int = -1) -> str:
    # source_pdf ist z. B. "source_pdfs/datei mit leerzeichen.pdf"
    parts = [quote(part) for part in Path(source_pdf).parts]
    rel_path = "/".join(parts)
    base_url = f"{API_URL}/course_files/{quote(course_id)}/{rel_path}"
    if page_start != -1:
        return f"{base_url}#page={page_start}"
    return base_url


courses = load_courses()
if not courses:
    st.stop()

profile = load_profile()
progress = load_progress()

with st.sidebar:
    st.header("Lernprofil")

    st.write(f"**Sprache:** {profile.get('language', 'de')}")
    st.write(f"**Stil:** {profile.get('preferred_style', '-')}")
    st.write(f"**Niveau:** {profile.get('level', '-')}")

    goals = profile.get("learning_goals", [])
    st.subheader("Lernziele")
    if goals:
        for goal in goals:
            st.markdown(f"- {goal}")
    else:
        st.caption("Noch keine Lernziele eingetragen.")

    seen_topics = progress.get("seen_topics", [])
    st.subheader("Bearbeitete Themen")
    if seen_topics:
        for topic in seen_topics:
            st.markdown(f"- {topic}")
    else:
        st.caption("Noch keine Themen gespeichert.")

    difficult_topics = progress.get("difficult_topics", [])
    st.subheader("Schwierige Themen")
    if difficult_topics:
        for topic in difficult_topics:
            st.markdown(f"- {topic}")
    else:
        st.caption("Noch keine schwierigen Themen gespeichert.")

    open_questions = progress.get("open_questions", [])
    st.subheader("Offene Fragen")
    if open_questions:
        for item in open_questions:
            st.markdown(f"- {item}")
    else:
        st.caption("Noch keine offenen Fragen gespeichert.")

    last_summary = progress.get("last_session_summary", "")
    st.subheader("Letzte Sitzung")
    if last_summary:
        st.write(last_summary)
    else:
        st.caption("Noch keine Sitzung gespeichert.")

    st.markdown("---")
    st.subheader("Verlauf verwalten")

    if st.button("Lernverlauf löschen", use_container_width=True):
        delete_history()
        st.success("history.jsonl wurde gelöscht.")

    if st.button("Fortschritt zurücksetzen", use_container_width=True):
        reset_progress()
        st.success("progress.json wurde zurückgesetzt.")

    if st.button("Alles zurücksetzen", use_container_width=True):
        delete_history()
        reset_progress()
        reset_profile()
        st.success("Profil, Fortschritt und Verlauf wurden zurückgesetzt.")

course_map = {f"{c['course_name']} ({c['course_id']})": c["course_id"] for c in courses}
selected_label = st.selectbox("Kurs wählen", list(course_map.keys()))
course_id = course_map[selected_label]

mode = st.selectbox(
    "Modus",
    [
        "explain",
        "summarize",
        "quiz",
        "flashcards",
        "study_guide",
        "group_prep",
        "discussion",
        "peer_review",
        "group_summary",
	"critical_ai_literacy",
        "collaborative_work"
    ],
    index=0,
)

question = st.text_area(
    "Frage an die Kurs-KI",
    height=140,
    placeholder="Stelle hier deine Frage zu den Kursmaterialien ...",
)

peer_text = ""
if mode == "peer_review":
    peer_text = st.text_area(
        "Text für Peer-Review",
        height=200,
        placeholder="Füge hier einen studentischen Text oder Entwurf ein ...",
    )

if st.button("Antwort erzeugen", use_container_width=True):
    if not question.strip():
        st.warning("Bitte zuerst eine Frage eingeben.")
        st.stop()

    payload = {
        "course_id": course_id,
        "question": question,
        "mode": mode,
        "user_id": USER_ID,
    }

    if mode == "peer_review":
        payload["peer_text"] = peer_text

    with st.spinner("Antwort wird erzeugt ..."):
        response = requests.post(
            f"{API_URL}/chat",
            json=payload,
            timeout=900,
        )
        response.raise_for_status()
        data = response.json()

    st.session_state["last_answer"] = data
    st.session_state["last_question"] = question
    st.session_state["last_mode"] = mode
    st.session_state["last_course_id"] = course_id

if "last_answer" in st.session_state:
    data = st.session_state["last_answer"]

    st.subheader("Antwort")
    st.write(data["answer"])

    st.subheader("Verwendete Quellen")
    if not data["sources"]:
        st.info("Es wurden keine Quellen aus dem lokalen Index gefunden.")
    else:
        for src in data["sources"]:
            title = f"{src['document']} · {src['chunk_id']}"
            with st.expander(title):
                source_pdf = (src.get("source_pdf") or "").strip()
                page_start = src.get("page_start", -1)
                page_end = src.get("page_end", -1)
                src_course_id = src.get("course_id", st.session_state.get("last_course_id", course_id))

                if source_pdf:
                    pdf_url = build_pdf_http_url(src_course_id, source_pdf, page_start)

                    st.markdown(f"**Originalquelle:** `{source_pdf}`")

                    if page_start != -1:
                        if page_end != -1 and page_end != page_start:
                            st.markdown(f"**Seiten:** {page_start}-{page_end}")
                        else:
                            st.markdown(f"**Seite:** {page_start}")

                    st.markdown(f"[PDF öffnen]({pdf_url})")
                else:
                    st.caption("Keine Original-PDF hinterlegt.")

                st.write(src["snippet"])
                st.caption(f"Distanzwert: {src['distance']}")

    col1, col2 = st.columns(2)

    with col1:
        export_md = requests.post(
            f"{API_URL}/export_markdown",
            json={
                "course_id": st.session_state["last_course_id"],
                "question": st.session_state["last_question"],
                "answer": data["answer"],
                "sources": data["sources"],
                "mode": st.session_state["last_mode"],
            },
            timeout=60,
        ).text

        st.download_button(
            "Als Markdown exportieren",
            data=export_md,
            file_name=f"{st.session_state['last_course_id']}_{st.session_state['last_mode']}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "Als JSON exportieren",
            data=json.dumps(data, ensure_ascii=False, indent=2),
            file_name=f"{st.session_state['last_course_id']}_{st.session_state['last_mode']}.json",
            mime="application/json",
            use_container_width=True,
        )

st.markdown("---")
st.markdown("### Hinweise für Gruppenarbeit")
st.markdown(
    """
- **group_prep** für Gruppenbeiträge vorbereiten
- **discussion** für Diskussionsfragen und Perspektiven
- **peer_review** für Rückmeldung zu Textentwürfen
- **group_summary** für einen kompakten Beitrag der Gruppe
"""
)