from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime
from typing import Any

BASE_DIR = Path("student_data")
COURSES_DIR = Path("courses")
DEFAULT_USER_ID = "default_user"
DEFAULT_COURSE_ID = "demo_kurs"


def _user_dir(user_id: str = DEFAULT_USER_ID) -> Path:
    path = BASE_DIR / user_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def _read_json(path: Path, default: dict | list) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, data: Any) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_profile(user_id: str = DEFAULT_USER_ID) -> dict:
    path = _user_dir(user_id) / "profile.json"
    default = {
        "user_id": user_id,
        "language": "de",
        "preferred_style": "klar, strukturiert, fachlich",
        "level": "unbekannt",
        "preferred_term_mode": "de_with_en_in_brackets",
        "learning_goals": [],
    }
    if not path.exists():
        _write_json(path, default)
    return _read_json(path, default)


def load_progress(user_id: str = DEFAULT_USER_ID) -> dict:
    path = _user_dir(user_id) / "progress.json"
    default = {
        "seen_topics": [],
        "difficult_topics": [],
        "open_questions": [],
        "last_session_summary": "",
        "last_question": "",
    }
    if not path.exists():
        _write_json(path, default)
    return _read_json(path, default)


def append_history(
    course_id: str,
    mode: str,
    question: str,
    answer: str,
    topics: list[str] | None = None,
    user_id: str = DEFAULT_USER_ID,
) -> None:
    path = _user_dir(user_id) / "history.jsonl"
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "course_id": course_id,
        "mode": mode,
        "question": question,
        "answer_preview": answer[:300],
        "topics": topics or [],
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_topic_map(course_id: str = DEFAULT_COURSE_ID) -> dict[str, list[str]]:
    path = COURSES_DIR / course_id / "topic_map.json"
    default = {
        "Schauspiel": ["schauspiel", "rolle", "theater"],
        "Körperarbeit": ["körperarbeit", "körper", "leib", "bewegung", "haltung", "gestik"],
        "Stanislawski": ["stanislawski"],
        "Action Theater": ["action theater", "zaporah"],
        "Tschechow": ["tschechow", "tschechov", "chekhov"],
        "Improvisation": ["improvisation", "improvisieren"],
        "Traumarbeit": ["traum", "träume", "traumarbeit"],
        "Jung": ["jung", "ich-selbst-achse", "selbst"],
        "Paperanalyse": ["paper", "studie", "artikel", "methode", "ergebnis"],
    }

    if not path.exists():
        return default

    data = _read_json(path, default)
    if isinstance(data, dict):
        return data

    return default


def detect_topics(text: str, course_id: str = DEFAULT_COURSE_ID) -> list[str]:
    topic_map = load_topic_map(course_id)
    found = []
    lowered = text.lower()

    for label, keywords in topic_map.items():
        if not isinstance(keywords, list):
            continue
        if any(str(keyword).lower() in lowered for keyword in keywords):
            found.append(label)

    return found


def detect_difficult_topics(text: str, topics: list[str]) -> list[str]:
    lowered = text.lower()

    difficulty_markers = [
        "ich verstehe nicht",
        "unklar",
        "nicht eindeutig",
        "schwierig",
        "unsicher",
        "verwirrt",
        "was genau",
        "nicht klar",
        "mehrdeutig",
    ]

    if not any(marker in lowered for marker in difficulty_markers):
        return []

    if topics:
        return topics

    return ["noch nicht genauer bestimmtes schwieriges Thema"]


def answer_indicates_open_question(answer: str) -> bool:
    lowered = answer.lower()

    markers = [
        "nicht eindeutig",
        "nicht klar",
        "keine direkte liste",
        "im material nicht direkt",
        "nicht direkt beantwortet",
        "nicht sicher ableitbar",
        "aus dem material nicht eindeutig",
        "unsicherheit",
    ]

    return any(marker in lowered for marker in markers)


def update_progress_from_question(
    question: str,
    answer: str,
    user_id: str = DEFAULT_USER_ID,
    course_id: str = DEFAULT_COURSE_ID,
) -> None:
    progress = load_progress(user_id)

    combined = f"{question}\n{answer}"
    topics = detect_topics(combined, course_id=course_id)

    for topic in topics:
        if topic not in progress["seen_topics"]:
            progress["seen_topics"].append(topic)

    difficult_topics = detect_difficult_topics(combined, topics)
    for topic in difficult_topics:
        if topic not in progress["difficult_topics"]:
            progress["difficult_topics"].append(topic)

    if answer_indicates_open_question(answer):
        if question not in progress["open_questions"]:
            if len(progress["open_questions"]) < 10:
                progress["open_questions"].append(question)

    progress["last_question"] = question
    progress["last_session_summary"] = answer

    _write_json(_user_dir(user_id) / "progress.json", progress)


def build_learning_context(
    user_id: str = DEFAULT_USER_ID,
    course_id: str = DEFAULT_COURSE_ID,
) -> str:
    profile = load_profile(user_id)
    progress = load_progress(user_id)

    parts = []
    parts.append("Lernkontext der Person:")

    language = profile.get("language", "de")
    style = profile.get("preferred_style", "klar")
    level = profile.get("level", "unbekannt")
    parts.append(f"- Sprache: {language}")
    parts.append(f"- Bevorzugter Stil: {style}")
    parts.append(f"- Niveau: {level}")

    goals = profile.get("learning_goals", [])
    if goals:
        parts.append("- Lernziele: " + "; ".join(goals[:5]))

    seen_topics = progress.get("seen_topics", [])
    if seen_topics:
        parts.append("- Bereits bearbeitete Themen: " + "; ".join(seen_topics[:8]))

    difficult_topics = progress.get("difficult_topics", [])
    if difficult_topics:
        parts.append("- Schwierige Themen: " + "; ".join(difficult_topics[:8]))

    open_questions = progress.get("open_questions", [])
    if open_questions:
        parts.append("- Offene Fragen: " + "; ".join(open_questions[:5]))

    summary = progress.get("last_session_summary", "")
    if summary:
        parts.append("- Letzte Sitzung vorhanden.")

    parts.append(
        "- Bitte antworte anschlussfähig an diesen Lernkontext, ohne unnötige Wiederholungen."
    )

    return "\n".join(parts)