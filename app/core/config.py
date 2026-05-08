from pathlib import Path
import yaml

COURSES_DIR = Path("courses")

def load_course_config(course_id: str) -> dict:
    path = COURSES_DIR / course_id / "config.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Konfiguration für Kurs '{course_id}' nicht gefunden.")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def list_courses() -> list[dict]:
    courses = []
    if not COURSES_DIR.exists():
        return courses
    for course_dir in COURSES_DIR.iterdir():
        if not course_dir.is_dir():
            continue
        cfg_file = course_dir / "config.yaml"
        if not cfg_file.exists():
            continue
        cfg = yaml.safe_load(cfg_file.read_text(encoding="utf-8"))
        courses.append({
            "course_id": cfg.get("course_id", course_dir.name),
            "course_name": cfg.get("course_name", course_dir.name),
            "language": cfg.get("language", "de"),
        })
    return sorted(courses, key=lambda x: x["course_name"].lower())
