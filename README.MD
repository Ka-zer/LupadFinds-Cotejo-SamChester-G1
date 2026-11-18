# LupadFinds

A Django web application for reporting and managing **lost items** on campus. Students and staff can submit lost-item reports, while administrators can see and manage all reports.

---

## Features

- School-email-only signup and login (`@cit.edu` by default)
- User profiles with role-based access control:
  - **Student** / **Staff** — see and manage only their own lost reports
  - **Admin** — see and manage all lost reports
- Role-specific dashboards with counts and recent activity
- Lost-item reports with category, last-known location, date lost, and description
- Validation: item name ≥ 3 characters, description ≥ 10 characters, date lost cannot be in the future
- Seeded categories and locations (via data migration)
- Toggle between local **SQLite** and remote **PostgreSQL / Supabase** using one environment variable

---

## Tech stack

- Python 3.13+
- Django 6.1
- `psycopg[binary]` (for optional PostgreSQL/Supabase use)
- `python-dotenv`
- SQLite (default local database)

---

## Getting started

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Create a `.env` file in the project root

```dotenv
SECRET_KEY=replace-with-a-long-random-string
DEBUG=True

# Local development (default)
DB_ENGINE=sqlite

# Only needed when DB_ENGINE is set to postgresql
DB_NAME=postgres
DB_USER=your-user
DB_PASSWORD=your-password
DB_HOST=your-host.pooler.supabase.com
DB_PORT=5432
DB_SSLMODE=require
```

> `.env` is listed in `.gitignore` and must never be committed. Generate a real `SECRET_KEY` with:
> `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 4. Run migrations

```powershell
python manage.py migrate
```

### 5. Start the development server

```powershell
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. Create an account at `/accounts/signup/`, or create an admin with:

```powershell
python manage.py createsuperuser
```

(Superusers are automatically assigned the ADMIN role.)

---

## Database configuration

`lupadfinds/settings.py` reads `DB_ENGINE` from `.env`:

| `DB_ENGINE` | Database used |
|---|---|
| `sqlite` (default) | Local `db.sqlite3` file — no external setup required |
| `postgresql` (or any other value) | PostgreSQL using the `DB_*` variables, e.g. Supabase |

To switch to Supabase later, set `DB_ENGINE=postgresql` and fill in the `DB_*` variables. Make sure a working PostgreSQL driver is available. On Windows, if you see
`DLL load failed while importing pq: An Application Control policy has blocked this file`, the `psycopg` binary DLL is being blocked by a machine security policy (WDAC/AppLocker/SmartScreen); the pure-Python fallback requires a system `libpq` installation. SQLite avoids this entirely for local development.

---

## Project structure

```
lupadfinds/          Project settings, URLs, WSGI/ASGI
accounts/            Signup, login, logout, profile, custom user model
dashboard/           Role-based dashboards (student / staff / admin)
items/               Lost-item reports: models, forms, views, URLs, migrations
templates/           HTML templates grouped by app
static/css/          Stylesheets
requirements.txt     Python dependencies
.env                 Local secrets and database config (gitignored)
db.sqlite3           Local development database
manage.py            Django management entry point
```

### Main routes

| URL | Description |
|---|---|
| `/` | Redirects logged-in users to their role dashboard |
| `/accounts/signup/` | Register |
| `/accounts/login/` / `/accounts/logout/` | Authentication |
| `/accounts/profile/` / `/accounts/profile/edit/` | Profile |
| `/dashboard/student/` / `/dashboard/staff/` / `/dashboard/admin/` | Role dashboards |
| `/reports/lost/` | List lost reports |
| `/reports/lost/new/` | Create a lost report |
| `/reports/lost/<pk>/` | Report detail |
| `/reports/lost/<pk>/edit/` / `/reports/lost/<pk>/delete/` | Update / delete |
| `/admin/` | Django admin site |

---

## Testing

```powershell
python manage.py test
```

`python manage.py check` validates settings, URLs, and models without touching the database.

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `No module named 'django'` | Dependencies not installed in the active virtual environment | `python -m pip install -r requirements.txt` |
| `Error loading psycopg2 or psycopg module` | PostgreSQL backend selected but no usable driver (blocked DLL / missing libpq / missing psycopg2) | Use `DB_ENGINE=sqlite` locally, or install and allow a working PostgreSQL driver |
| `module 'items.views' has no attribute 'LostReportListView'` | `items/views.py` did not define the views referenced in `items/urls.py` | Ensure all five `LostReport*` class-based views are defined in `items/views.py` |
