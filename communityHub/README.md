# 🏘️ CommunityHub

Forum + Archiv-Plattform für Vereine & Communities  
**IHK Abschlussprojekt – Fachinformatiker Anwendungsentwicklung (FIAE)**

---

## 📁 Projektstruktur

```
communityHub/
├── backend/
│   ├── __init__.py       # App-Factory (create_app)
│   ├── app.py            # Konfiguration & Initialisierung
│   ├── models.py         # Datenbankmodelle
│   ├── routes/
│   │   ├── auth.py       # Login / Register / Logout
│   │   ├── forum.py      # Beiträge & Kommentare
│   │   └── archiv.py     # Datei-Upload & Links
│   └── uploads/          # Hochgeladene Dateien (auto-erstellt)
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/         # login.html, register.html
│   │   ├── forum/        # uebersicht, detail, neu, bearbeiten
│   │   └── archiv/       # uebersicht, datei_hochladen, link_neu
│   └── static/
│       └── css/style.css
├── run.py
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Starten

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. App starten

```bash
python run.py
```

### 3. Im Browser öffnen

```
http://127.0.0.1:5000
```

Die Datenbank (`communityHub.db`) wird beim ersten Start automatisch erstellt.

---

## ⚙️ Tech-Stack

| Bereich   | Technologie              |
|-----------|--------------------------|
| Backend   | Python 3.x + Flask       |
| Datenbank | SQLite + SQLAlchemy ORM  |
| Auth      | Flask-Login + Werkzeug   |
| Frontend  | HTML5 + CSS3 + Jinja2    |

---

## ✅ Features

- **Registrierung & Login** mit Session-basierter Authentifizierung
- **Forum** – Beiträge erstellen, lesen, bearbeiten, löschen
- **Kategorien** – Allgemein, Ankündigungen, Fragen, Projekte, Offtopic
- **Kommentare** – Hinzufügen und Löschen
- **Archiv** – PDF/Dokumente hochladen und herunterladen
- **Links** – URLs mit Titel & Beschreibung speichern
- Nur eigene Beiträge/Dateien/Links können gelöscht werden

---

## 🔒 Sicherheit

- Passwörter werden mit `werkzeug.security` gehasht (PBKDF2 + SHA256)
- Dateinamen werden mit `secure_filename` bereinigt
- Jede Route ist mit `@login_required` geschützt
- Dateigrößen-Limit: 16 MB

---

## 📝 Hinweis

`SECRET_KEY` in `backend/app.py` vor dem Produktiveinsatz ändern!
