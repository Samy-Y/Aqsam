# Aqsam – Open‑Source School Management System

**Aqsam** (Arabic **أقسام** = *“classes / sections”*) is a lightweight, modular platform that helps small‑to‑medium schools handle their daily workflow—​from enrolling students to publishing grades—​without expensive vendor lock‑in.

---

## Key Features

| Area            | What You Get                                         |
|-----------------|------------------------------------------------------|
| **Role‑based dashboards** | Separate views for **Admin**, **Teacher**, **Student**, **Parent**, **Writer** |
| **Class & subject management** | Create classes/sections, assign teachers, link multiple subjects |
| **Many‑to‑many teacher mapping** | One teacher → many classes/subjects **and** vice‑versa |
| **Attendance & grading** | Quick roll‑call UI, performance history, CSV export |
| **Assignments** *(planned)* | File uploads, deadlines, submission tracking |
| **Article publishing** | Writers can draft, edit, and publish Markdown posts |
| **Multilingual UI** | Via the `app/lang/` directory |
| **API‑ready** | All core operations exposed via JSON (coming soon) |

---

## Architecture

```text
Flask (app factory)
└── Blueprints
    ├─ auth/
    ├─ admin/
    ├─ teacher/
    ├─ student/
    └─ writer/
SQLAlchemy  (SQLite by default)
└── Models
    ├─ User  ← base
    ├─ Student / Teacher / Writer  (one‑to‑one with User)
    ├─ Class, Subject
    ├─ Grade, Article
    └─ Junctions: teacher_subject / teacher_class / teacher_grades
```

*Database migrations* are managed with **Flask‑Migrate (Alembic)**.

---

## Quick‑Start (Dev)

```bash
# 1.  Clone & enter
git clone https://github.com/your‑org/aqsam.git
cd aqsam

# 2.  Set up a virtual env & install deps
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3.  Configure (optional)
cp config.example.json config.json  # then edit secrets / DB path

# 4.  Create the DB & run
flask db upgrade        # or python -m aqsam.db_init for quick start
python run.py           # http://127.0.0.1:5000
```

> **Note:** In production, run Aqsam behind **Gunicorn/Uwsgi + Nginx** and swap SQLite for PostgreSQL.

---

## Tech Stack

* **Backend:** Flask 3 · SQLAlchemy 3 · Flask‑Login · Flask‑Migrate
* **Frontend:** Jinja2 · Bootstrap 5 (Tailwind optional)
* **Docs:** MkDocs Material
* **CI:** GitHub Actions (lint + pytest)

---

## Contributing

This project isn't even finished yet. Just wait.

---

## License

Aqsam is released under the **MIT License**.