# 🥗 Vegetarischer Wochen-Ernährungsplan

Eine **einfache und benutzerfreundliche App** zum Erstellen von personalisierten Essensplanen für vegetarische Ernährung.

## ✨ Was kann die App?

- ✅ **Automatische Wochenplanung** - Neue Rezepte jede Woche
- ✅ **Personalisierte Portionen** - Basierend auf deinem Aktivitätsniveau
- ✅ **Einkaufsliste** - Automatisch generiert aus deinem Essensplan
- ✅ **Export-Optionen** - Excel oder Apple Reminders
- ✅ **Schnelle Rezepte** - Alle Mahlzeiten in ~15 Minuten zubereitet
- ✅ **Vegetarisch** - Gesund und ausgewogen

## 🚀 Schnellstart

### Für Mac-Nutzer (empfohlen)

#### 1. Einmalige Installation
Öffne das Terminal und kopiere folgende Befehle:

```bash
cd /Users/piusschlachter/Code/Streamlit_mealplan
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chmod +x start_app.command
```

#### 2. App starten
Doppelklick auf **`start_app.command`** im Ordner `Streamlit_mealplan`

**Die App öffnet sich automatisch im Browser!**

### Für Windows-Nutzer

#### 1. Einmalige Installation
Öffne die Eingabeaufforderung und kopiere folgende Befehle:

```bash
cd C:\Users\DEINNAME\Code\Streamlit_mealplan
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### 2. App starten
Doppelklick auf **`start_app.bat`** im Ordner `Streamlit_mealplan`

---

## 📖 Benutzerhandbuch

Für detaillierte Anleitungen, siehe [SETUP_GUIDE.md](SETUP_GUIDE.md)

### Verwendung der App

1. **Woche wählen** (1-52)
2. **Aktivitätsniveau pro Tag festlegen**
3. **Wochenplan ansehen**
4. **Einkaufsliste generieren**
5. **Exportieren** (Excel oder Apple Reminders)

---

## 🍽️ Rezepte

Die App enthält über 18 vegetarische Rezepte:

### Frühstück
- Skyr-Bowl mit Beeren
- Brötchen mit Avocado & Ei
- Hafer-Erdnussbutter-Bowl
- Overnight Oats
- Tofu-Rührei

### Mittagessen & Abendessen
- Reis-Tofu-Gemüse-Pfanne
- Quinoa-Tofu-Bowl
- Linsennudel-Tomaten-Spinat
- Kichererbsen-Wraps
- Kichererbsen-Curry
- Kimchi-Fried-Rice
- und mehr...

### Snacks
- Proteinshake
- Apfel + Mandelmus
- Skyr mit Honig
- Nüsse + Banane
- Gemüsesticks + Hummus
- Edamame

---

## 🎯 Aktivitätsniveaus

Die App berechnet automatisch die richtige Portion für dich:

| Level | Kalorien | Aktivität | Beispiel |
|-------|----------|-----------|----------|
| Sedentary | 1750 kcal | Wenig Bewegung | Schreibtishjob |
| Lightly active | 2050 kcal | 1-3 Tage Sport | Leichtes Training |
| Moderately active | 2350 kcal | 3-5 Tage Sport | Standard |
| Very active | 2600 kcal | 6-7 Tage Sport | Intensives Training |

---

## 💾 Exportieren

### Excel-Dateien
- Wochenplan und Einkaufsliste als `.xlsx`
- Öffne in Excel, Google Sheets oder einem beliebigen Tabellenkalkulationsprogramm
- Perfekt zum Ausdrucken oder mobilen Zugriff

### Apple Reminders
- Importiere deine Mahlzeiten als Erinnerungen
- Automatische Benachrichtigungen für jede Mahlzeit
- Synchronisiert mit allen deinen Apple-Geräten

---

## 🛠️ Technische Details

**Anforderungen:**
- Python 3.10+
- Keine Internetverbindung erforderlich
- Funktioniert offline

**Verwendete Technologien:**
- Streamlit (Web-Interface)
- Pandas (Datenverarbeitung)
- Python (Backend)

---

## ❓ Häufig gestellte Fragen

**F: Ist die App kostenlos?**  
A: Ja, vollständig kostenlos zu verwenden.

**F: Muss ich meine Daten hochladen?**  
A: Nein, alles läuft lokal auf deinem Computer. Keine Cloud-Synchronisation.

**F: Kann ich Rezepte ändern?**  
A: Das erfordert technisches Wissen. Kontaktiere den Administrator.

**F: Funktioniert die App auf dem Handy?**  
A: Ja, du kannst auf `localhost:8501` vom Handy zugreifen, solange es im selben WLAN-Netzwerk ist.

---

## 📞 Support

Bei Problemen siehe die [Fehlerbehebung](SETUP_GUIDE.md#fehlerbehebung) im Setup-Guide.

---

**Viel Spaß mit deinem personalisierten Ernährungsplan! 🥗**
