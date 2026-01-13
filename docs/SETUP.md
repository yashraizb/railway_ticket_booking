# 🚀 Installation & Setup

[← Back to Main README](../README.md)

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/railway_ticket_booking.git
cd railway_ticket_booking
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Seed Database (Optional)

```bash
python manage.py shell < scripts/populate.py
```

Or run the populate script:
```bash
python manage.py runscript populate
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

---

## Environment Configuration

### Development Settings

The project uses SQLite by default for development. No additional configuration needed.

### Production Settings (Optional)

For PostgreSQL in production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway_booking',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Project Dependencies

```
# requirements.txt
Django>=4.0
djangorestframework>=3.14
djangorestframework-simplejwt>=5.0
```

---

## API Testing

### Using cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","first_name":"Test","last_name":"User"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

**Search Trains:**
```bash
curl "http://localhost:8000/api/booking/trains/search/?source=Delhi&destination=Mumbai&journey_date=2026-01-20&coach_type=3A"
```

**Book Seats (with token):**
```bash
curl -X POST http://localhost:8000/api/booking/book/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "train_number": 12301,
    "source": "Delhi",
    "destination": "Mumbai",
    "journey_date": "2026-01-20",
    "coach_type": "3A",
    "passengers": [{"name":"John Doe","age":30,"gender":"M"}]
  }'
```

### Using Postman

1. Import the API endpoints
2. Set base URL: `http://localhost:8000/api/`
3. For authenticated requests, add header: `Authorization: Bearer <token>`

---

## Admin Interface

Access Django Admin at `http://localhost:8000/admin/`

Features available:
- View/Edit Trains
- View/Edit Stations and Routes
- View/Edit Bookings
- View/Edit Invoices and Refunds
- Manage Users

---

## Troubleshooting

### Common Issues

**1. Migration errors:**
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

**2. Database reset:**
```bash
# Delete db.sqlite3 and migrations (except __init__.py)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**3. Port already in use:**
```bash
python manage.py runserver 8001
```

**4. Token expired:**
- Use the refresh token endpoint to get a new access token
- Or login again to get new tokens

---

## Development Workflow

```bash
# Start development server
python manage.py runserver

# Run migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Run tests
python manage.py test
```

---

[← Back to Main README](../README.md)
