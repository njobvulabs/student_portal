# AGENTS.md — Student Portal

## Project

NJOBVU COLLEGE Student Portal — Django 5.0.1 monolith (Python 3.14.6).  
Two apps: `users` (custom `User` model, auth, profiles) and `courses` (courses, assignments, enrollments, grades, announcements).

## Commands (run from repo root)

```bash
# Dev server
python manage.py runserver

# Migrations
python manage.py makemigrations && python manage.py migrate

# Tests — 27 tests across both apps
python manage.py test

# Create a dummy announcement (custom command)
python manage.py create_announcement
python manage.py create_announcement --title "Exam Update" --content "..." --course-id 1

# Static files for production
python manage.py collectstatic

# Create admin user
python manage.py createsuperuser
```

## Key Architecture

- **Settings**: `student_portal/settings` — `DEBUG`/`PRODUCTION` driven by env vars, defaults to `False`.
  No production_settings module (deleted — was dead code).
- **Custom User Model**: `users.models.User` (extends `AbstractUser`). Roles: `student`, `instructor`, `admin`.
- **Templates**: All live in project-level `templates/` (`templates/courses/`, `templates/users/`). App-level template dirs are empty.
- **Static files**: WhiteNoise (`CompressedManifestStaticFilesStorage`), collected to `staticfiles/`.
  `default-avatar.png` lives in `static/img/`.
- **Env vars**: Loaded from `.env` via `python-dotenv`. PostgreSQL via `DB_NAME/USER/PASSWORD/HOST/PORT`; falls back to SQLite.
- **Frontend**: Bootstrap 5.3 + Font Awesome 6.0 from CDN. Dark/light theme toggle in `base.html`.

## Conventions

- `django-crispy-forms` + `crispy-bootstrap5` for form rendering.
- No linters, formatters, typecheckers, pre-commit, or CI/CD configured.
- Single branch (`main`), single commit — treat as early-stage project.
- Deployed to `njobvu4linux.pythonanywhere.com`.

## Known Quirks

- `Grade.max_score` is a `@property` delegating to `assignment.max_score` (not a DB field).
  Don't use `annotate` or `F()` on it — compute percentages in Python.
- `Grade.assignment_name` is also a `@property` (delegates to `assignment.title`).
- Python 3.14 + Django 5.0.1 test client requires a patch to `BaseContext.__copy__` in
  `venv/lib/python3.14/site-packages/django/template/context.py` (addressed in-place).
