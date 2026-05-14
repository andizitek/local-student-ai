from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
from typing import Any
import uuid

DEFAULT_USER_ID = "default_user"
STUDENT_DATA_DIR = Path("student_data")


def _user_dir(user_id: str) -> Path:
    path = STUDENT_DATA_DIR / user_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_quiz_results(user_id: str = DEFAULT_USER_ID) -> list[dict]:
    path = _user_dir(user_id) / "quiz_results.json"
    return _read_json(path, [])


def make_quiz_session_id(course_id: str, topic: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    return f"{timestamp}_{course_id}_{topic}_{uuid.uuid4().hex[:6]}"


def append_quiz_result(
    quiz_session_id: str,
    course_id: str,
    topic: str,
    question: str,
    options: list[str],
    correct_index: int,
    selected_index: int,
    is_correct: bool,
    mode: str = "quiz_mc",
    user_id: str = DEFAULT_USER_ID,
) -> None:
    results = load_quiz_results(user_id)
    results.append(
        {
            "quiz_session_id": quiz_session_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "course_id": course_id,
            "topic": topic,
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "selected_index": selected_index,
            "is_correct": is_correct,
            "mode": mode,
        }
    )
    _write_json(_user_dir(user_id) / "quiz_results.json", results)


def compute_quiz_analytics(user_id: str = DEFAULT_USER_ID) -> dict:
    results = load_quiz_results(user_id)

    total = len(results)
    correct = sum(1 for r in results if r.get("is_correct") is True)
    incorrect = total - correct
    accuracy = (correct / total) if total else 0.0

    topic_stats: dict[str, dict[str, int]] = {}
    sessions: dict[str, dict] = {}

    for r in results:
        topic = r.get("topic", "Unbekannt")
        if topic not in topic_stats:
            topic_stats[topic] = {"total": 0, "correct": 0, "incorrect": 0}
        topic_stats[topic]["total"] += 1
        if r.get("is_correct") is True:
            topic_stats[topic]["correct"] += 1
        else:
            topic_stats[topic]["incorrect"] += 1

        session_id = r.get("quiz_session_id", "unknown_session")
        if session_id not in sessions:
            sessions[session_id] = {
                "topic": topic,
                "timestamp": r.get("timestamp", ""),
                "total": 0,
                "correct": 0,
                "incorrect": 0,
                "wrong_questions": [],
            }

        sessions[session_id]["total"] += 1
        if r.get("is_correct") is True:
            sessions[session_id]["correct"] += 1
        else:
            sessions[session_id]["incorrect"] += 1
            sessions[session_id]["wrong_questions"].append(
                {
                    "question": r.get("question", ""),
                    "selected_index": r.get("selected_index"),
                    "correct_index": r.get("correct_index"),
                    "options": r.get("options", []),
                }
            )

    difficult_topics = [
        topic for topic, stats in topic_stats.items()
        if stats["incorrect"] > stats["correct"]
    ]

    return {
        "total_quiz_items": total,
        "correct_count": correct,
        "incorrect_count": incorrect,
        "accuracy": round(accuracy, 2),
        "topic_stats": topic_stats,
        "difficult_topics_from_quiz": difficult_topics,
        "sessions": sessions,
    }