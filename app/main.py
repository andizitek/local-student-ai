from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router
from app.api.health import router as health_router

app = FastAPI(title="Student Course AI")

app.include_router(chat_router)
app.include_router(health_router)

# Macht den gesamten courses-Ordner per HTTP zugänglich
# Beispiel:
# http://127.0.0.1:8000/course_files/demo_course/source_pdfs/datei.pdf
app.mount("/course_files", StaticFiles(directory="courses"), name="course_files")
