# local-student-ai
Ein lokaler KI-Chatbot für kollaboratives Lernen, kritische Reflexion und Kompetenzentwicklung

**Praktische Einrichtung.**
Zuerst alle Ordner herunterladen (oben auf Code gehen, Download ZIP auswählen und alle Dateien herunterladen. Danach lokal unter Benutzer entzippen). Nach Installation von Python, Ollama und den Projektabhängigkeiten werden lokale Modelle geladen. Anschließend werden Original-PDFs in einem Quellordner abgelegt, in Markdown überführt und über eine Metadaten-Datei beschrieben. Zusätzliche fachliche und reflexive Materialien können in eigenen Ordnern ergänzt werden. Danach werden die Materialien gechunkt, eingebettet und in einer Vektordatenbank indexiert. Erst auf dieser Grundlage werden Backend und Benutzeroberfläche gestartet und für unterschiedliche Modi nutzbar gemacht.  
**Strukturelle Gliederung.**
Die Materialien der App sind in mehrere Bereiche gegliedert: Originalquellen liegen in einem PDF-Ordner vor, fachliche Kursmaterialien werden in einem Materialordner als Markdown aufbereitet, und zusätzliche Reflexions- und Orientierungstexte können in einem eigenen Critical-Ordner hinterlegt werden. Ergänzt wird dies durch Konfigurations-, Prompt- und Metadatendateien. Die App arbeitet mit verschiedenen Modi, die von Erklärung, Zusammenfassung und Quiz über Gruppenarbeit und Peer-Review bis hin zu kritischer KI-Reflexion und der Strukturierung kollaborativer Arbeitsprozesse reichen.
## Voraussetzungen RAM und VRAM
Arbeitsspeicher (RAM) und Grafikspeicher (VRAM) sind getrennte Ressourcen. Für kleinere lokale Modelle kann ein Rechner mit 16 GB RAM auch ohne starke GPU ausreichen, dann allerdings oft mit längeren Antwortzeiten. Wenn eine dedizierte GPU genutzt wird, sind etwa 6–8 GB VRAM ein brauchbarer Einstieg, während 10–12 GB oder mehr das Arbeiten mit größeren Modellen deutlich erleichtern.
## Benötigter lokaler Speicherplatz
Neben RAM und gegebenenfalls VRAM ist auch ausreichender freier Speicherplatz erforderlich. Als grobe Untergrenze erscheinen etwa 15-30 GB sinnvoll; bei mehreren lokalen Modellen, umfangreicheren Materialsammlungen oder mehreren Kursindizes können mehr als 30 GB notwendig sein.
## Allgemeines zu Installation und Start des Modells
Zuerst werden die Ordner und die notwendigen Dateien installiert. Die Installation der notwendigen Dateien und Modelle erfolgt im Eingabefenster (Windows-Taste und "R", dann cmd, dann in den Ordner des Chatbots wechseln, und die weiteren Befehle ausführen). Nach der Installation werden einerseits das Backend und die Applikation in jeweils einem eigenen Eingabefenster gestartet, dadurch öffnet sich im Browser normalerweise direkt das User Interface (Streamlit). Wenn man etwas ändern möchte bzw. geändert hat, dann kann man mit der Strg.-Taste und "C" den laufenden Prozess unterbrechen, und wieder neu starten. Alles weitere findet sich in der untenstehenden Anleitung.

## Projektstruktur
```text
student-course-ai/
├── app/
│   ├── api/
│   ├── core/
│   └── ui/
├── courses/
│   └── demo_kurs/
│       ├── source_pdfs/
│       ├── materials/
│       ├── critical/
│       ├── config.yaml
│       ├── system_prompt.md
│       ├── metadata.csv
│       └── topic_map.json
├── scripts/
├── student_data/
├── requirements.txt
└── README.md
```
### Ordnerstruktur und Funktion

| Bereich            | Funktion                                                                                                                                        |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `source_pdfs/`     | Enthält die Originalquellen, insbesondere PDF-Dateien.                                                                                          |
| `materials/`       | Enthält die fachlichen, für das Retrieval aufbereiteten Materialien, meist als Markdown.                                                        |
| `critical/`        | Enthält zusätzliche Reflexions- und Orientierungstexte, etwa für kritische KI-Reflexion oder die Strukturierung kollaborativer Arbeitsprozesse. |
| `metadata.csv`     | Enthält strukturierte Metadaten zu Quellen, z. B. Titel, Autor:in, Jahr, DOI, URL und Dateizuordnung.                                           |
| `config.yaml`      | Enthält die zentrale Konfiguration, etwa Modellwahl, Retrieval-Parameter und Antwortverhalten.                                                  |
| `system_prompt.md` | Enthält die grundlegenden Regeln und den didaktischen Rahmen für die Antworten der App.                                                         |
| `topic_map.json`   | Enthält thematische Zuordnungen für Lern- und Verlaufsfunktionen.                                                                               |

## Wichtige Ordner mit Funktion
### Originalquellen
courses\demo_kurs\source_pdfs\

### Fachliche Materialien als .md files
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

### Modi der App

| Modus                  | Funktion                                                                                                    |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| `explain`              | Erklärt Begriffe und Zusammenhänge verständlich.                                                            |
| `summarize`            | Fasst Materialien oder Themen strukturiert zusammen.                                                        |
| `quiz`                 | Erzeugt Verständnisfragen für Lern- und Gruppenprozesse.                                                    |
| `flashcards`           | Erstellt Lernkarten für Wiederholung und Begriffsarbeit.                                                    |
| `study_guide`          | Unterstützt die Strukturierung von Lernprozessen.                                                           |
| `group_prep`           | Unterstützt die Vorbereitung von Gruppenbeiträgen.                                                          |
| `discussion`           | Erzeugt Fragen, Perspektiven und Kontroversen für Diskussionen.                                             |
| `peer_review`          | Unterstützt Rückmeldungen zu Texten und Entwürfen.                                                          |
| `group_summary`        | Bündelt Gruppenergebnisse in verdichteter Form.                                                             |
| `critical_ai_literacy` | Unterstützt die kritische Prüfung von KI-Antworten und Materialien.                                         |
| `collaborative_work`   | Unterstützt die Strukturierung gemeinsamer Arbeitsprozesse, z. B. Rollen, Teilaufgaben und Zusammenführung. |

## Typischer Workflow

1. Projektordner anlegen (z.B. C:\Users\andre\student-course-ai)
2. Python (3.11 bis 3.13) und die vorausgesetzten files (in requirements.text) installieren (mit Windows "R" Taste und "cmd" das Eingabefenster öffnen)
3. PDFs nach `source_pdfs/` legen
4. `metadata.csv` ergänzen (Metadaten werden beim Tool-spezifischen Ablauf der Markdown-files automatisch in den Header geschrieben. Wichtig: Filename und Eintrag im Metadatenfile müssen eindeutig übereinstimmen (inkl. Filetyp-Endung)
5. PDFs in Markdown überführen
6. Materialien in `materials/` und ggf. `critical/` ablegen
7. Index bauen (Chunking Parameter beachten)
8. Backend starten
9. Streamlit starten
10. Modi testen und bei Bedarf anpassen (die Metaprompts aber auch z. B. die Temperatur lässt sich in der config.yaml Datei anpassen)

## Typischer Workflow mit Befehlen
### 1. Projektordner öffnen
cd C:\Users\andre\student-course-ai

### 2. Virtuelle Umgebung anlegen
Nur falls noch keine `.venv` vorhanden ist:  
py -3.11 -m venv .venv (oder mit Python 3.13 - damit wurde das Modell erfolgreich getestet)

### 3. Abhängigkeiten installieren
.venv\Scripts\python.exe -m pip install --upgrade pip     
.venv\Scripts\pip.exe install -r requirements.txt  

### 4. Ollama prüfen oder starten
Prüfen:  
ollama list -> listet welche Modelle bereits lokal vorhanden sind

Falls nötig starten:  
ollama serve

### 5. Modelle herunterladen (von https://ollama.com/library/)
Beispiel:  
ollama pull qwen2.5:7b  
ollama pull qwen2.5:3b-instruct  
ollama pull gemma3:12b  
ollama pull mxbai-embed-large  

Wenn ich ein anderes Modell verwenden will, dann muss ich dieses in der config.yaml als chat_model eintragen. 

### 6. Original-PDFs ablegen
In:  
text. 
courses\demo_kurs\source_pdfs\

### 7. `metadata.csv` ergänzen
Datei:
text. 
courses\demo_kurs\metadata.csv

### 8. PDFs in Markdown umwandeln
.venv\Scripts\python.exe scripts\pdfs_to_md_with_metadata.py

Vorhandene Markdown-Dateien überschreiben:  
.venv\Scripts\python.exe scripts\pdfs_to_md_with_metadata.py --force

### 9. Alternative PDF-zu-Markdown-Skripte basierend auf MarkItDown (muss noch separat installiert werden)
scripts/pdfs_to_md_alternative.py. 
Einige alternative Skripte zur Umwandlung von PDFs in Markdown basieren auf **MarkItDown**.  
Diese Variante ist nicht Teil der Standardinstallation und erfordert eine separate Installation von markitdown.  
Beispiel:
py -m pip install "markitdown[all]". 
Das pdfs_to_md_alternative.py file wird in den source_pdfs Ordner kopiert und über die Befehlseingabe aufgerufen. Dadurch werden die entsprechenden .md files kreiert, die dann in den materials Ordner kompiert werden.

### 10. Zusätzliche Materialien ergänzen
Normale Materialien nach:
courses\demo_kurs\materials\

Reflexions-/Critical-Dateien nach:
courses\demo_kurs\critical\

### 11. Index bauen
set PYTHONPATH=.

.venv\Scripts\python.exe scripts\build_index.py --course demo_kurs  

Das Chunking, das beim Index bauen geschieht, ist für die Qualität des Retrievals ist das zentral. Die in Einheiten zerlegten längerne Texte werde dabei eingebettet und in der Vektordatenbank gespeichert. Relevante Parameter sind insbesondere chunk_size, chunk_overlap und top_k.  Diese Parameter sind in der config.yaml auf Ebene des Kurses definiert (chunk_size: standarddmäßig auf 2000, chunk_overlap: standardmäßig auf 100 und top_k (als Anzahl der herangezogenen Chunks für eine Antwort): standardmäßig auf 4). Diese können je nach Material und "Auflösungstiefe" der Materialien angepasst werden. Zu große Chunks können die Suche unpräzise machen, zu kleine Chunks wichtige Zusammenhänge zerstören. Praktisch verbessert eine vorgängige Bereinigung der Materialien, etwa durch PDF-zu-Markdown-Konvertierung und das Anpassen der Markdown-Dateien hinsichtlich störender Fragmente, die Qualität der Ergebnisse deutlich.

Ebenfalls in der config.yaml ist die Temperatur des Modells angegeben. Die Temperatur steuert, wie eng ein Sprachmodell am bereitgestellten Material und an naheliegenden Formulierungen bleibt: Niedrige Werte führen in der Regel zu stärker materialgebundenen, stabileren Antworten, während höhere Werte eher zu freieren und weniger eng am Kontext orientierten Ausgaben führen. Standardmäßig ist die Temperatur auf 0.2 eingestellt, was bedeutet, dass die Ausgaben in der Regel stärker am bereitgestellten Material orientiert sind und konsistente Antworten mit nüchternen Formulierungen ausgegeben werden und somit weniger kreative Ausschmückung und Halluzinationen beinhalten. Es werden auch bei mehreren Abfragen weniger zufällige Varianten erzeugt. Dies ist bevorzugt wenn auf Quellenbezug und den Inhalt der bereitgestellten Materialien wert gelegt wird.

### 12. Backend starten (erstes Eingabefenster - Windows-Taste und "R", dann cmd eintippen)
Erstes Fenster öffen  

cd C:\Users\andre\student-course-ai  
.venv\Scripts\python.exe -m uvicorn app.main:app --reload

### 13. Streamlit starten (zweites Eingabefenster, wiede Windows-Taste und "R", dann cmd eintippen)
In einem zweiten Fenster:

cd C:\Users\andre\student-course-ai  
.venv\Scripts\python.exe -m streamlit run app\ui\streamlit_app.py

### 14. App im Browser öffnen
http://localhost:8501

## Wann muss was neu gestartet werden 
### Nur `chat_model` in `config.yaml` geändert
Dann reicht:
.venv\Scripts\python.exe -m uvicorn app.main:app --reload. 
.venv\Scripts\python.exe -m streamlit run app\ui\streamlit_app.py. 

### Neue Materialien / neue `.md` / neuer `critical`-Text
Dann erst neu indexieren:
set PYTHONPATH=. 
.venv\Scripts\python.exe scripts\build_index.py --course demo_kurs

danach Backend und Streamlit neu starten.

### Nur Prompt geändert
Dann meist nur Backend neu starten:  
.venv\Scripts\python.exe -m uvicorn app.main:app --reload

## Mögliche Modelle für den lokalen Betrieb
Für die lokale Nutzung erwies sich ein mittelgroßes Modell als besonders praktikabel, da es ein gutes Verhältnis zwischen Antwortqualität, Sprachkompetenz in Deutsch und Englisch sowie Verarbeitungsgeschwindigkeit bietet; kleinere Modelle sind für ressourcenschwächere Systeme interessant, größere Modelle eher für leistungsstärkere Rechner und qualitativ anspruchsvollere Szenarien. Auf https://ollama.com/library finden sich immer die neuesten verfügbaren Modelle.

Grundsätzlich (die Zahl "b" gibt dabei die Modellgröße in Milliarden Parametern an und entspricht grob dem benötigen RAM-Speicher in GB):  
3B–4B: schneller, schwächere Rechner  
7B: guter Allrounder  
12B–14B+: besser, aber deutlich langsamer und speicherhungriger  

# Beispielmodelle
- Standardmodell: qwen2.5:7b
- Schnellmodus: qwen2.5:3b-instruct
- Qualitätsmodus: gemma3:12b

qwen2.5:7b ist für Englisch und Deutsch wahrscheinlich dein bester Allrounder, hier können und sollten weitere Tests systematisch selbst durchgeführt werden.

# So testest du die drei Modelle sinnvoll
Du vergleichst immer dieselbe Frage mit:
qwen2.5:7b. 
qwen2.5:3b-instruct. 
gemma3:12b

und achtest auf:

Geschwindigkeit
Deutsch. 
Englisch. 
Quellentreue. 
Nützlichkeit für eure Modi. 

## Immer nur ein Modell in config.yaml z.B
chat_model: qwen2.5:7b
## embedding_model in config.yaml bleibt gleich:
embedding_model: mxbai-embed-large
## Zeit messen und Qualität bewerten
Tabellarische Vergleichsdokumentation erstellen.
