# 🥗 Vegetarischer Ernährungsplan App - Benutzerhandbuch

## Für Mac-Benutzer (einfachste Option)

### Erste Installation (einmalig)
1. Öffne das Terminal (Spotlight-Suche: `Terminal`)
2. Kopiere folgende Befehle und füge sie ins Terminal ein:

```bash
cd /Users/piusschlachter/Code/Streamlit_mealplan
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chmod +x start_app.command
```

3. Drücke Enter und warte, bis alles installiert ist (dauert ca. 2-3 Minuten)

### App starten (jedes Mal danach)
**Option 1: Doppelklick (am einfachsten)**
- Gehe zum Ordner `Streamlit_mealplan`
- Doppelklick auf `start_app.command`
- Die App öffnet sich automatisch im Browser

**Option 2: Terminal-Befehl**
```bash
cd /Users/piusschlachter/Code/Streamlit_mealplan
source .venv/bin/activate
streamlit run src/mealplan/app.py
```

---

## Für Windows-Benutzer

### Erste Installation (einmalig)
1. Öffne die Eingabeaufforderung (Suche: `cmd`)
2. Kopiere folgende Befehle:

```bash
cd C:\Users\DEINNAME\Code\Streamlit_mealplan
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

3. Drücke Enter und warte auf die Installation (ca. 2-3 Minuten)

### App starten (jedes Mal danach)
**Option 1: Doppelklick**
- Gehe zum Ordner `Streamlit_mealplan`
- Doppelklick auf `start_app.bat`

**Option 2: Eingabeaufforderung**
```bash
cd C:\Users\DEINNAME\Code\Streamlit_mealplan
.venv\Scripts\activate.bat
streamlit run src\mealplan\app.py
```

---

## Wie man die App verwendet

### Schritt 1: Woche auswählen
- Gib die Wochennummer ein (1-52)
- Woche 1 = erste Woche des Jahres

### Schritt 2: Aktivitätsniveau pro Tag festlegen
Wähle für jeden Wochentag, wie aktiv du sein wirst:

| Level | Beschreibung | Beispiel |
|-------|-------------|----------|
| 🛋️ Sedentary | Wenig Bewegung | Bürojob, wenig Sport |
| 🚶 Lightly active | Leichte Aktivität | 1-3 Tage Sport pro Woche |
| 🏃 Moderately active | Mittlere Aktivität | 3-5 Tage Sport (Standard) |
| 🏋️ Very active | Viel Sport | 6-7 Tage intensives Training |

### Schritt 3: Wochenplan ansehen
Die App zeigt dir automatisch:
- **Alle Mahlzeiten** für die Woche
- **Zutatenmengen** passend zu deinem Aktivitätsniveau
- **Zubereitungszeit** (~15 Minuten pro Mahlzeit)

### Schritt 4: Einkaufsliste nutzen
Die Einkaufsliste zeigt:
- **Alle Zutaten**, die du brauchst
- **Mengen** berechnet für dein höchstes Aktivitätsniveau
- Sortiert nach Zutat für leichteres Einkaufen

### Schritt 5: Speichern und mitnehmen

**Excel-Dateien** (Wochenplan & Einkaufsliste):
- Klick auf Download-Button
- Öffne die Datei in Excel oder Google Sheets
- Drucke sie aus oder schau sie mobil an

**Apple Reminders** (Erinnerungen):
- Klick auf "Zu Reminders importieren"
- Die `.ics` Datei öffnet sich automatisch
- Alle Mahlzeiten werden als Erinnerungen im Kalender angezeigt

---

## Häufig gestellte Fragen

### F: Was bedeuten die Einheiten?
- **g** = Gramm
- **ml** = Milliliter
- **TL** = Teelöffel (~5ml)
- **EL** = Esslöffel (~15ml)
- **Stk** = Stück

### F: Warum unterscheiden sich die Mengen pro Tag?
Die Mengen werden basierend auf deinem gewählten Aktivitätsniveau berechnet. Mehr Aktivität = mehr Kalorien = größere Portionen.

### F: Kann ich eine andere Woche wählen?
Ja! Wähle einfach eine andere Wochennummer (1-52). Die Rezepte wechseln jede Woche automatisch.

### F: Sind alle Rezepte vegetarisch?
Ja! Alle Rezepte enthalten kein Fleisch oder Fisch.

### F: Kann ich Rezepte ändern oder meine eigenen hinzufügen?
Das erfordert technisches Wissen. Kontaktiere den Administrator für Änderungen.

---

## Fehlerbehebung

### Problem: "Befehl nicht erkannt"
- Stelle sicher, dass du im richtigen Verzeichnis bist
- Mac: `cd /Users/DEINNAME/Code/Streamlit_mealplan`
- Windows: `cd C:\Users\DEINNAME\Code\Streamlit_mealplan`

### Problem: Browser öffnet sich nicht
- Öffne manuell: `http://localhost:8501`
- Die App läuft im Terminal/Eingabeaufforderung im Hintergrund

### Problem: "ModuleNotFoundError"
- Stelle sicher, dass die virtuelle Umgebung aktiviert ist:
  - Mac: `source .venv/bin/activate`
  - Windows: `.venv\Scripts\activate.bat`

### Problem: App startet gar nicht
- Versuche die Installation neu: Lösche den Ordner `.venv` und wiederhole den ersten Installationsschritt

---

## Kontakt & Support

Bei Fragen oder Problemen kontaktiere: [Administrator]

Viel Spaß mit deinem personalisierten Ernährungsplan! 🥗
