# local-student-ai
Ein lokaler KI-Chatbot für kollaboratives Lernen, kritische Reflexion und Kompetenzentwicklung

**Praktische Einrichtung.**
Zuerst alle Ordner herunterladen (oben auf Code gehen, Download ZIP auswählen und alle Dateien herunterladen. Danach lokal unter Benutzer entzippen). Nach Installation von Python (https://www.python.org/downloads), Ollama (mit Kommando in Eingebafenster, s.u.) und den Projektabhängigkeiten werden lokale Modelle geladen. Anschließend werden Original-PDFs in einem Quellordner abgelegt, in Markdown überführt und über eine Metadaten-Datei beschrieben. Zusätzliche fachliche und reflexive Materialien können in eigenen Ordnern ergänzt werden. Danach werden die Materialien gechunkt, eingebettet und in einer Vektordatenbank indexiert. Erst auf dieser Grundlage werden Backend und Benutzeroberfläche gestartet und für unterschiedliche Modi nutzbar gemacht.  
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
│   └── demo_course/
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
courses\demo_course\source_pdfs\

### Fachliche Materialien als .md files
courses\demo_course\materials\

### Reflexions- und Zusatztexte
courses\demo_course\critical\
### Metadaten
courses\demo_course\metadata.csv

### Konfiguration
courses\demo_course\config.yaml
### Systemprompt
courses\demo_course\system_prompt.md

### Thematische Zuordnungen
courses\demo_course\topic_map.json

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
ollama pull gemma3:4b  
ollama pull gemma3:12b    

Für das embedding z.B.:  
ollama pull mxbai-embed-large  

Wenn ich ein anderes Modell verwenden will, dann muss ich dieses in der config.yaml als chat_model eintragen. 

### 6. Original-PDFs ablegen
In:  
text. 
courses\demo_course\source_pdfs\

### 7. `metadata.csv` ergänzen
Datei:
text. 
courses\demo_course\metadata.csv

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

#### Mini-Checkliste für Markdown-Dateien vor dem Indexieren
Vor dem Indexieren kann kurz geprüft werden, ob eine Markdown-Datei als gute Grundlage für die KI-Suche geeignet ist.
#### Ja/Nein-Check

- Ist der Text für Menschen gut lesbar?
- Gibt es klare Überschriften und sinnvolle Abschnitte?
- Enthält die Datei möglichst wenig Seitenzahlen, Punktlinien oder Inhaltsverzeichnis-Reste?
- Gibt es keine störenden Literatur- oder Fußnotenfragmente mitten im Fließtext?
- Sind kaputte Worttrennungen und seltsame Leerzeichen weitgehend bereinigt?
- Enthält die Datei keine unnötigen Layout-, Tabellen- oder Lizenzreste?
- Sind die Abschnitte inhaltlich zusammenhängend und nicht nur lose Fragmente?
- Würde ich wollen, dass die KI genau diesen Abschnitt als Antwortgrundlage verwendet?
  
#### Faustregel
Wenn mehrere Fragen mit **Nein** beantwortet werden, sollte die Datei vor dem Indexieren noch bereinigt oder in kleinere, klarere Einheiten aufgeteilt werden.

### 10. Zusätzliche Materialien ergänzen
Inhaltliche Materialien als  .md-Dateien nach:
courses\demo_course\materials\

Reflexions-/Critical-Dateien nach:
courses\demo_course\critical\

### 11. Index bauen
set PYTHONPATH=.

.venv\Scripts\python.exe scripts\build_index.py --course demo_course  

Beim Index bauen geschieht das sog. **"Chunking"**, ist für die Qualität des Retrievals ist das zentral. Die in Einheiten zerlegten längerne Texte werde dabei eingebettet und in der Vektordatenbank gespeichert. Relevante Parameter sind insbesondere **chunk_size**, **chunk_overlap** und **top_k**. Diese Parameter sind in der ***config.yaml*** auf Ebene des Kurses definiert (chunk_size: standarddmäßig auf 1200, chunk_overlap: standardmäßig auf 100 und top_k (als Anzahl der herangezogenen Chunks für eine Antwort): standardmäßig auf 4). Diese können je nach Material und "Auflösungstiefe" der Materialien angepasst werden. Zu große Chunks können die Suche unpräzise machen, zu kleine Chunks wichtige Zusammenhänge zerstören. Praktisch verbessert eine vorgängige Bereinigung der Materialien, etwa durch PDF-zu-Markdown-Konvertierung und das Anpassen der Markdown-Dateien hinsichtlich störender Fragmente, die Qualität der Ergebnisse deutlich.

Ebenfalls in der ***config.yaml*** ist die **Temperatur** des Modells angegeben. Die Temperatur steuert, wie eng ein Sprachmodell am bereitgestellten Material und an naheliegenden Formulierungen bleibt: Niedrige Werte führen in der Regel zu stärker materialgebundenen, stabileren Antworten, während höhere Werte eher zu freieren und weniger eng am Kontext orientierten Ausgaben führen. Standardmäßig ist die Temperatur auf 0.2 eingestellt, was bedeutet, dass die Ausgaben in der Regel stärker am bereitgestellten Material orientiert sind und konsistente Antworten mit nüchternen Formulierungen ausgegeben werden und somit weniger kreative Ausschmückung und Halluzinationen beinhalten. Es werden auch bei mehreren Abfragen weniger zufällige Varianten erzeugt. Dies ist bevorzugt wenn auf Quellenbezug und den Inhalt der bereitgestellten Materialien wert gelegt wird.

#### ACHTUNG: wenn das embedding_model: mxbai-embed-large mehrmals heruntergeladen wurde, muss in der .yaml Datei mxbai-embed-large:latest verwendet werden. Die aktuelle Version kann mit dem Befehl: ollama list herausgelesen werden.

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

### Beispielmodelle
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

# Mögliche Übungen
## Wie ändere ich das Modell?
Wenn ich das Srachmodell ändern will, überprüfe ich zuerst, ob dieses schon installiert ist. 
Das mache ich mit dem Befehl  
-> ollama list  
Falls nötig Ollama zuerst starten:  
-> ollama serve  
Wenn das Modell nicht installiert ist, dann kannich ein Modell, das ich verwenden möchte von Ollama herunterladen.  
Das mache ich mit dem Befehl:  
-> ollama pull gemma3:12b
Schlussendlich, muss ich dieses in der config.yaml als chat_model eintragen. Fertig.
## Wie ändere ich die Parameter des Chunking und die Temperatur?
Diese Parameter sind in der config.yaml abgelegt, und können dort angepasst werden. Die chunk_size ist standarddmäßig auf 2000, chunk_overlap standardmäßig auf 100 und top_k (als Anzahl der herangezogenen Chunks für eine Antwort) standardmäßig auf 4 gesetzt. 
Ebenfalls in der config.yaml ist die Temperatur des Modells angegeben. 
### Darstellung der Einstellungen in `config.yaml`
```yaml
Die kursbezogene Konfiguration liegt in:
courses/demo_kurs/config.yaml
````
Dort können zentrale Parameter der App angepasst werden.

### Modellwahl
```yaml
llm:
  chat_model: gemma3:4b
  embedding_model: mxbai-embed-large
```

* `chat_model` bestimmt das verwendete Sprachmodell für die Antworten.
* `embedding_model` bestimmt das Modell zur Einbettung und Suche in den Materialien.

Wenn Antworten zu langsam sind, kann ein kleineres Chatmodell gewählt werden. Die Auswahl lokaler Modelle richtet sich nach den in Ollama installierten Modellen.

### Retrieval
```yaml
retrieval:
  top_k: 4
  chunk_size: 1200
  chunk_overlap: 100
```
* `top_k`: Anzahl der Chunks, die für eine Antwort herangezogen werden
* `chunk_size`: Größe der Textsegmente beim Chunking
* `chunk_overlap`: Überlappung zwischen zwei Chunks
Diese Werte beeinflussen, wie gut relevante Textstellen gefunden und als Kontext genutzt werden.

### Antwortverhalten

```yaml
response:
  temperature: 0.2
  cite_sources: true
  refusal_on_missing_context: true
```

* `temperature` steuert, wie eng das Modell am bereitgestellten Material und an naheliegenden Formulierungen bleibt. Niedrige Werte führen meist zu stabileren, stärker materialgebundenen Antworten.
* `cite_sources` steuert, ob Quellenhinweise ausgegeben werden.
* `refusal_on_missing_context` steuert, ob das System eine Antwort verweigert, wenn kein ausreichender Materialkontext gefunden wird.

### Was muss nach einer Änderung neu gestartet werden?

### Nur `chat_model` oder `temperature` geändert

Dann reicht in der Regel ein Neustart von Backend und Streamlit.

#### `chunk_size`, `chunk_overlap` oder Materialien geändert

Dann muss der Index neu gebaut werden, da sich die Segmentierung oder der Materialbestand geändert hat.

## Beschreibung der vorhandenen Modi
```md
## Interaktionsmodi der App

Die App bietet verschiedene Modi, die unterschiedliche Formen der Arbeit mit den Kursmaterialien unterstützen.  
Je nach Modus liegt der Schwerpunkt stärker auf Erklärung, Zusammenfassung, Gruppenarbeit, Rückmeldung oder kritischer Reflexion.

### `explain`
Dieser Modus dient dazu, Begriffe, Zusammenhänge oder Fragen verständlich zu erklären.  
Er eignet sich besonders, wenn ein Thema zum ersten Mal erschlossen oder ein schwieriger Zusammenhang schrittweise nachvollzogen werden soll.

**Geeignet für:**
- Begriffe erklären
- Zusammenhänge verständlich machen
- in ein Thema einsteigen

**Beispiel:**
> Erkläre, was im Material unter Körperarbeit verstanden wird.

---

### `summarize`
Dieser Modus fasst Inhalte knapp und strukturiert zusammen.  
Er eignet sich, wenn ein Überblick über ein Thema oder einen Text benötigt wird.

**Geeignet für:**
- Überblick gewinnen
- längere Texte verdichten
- Vorbereitung auf Diskussionen oder Lernen

**Beispiel:**
> Fasse die wichtigsten Aussagen zum Thema Körperarbeit knapp zusammen.

---

### `quiz`
Dieser Modus erzeugt Verständnisfragen zu einem Thema oder Text.  
Er eignet sich, um Wissen zu überprüfen oder Gruppenarbeit aktivierender zu gestalten.

**Geeignet für:**
- gemeinsame Lernkontrolle
- gemeinsame Wiederholung
- Aktivierung des Wissens
- gemeinsame Suche nach den richtigen Antworten

**Beispiel:**
> Erstelle 3 Quizfragen zum Thema xy.

---

### `flashcards`
Dieser Modus erstellt Lernkarten mit Begriff und kurzer Erklärung.  
Er eignet sich besonders für Wiederholung, Prüfungsvorbereitung und Begriffsarbeit.

**Geeignet für:**
- zentrale Begriffe lernen
- Wiederholung
- Selbststudium

**Beispiel:**
> Erstelle Lernkarten zu Stanislawski, Körperarbeit und Improvisation.

---

### `study_guide`
Dieser Modus erstellt einen Lernleitfaden.  
Er ordnet die Inhalte, benennt zentrale Punkte und hilft, einen sinnvollen Lernweg zu entwickeln.

**Geeignet für:**
- Prüfungsvorbereitung
- Strukturierung eines Themas
- Orientierung bei umfangreichen Materialien

**Beispiel:**
> Erstelle einen Lernleitfaden zum Thema körperorientierte Schauspieltechniken.

---

### `group_prep`
Dieser Modus unterstützt die Vorbereitung von Gruppenbeiträgen.  
Er hilft dabei, Kernaussagen, offene Fragen und Diskussionspunkte zu strukturieren.

**Geeignet für:**
- Vorbereitung von Gruppenarbeiten
- Referate
- gemeinsame Themenerschließung

**Beispiel:**
> Hilf uns, einen Gruppenbeitrag zur Bedeutung von Körperarbeit im Schauspiel vorzubereiten.

---

### `discussion`
Dieser Modus erzeugt Material für Diskussionen.  
Er kann Perspektiven, Rückfragen und kontroverse Punkte sichtbar machen.

**Geeignet für:**
- Seminardiskussionen
- Gruppenarbeit
- kontroverse Fragestellungen

**Beispiel:**
> Erzeuge Diskussionsfragen zur Beziehung von innerem Erleben und äußerer Bewegung.

---

### `peer_review`
Dieser Modus dient der Rückmeldung zu einem vorhandenen Text.  
Dabei wird nicht nur die Frage betrachtet, sondern vor allem der eingefügte Entwurf.

**Geeignet für:**
- Rückmeldung zu Texten
- Gruppenentwürfe
- Überarbeitung von Antworten oder Zusammenfassungen

**Wichtig:**  
Zusätzlich zur Frage muss im Feld **„Text für Peer-Review“** ein zu prüfender Text eingefügt werden.

**Beispiel für das Fragefeld:**
> Bitte gib Peer-Feedback zu diesem Text im Hinblick auf Klarheit, Materialbezug und Argumentationsstruktur.

---

### `group_summary`
Dieser Modus hilft, Gruppenergebnisse kompakt zusammenzuführen.  
Er eignet sich, wenn mehrere Beiträge oder Diskussionspunkte zu einem gemeinsamen Ergebnis verdichtet werden sollen.

**Geeignet für:**
- Abschluss einer Gruppenarbeit
- Zusammenführung von Ergebnissen
- kompakte Ergebnisdarstellung

**Beispiel:**
> Formuliere eine kompakte Gruppenzusammenfassung zum Thema xy.

---

### `critical_ai_literacy`
Dieser Modus dient der **kritischen Reflexion** von KI-Antworten und Materialien.  
Er soll nicht nur antworten, sondern auch sichtbar machen,
- was im Material klar belegt ist,
- was eher Interpretation oder Verallgemeinerung ist,
- was unklar bleibt,
- was die Gruppe selbst prüfen sollte,
- und wie der KI-Einsatz transparent gemacht werden kann.

**Geeignet für:**
- kritische Prüfung von KI-Antworten
- Reflexion von Unsicherheiten
- Quellen- und Materialprüfung
- transparente KI-Nutzung

**Beispiel:**
> Prüfe die vorige Antwort auf meine Frage im Critical-AI-Literacy-Modus: Was ist klar belegt, was ist Interpretation, und was sollte die Gruppe selbst prüfen?

---

### `collaborative_work`
Dieser Modus unterstützt die Strukturierung gemeinsamer Arbeitsprozesse.  
Er hilft Gruppen dabei, Aufgaben in Teilaufgaben zu zerlegen, Rollen zu klären, Abhängigkeiten sichtbar zu machen und die Zusammenführung von Ergebnissen zu planen.

**Geeignet für:**
- Gruppenreferate
- Schreibprojekte
- Projektarbeit
- kollaboratives Arbeiten allgemein
- auch Programmierung als Spezialfall

**Beispiel:**
> Hilf uns, die Aufgabe als Gruppe zu strukturieren: Ziel, Teilaufgaben, Rollen, Abhängigkeiten und Zusammenführung.

---
```
## Welche Modi eignen sich wofür?

### Wenn etwas erklärt werden soll
- `explain`
- `study_guide`

### Wenn etwas knapp zusammengefasst werden soll
- `summarize`
- `group_summary`

### Wenn aktiv gelernt oder überprüft werden soll
- `quiz`
- `flashcards`

### Wenn Gruppenarbeit vorbereitet oder begleitet werden soll
- `group_prep`
- `discussion`
- `collaborative_work`

### Wenn ein vorhandener Text überprüft werden soll
- `peer_review`

### Wenn KI-Antworten oder Materialien kritisch geprüft werden sollen
- `critical_ai_literacy`

---

### Praktischer Hinweis

Für einfache Sachfragen reicht oft `explain` oder `summarize`.  
Für Gruppenarbeit sind `group_prep`, `discussion` und `collaborative_work` besonders nützlich.  
Wenn eine Antwort kritisch hinterfragt werden soll, ist `critical_ai_literacy` der passende Modus.  
Wenn ein vorhandener Text überprüft werden soll, sollte `peer_review` genutzt und zusätzlich ein Textentwurf eingefügt werden.
```
```
## Modi anpassen oder neue Modi hinzufügen

Die Interaktionsmodi der App lassen sich relativ einfach ändern oder erweitern. In der Regel sind dafür drei Dateien wichtig:

### 1. Bearbeiten des Modus bzw. Modus hinzufügen
Öffnen der Datei mit einem Editor:
```text
app/ui/streamlit_app.py
````

Dort wird die Liste der auswählbaren Modi in der `selectbox` gepflegt.
Ein bestehender Modus kann dort umbenannt oder ein neuer Modus ergänzt werden.

Beispiel:

```python
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
        "collaborative_work",
        "neuer_modus",
    ],
    index=0,
)
```

### 2. Festlegen, wie der Modus antworten soll
Öffnen der Datei mit einem Editor:
```text
app/core/prompts.py
```

Hier wird definiert, welche Aufgabe ein Modus erfüllen soll.
Dazu wird im `mode_instruction`-Block ein neuer Eintrag ergänzt oder ein bestehender angepasst.

Beispiel:

```python
"neuer_modus": "Beschreibe kurz, was dieser Modus tun soll und in welcher Struktur geantwortet werden soll.",
```

Wenn ein Modus eine speziellere Prompt-Logik braucht, kann in derselben Datei auch eine eigene Behandlung ergänzt werden.

**Nicht alle Modi werden jedoch in prompts.py im mode_instruction-Block definiert. critical_ai_literacy wird in build_user_prompt() separat behandelt, weil dieser Modus Fach- und Reflexionskontext getrennt verarbeitet. peer_review verwendet mit build_peer_review_prompt() eine eigene Funktion, da hier zusätzlich ein zu prüfender Text einbezogen wird. Die übrigen Modi werden über den mode_instruction-Block gesteuert.**

**Generell arbeitet die App mit einem mehrschichtigen Prompt-System:  
-> prompts.py - baut den konkreten User-Prompt aus Frage, Modus, Kontext und zusätzlichen Regeln,     
-> system_prompt.md - enthält den allgemeinen Antwort- und Regelrahmen des Kurses.,  
-> chat.py - legt fest, welche Inhalte aus den verfügbaren Kursdaten für einen bestimmten Modus verwendet werden. Dazu können fachliche Materialien aus materials/ ebenso gehören wie zusätzliche Reflexions- und Orientierungstexte aus critical/.** 


### 3. Falls nötig: Retrieval oder Sonderlogik anpassen

Öffnen der Datei mit einem Editor:

```text
app/api/chat.py
```

#### Kontext je nach Modus steuern

In `app/api/chat.py` wird festgelegt, aus welchen Bereichen der Kursdaten der Kontext für einen Modus geholt wird.

- Der Modus critical_ai_literacy trennt zwischen Fachkontext (materials/) und zusätzlichem Reflexionskontext (critical/). Das bedeutet, dass zuerst der fachliche Inhalt aus den Materialien erschlossen und danach kritisch reflektiert wird.
- Der Modus collaborative_work kann Materialien und Critical-Texte gemeinsam nutzen. Dabei werden Fachinhalt und Reflexions- bzw. Orientierungstexte zusammen verwendet, um Gruppen bei der Planung und Durchführung gemeinsamer Arbeit zu unterstützen.
- Alle übrigen Modi greifen standardmäßig nur auf fachliche Materialien aus materials/ zu. Das bedeutet, dass ihre Antworten in erster Linie auf den inhaltlichen Kursmaterialien beruhen und keine zusätzlichen Reflexionstexte aus critical/ einbeziehen.

Beispiel aus `app/api/chat.py`:

```python
if req.mode == "critical_ai_literacy":
    hits = retrieve(
        course_id=req.course_id,
        question=req.question,
        embedding_model=cfg["llm"]["embedding_model"],
        top_k=max(2, min(cfg["retrieval"]["top_k"], 3)),
        allowed_content_types=["material"],
    )

    critical_hits = retrieve(
        course_id=req.course_id,
        question=req.question,
        embedding_model=cfg["llm"]["embedding_model"],
        top_k=2,
        allowed_content_types=["critical"],
    )
elif req.mode == "collaborative_work":
    hits = retrieve(
        course_id=req.course_id,
        question=req.question,
        embedding_model=cfg["llm"]["embedding_model"],
        top_k=cfg["retrieval"]["top_k"],
        allowed_content_types=["material", "critical"],
    )
else:
    hits = retrieve(
        course_id=req.course_id,
        question=req.question,
        embedding_model=cfg["llm"]["embedding_model"],
        top_k=cfg["retrieval"]["top_k"],
        allowed_content_types=["material"],
    )
```
#### Zusätzliche Materialien für einen Modus hinzufügwn

Wenn ein Modus zusätzliche Inhalte oder Reflexionstexte nutzen soll, können passende Markdown-Dateien ergänzt werden in:
```text
courses/demo_course/materials/
courses/demo_course/critical/
```

* `materials/` für fachliche Inhalte
* `critical/` für Reflexions-, Transparenz- oder Orientierungstexte

---
### Danach nicht vergessen

#### Wenn neue Materialien hinzugefügt wurden
Nach dem Hinzufügen neuer Dateien muss der Index neu gebaut werden.
```bat
set PYTHONPATH=.
.venv\Scripts\python.exe scripts\build_index.py --course demo_course
```

#### Backend neu starten

```bat
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

#### Streamlit neu starten

```bat
.venv\Scripts\python.exe -m streamlit run app\ui\streamlit_app.py
```
---

### Kurz gesagt

Ein neuer oder angepasster Modus braucht in der Regel:

* einen Eintrag in `app/ui/streamlit_app.py`
* eine Prompt-Definition in `app/core/prompts.py`
* gegebenenfalls eine Anpassung in `app/api/chat.py`
* optional neue Markdown-Dateien in `materials/` oder `critical/`

# Beschreibung des Interaktionsfensters
## Seitenleiste: Lernprofil und Lernverlauf

Die App zeigt in der Seitenleiste lokal gespeicherte Profil- und Verlaufsdaten an. Diese Informationen werden nicht in einer externen Cloud gespeichert, sondern im Projektordner unter `student_data/`, typischerweise nutzerbezogen in einem Unterordner wie:  
-> student_data/default_user/

### Lernprofil (`profile.json`)
Das Lernprofil wird aus `profile.json` geladen. Dort stehen grundlegende Präferenzen des Nutzers/der Nutzerin und müssen selbst eingetragen werden, zum Beispiel:

* "user_id": "default_user",  
* "language": "de",  
* "preferred_style": "klar, strukturiert, fachlich",  
* "level": "unbekannt",  
* "preferred_term_mode": "de_with_en_in_brackets",
* "learning_goals": ["Verstehen"]

Daraus entstehen in der Seitenleiste zum Beispiel die Einträge:

* **Sprache: de**
* **Stil: klar, strukturiert, fachlich**
* **Niveau: unbekannt**
* **Lernziele: Verstehen**

Wenn `learning_goals` leer ist, erscheint unter **Lernziele** ein Hinweis wie „Noch keine Lernziele eingetragen“.

### Lernverlauf (`progress.json`)

Weitere Bereiche der Seitenleiste werden aus `progress.json` erzeugt. Dazu gehören insbesondere:

* `seen_topics` – bereits bearbeitete oder erkannte Themen
* `difficult_topics` – als schwierig markierte Themen
* `open_questions` – offene oder ungeklärte Fragen
* `last_question` – zuletzt gestellte Frage
* `last_session_summary` – zuletzt gespeicherte Antwort oder Zusammenfassung

### Bedeutung der einzelnen Anzeigen

* **Bearbeitete Themen**
*   Der Bereich **Bearbeitete Themen** wird aus dem Feld `seen_topics` in `student_data/default_user/progress.json` erzeugt.  
*   Diese Themen werden nicht manuell formuliert, sondern heuristisch erkannt. Grundlage dafür ist die Datei:
```
*   courses/demo_course/topic_map.json
````
*   In `topic_map.json` werden Themennamen mit typischen Schlüsselwörtern verknüpft. Wenn in Fragen oder Antworten passende Begriffe vorkommen, kann die App diese Themen als bereits bearbeitet speichern.

*   Wenn in `topic_map.json` nur Platzhalter oder Beispielthemen stehen, können keine sinnvollen Themen erkannt werden. In diesem Fall bleibt `seen_topics` leer und in der Seitenleiste erscheint: ***Noch keine Themen gespeichert.***  

* **Schwierige Themen**  
  Werden aus `difficult_topics` in `student_data/default_user/progress.json` geladen. Die Erkennung und Aktualisierung erfolgt in `app/core/student_memory.py`. Wenn dabei zwar Unsicherheit erkannt wurde, aber kein genaues Thema zugeordnet werden konnte, kann ein allgemeiner Platzhalter erscheinen.

  Schwierige Themen werden dort über einfache Unsicherheitsmarker erkannt, zum Beispiel:

  * `ich verstehe nicht`
  * `unklar`
  * `nicht eindeutig`
  * `schwierig`
  * `unsicher`
  * `verwirrt`
  * `was genau`
  * `nicht klar`
  * `mehrdeutig`

  Wenn dabei bereits Themen erkannt wurden, werden diese als schwierige Themen gespeichert. Wenn kein konkretes Thema zugeordnet werden kann, wird aktuell ein allgemeiner Platzhalter eingetragen.

* **Offene Fragen**  
  Werden aus `open_questions` in `student_data/default_user/progress.json` geladen. Ist die Liste leer, erscheint „Noch keine offenen Fragen gespeichert“. Die Erkennung und Aktualisierung erfolgt ebenfalls in `app/core/student_memory.py`.

  Offene Fragen werden gespeichert, wenn die erzeugte Antwort sprachliche Hinweise darauf enthält, dass ein Punkt noch nicht eindeutig oder nicht direkt geklärt werden konnte. Dazu gehören Marker wie `nicht eindeutig`, `nicht klar`, `im material nicht direkt`, `nicht direkt beantwortet` oder `unsicherheit`. In diesem Fall wird die ursprüngliche Nutzerfrage in `open_questions` übernommen.

* **Letzte Sitzung**  
  Wird aus `last_question` und `last_session_summary` erzeugt. Dort kann also die letzte Frage und die dazu gespeicherte Antwort oder Zusammenfassung erscheinen.

### Verlauf verwalten

Über die Buttons in der Seitenleiste kann der lokale Verlauf wieder gelöscht oder zurückgesetzt werden, zum Beispiel:

* **Lernverlauf löschen**
* **Fortschritt zurücksetzen**
* **Alles zurücksetzen**

Damit lassen sich die gespeicherten Profil- und Verlaufsdaten lokal bereinigen.


