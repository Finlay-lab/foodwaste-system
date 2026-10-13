# Food Waste Prediction and Management System

Helps restaurants predict demand and reduce leftover food.

## Stack

- Python 3.11 (use 3.12 locally if 3.11 is not installed)
- Django 5.x
- Django REST Framework
- PostgreSQL 16.x
- Bootstrap 5

## Setup

1. Install Python 3.11+ and PostgreSQL 16. Create a database named `foodwaste`.
2. Copy `.env.example` to `.env` and set `DJANGO_SECRET_KEY` and `DB_PASSWORD`. Do not commit `.env`.
3. Create a virtual environment and install dependencies:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Run:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test
```

`createsuperuser` prompts for email, full name, and password. The account is stored as a System Administrator.

5. Open http://127.0.0.1:8000/

## Project layout

- `config/` — Django settings and URLs
- `apps/core/` — home and health
- `apps/accounts/` — users, login, signup, roles
- `apps/dashboard/` — role dashboards
- `apps/business/` — business profiles
- `apps/inventory/` — food categories
- `apps/forecasting`, `recommendations`, `notifications` — later features
