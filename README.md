# Online Bookstore - Django

A complete Django-based online bookstore: browse by category, detailed book pages, session-based shopping cart, checkout with order confirmation, order management, and a Django admin panel for inventory.

## Demo

_Add screenshots of the storefront, cart and admin panel here._

## Features

- Browse books by category
- Detailed book pages
- Session-based shopping cart (no account needed to add items)
- Checkout with order placement and confirmation page
- Order management
- Admin panel for book/inventory management
- Responsive templates (base, home, book detail, cart, place order, confirmation)

## Tech stack

- **Backend:** Python 3.x, Django
- **Database:** SQLite by default (zero setup); MySQL supported via a commented-out config block in `bookstore_project/settings.py`
- **Frontend:** Django templates, HTML5, CSS3
- **ORM:** Django ORM (`books`, `cart`, `orders` apps)

## Setup

### Prerequisites

- Python 3.x

### Quick start (SQLite, no database server needed)

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   # venv\Scripts\activate     # Windows
   ```

2. Install Django:

   ```bash
   pip install django
   ```

3. Migrate, create an admin user, and run:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. Visit `http://127.0.0.1:8000` (admin at `/admin`).

### MySQL option

`setup.sh` automates the MySQL path: it checks for MySQL, creates the `bookstore_db` database, runs migrations, prompts for a superuser, and starts the server. To use MySQL, open `bookstore_project/settings.py`, comment out the SQLite `DATABASES` block, uncomment the MySQL block, set your password, then run `./setup.sh`.

## Project layout

```text
book_store/
├── bookstore_project/   # Django project settings, root URLs
├── books/               # Catalog: Category + Book models, views
├── cart/                # Session cart
├── orders/              # Checkout forms, order models
├── templates/           # base, home, book detail, cart, checkout, confirmation
└── static/css/          # Styling
```

## What this demonstrates

Classic backend engineering: relational schema design, Django ORM across multiple apps, session-based cart state, an order flow with forms, and the built-in admin - the CRUD fundamentals most entry-level backend roles test for.
