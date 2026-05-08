# local-student-ai
Ein lokaler KI-Chatbot für kollaboratives Lernen, kritische Reflexion und Kompetenzentwicklung

**Praktische Einrichtung.**
Nach Installation von Python, Ollama und den Projektabhängigkeiten werden lokale Modelle geladen. Anschließend werden Original-PDFs in einem Quellordner abgelegt, in Markdown überführt und über eine Metadaten-Datei beschrieben. Zusätzliche fachliche und reflexive Materialien können in eigenen Ordnern ergänzt werden. Danach werden die Materialien gechunkt, eingebettet und in einer Vektordatenbank indexiert. Erst auf dieser Grundlage werden Backend und Benutzeroberfläche gestartet und für unterschiedliche Modi nutzbar gemacht.

## Typischer Workflow mit Befehlen
### 1. Projektordner öffnen
cd C:\Users\andre\student-course-ai-final

### 2. Virtuelle Umgebung anlegen
Nur falls noch keine `.venv` vorhanden ist:
py -3.11 -m venv .venv

### 3. Abhängigkeiten installieren
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip.exe install -r requirements.txt

### 4. Ollama prüfen oder starten
Prüfen:
ollama list

Falls nötig starten:
ollama serve

### 5. Modelle laden
Beispiel:
ollama pull qwen2.5:7b
ollama pull qwen2.5:3b-instruct
ollama pull gemma3:12b
ollama pull mxbai-embed-large

### 6. Original-PDFs ablegen
In:
text
courses\demo_kurs\source_pdfs\

### 7. `metadata.csv` ergänzen
Datei:
text
courses\demo_kurs\metadata.csv

### 8. PDFs in Markdown umwandeln
.venv\Scripts\python.exe scripts\pdfs_to_md_with_metadata.py

Vorhandene Markdown-Dateien überschreiben:
.venv\Scripts\python.exe scripts\pdfs_to_md_with_metadata.py --force

### 9. Zusätzliche Materialien ergänzen
Normale Materialien nach:
courses\demo_kurs\materials\

Reflexions-/Critical-Dateien nach:
courses\demo_kurs\critical\

### 10. Index bauen
set PYTHONPATH=.
.venv\Scripts\python.exe scripts\build_index.py --course demo_kurs

### 11. Backend starten
.venv\Scripts\python.exe -m uvicorn app.main:app --reload

### 12. Streamlit starten
In einem zweiten Fenster:

cd C:\Users\andre\student-course-ai-final
.venv\Scripts\python.exe -m streamlit run app\ui\streamlit_app.py

### 13. App im Browser öffnen
http://localhost:8501

## Wichtige Ordner mit Funktion

### Originalquellen
courses\demo_kurs\source_pdfs\

### Fachliche Materialien ald .md files
courses\demo_kurs\materials\

### Reflexions- und Zusatztexte
courses\demo_kurs\critical\
### Metadaten
courses\demo_kurs\metadata.csv

### Konfiguration
courses\demo_kurs\config.yaml
### Systemprompt
courses\demo_kurs\system_prompt.md

### Thematische Zuordnungen
courses\demo_kurs\topic_map.json

## Wann du was neu starten musst
### Nur `chat_model` in `config.yaml` geändert
Dann reicht:
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
.venv\Scripts\python.exe -m streamlit run app\ui\streamlit_app.py
### Neue Materialien / neue `.md` / neuer `critical`-Text
Dann erst neu indexieren:
set PYTHONPATH=.
.venv\Scripts\python.exe scripts\build_index.py --course demo_kurs

danach Backend und Streamlit neu starten.

### Nur Prompt geändert
Dann meist nur Backend neu starten:
.venv\Scripts\python.exe -m uvicorn app.main:app --reload

