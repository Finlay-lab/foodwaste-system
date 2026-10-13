# Food Waste Prediction and Management System

Final-year project: predict demand, detect surplus, and support food-waste reduction for food businesses.

## Stack

- Python 3.11 (use 3.12 locally if 3.11 is not installed)
- Django 5.x
- Django REST Framework
- PostgreSQL 16.x
- Bootstrap 5

## Phase 1

Project foundation: settings, modular apps, home page.

## Phase 2

User authentication and RBAC. Custom `users` table (UUID, `password_hash`, role CHECK). Email/password login, logout, signup for Restaurant Manager and Inventory Staff, and System Administrator user-account management. Role-specific dashboard shells only.

## Phase 3

Business profiles. Restaurant Managers register and update one profile (`business_name`, `business_type`, `location`, `contact_number`, `registration_date`) linked 1:1 to their user. Administrators can list all businesses.

## Phase 4

Food categories. System Administrators add, edit, and delete global categories (`category_name`, `description`) used later to classify food items. PostgreSQL table: `food_categories`.

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

5. Open:
   - http://127.0.0.1:8000/
   - http://127.0.0.1:8000/accounts/login/
   - http://127.0.0.1:8000/accounts/signup/
   - http://127.0.0.1:8000/admin/
   - http://127.0.0.1:8000/health/

## Project layout

- `config/` — Django project settings and URLs
- `apps/core/` — home and health endpoints
- `apps/accounts/` — custom user, login/logout/signup, RBAC, manage user accounts
- `apps/dashboard/` — role-specific dashboard shells (placeholder content)
- `apps/business` — business profiles
- `apps/inventory` — food categories (food items in a later phase)
- `apps/forecasting`, `recommendations`, `notifications` — reserved for later phases
