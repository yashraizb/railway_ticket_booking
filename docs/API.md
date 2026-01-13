# 🔌 API Endpoints

[← Back to Main README](../README.md)

## Base URL
```
http://localhost:8000/api/
```

---

## Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register/` | Register new user | ❌ |
| POST | `/auth/login/` | Login and get JWT tokens | ❌ |
| POST | `/auth/token/refresh/` | Refresh access token | ❌ |

### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response (201):**
```json
{
    "message": "Registration successful",
    "user_id": 1
}
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "message": "Login successful"
}
```

---

## Booking Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/booking/health/` | Health check | ❌ |
| GET | `/booking/trains/` | List all trains | ❌ |
| GET | `/booking/trains/search/` | Search trains with availability | ❌ |
| POST | `/booking/book/` | Book seats | ✅ |
| DELETE | `/booking/cancel/` | Cancel booking | ✅ |

### Search Trains
```http
GET /api/booking/trains/search/?source=Delhi&destination=Mumbai&journey_date=2026-01-20&coach_type=3A
```

**Response (200):**
```json
{
    "trains": [
        {
            "name": "Rajdhani Express",
            "number": 12301,
            "available_seats": 45
        },
        {
            "name": "Duronto Express",
            "number": 12213,
            "available_seats": 32
        }
    ]
}
```

### Book Seats
```http
POST /api/booking/book/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "train_number": 12301,
    "source": "Delhi",
    "destination": "Mumbai",
    "journey_date": "2026-01-20",
    "coach_type": "3A",
    "passengers": [
        {
            "name": "John Doe",
            "age": 30,
            "gender": "M"
        },
        {
            "name": "Jane Doe",
            "age": 28,
            "gender": "F"
        }
    ]
}
```

**Response (200):**
```json
{
    "message": "Seat booked successfully",
    "pnr": 1001,
    "seat_number": [15, 16],
    "coach_type": "3A",
    "train_number": 12301,
    "source": "Delhi",
    "destination": "Mumbai"
}
```

### Cancel Booking
```http
DELETE /api/booking/cancel/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "pnr": 1001,
    "passengers": [
        {"name": "John Doe"}
    ]
}
```

**Response (200):**
```json
{
    "message": "Booking cancelled successfully"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "errors": {
        "field_name": ["Error message"]
    },
    "message": "Invalid request"
}
```

### 401 Unauthorized
```json
{
    "message": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
    "message": "Unauthorized to cancel this booking",
    "name": "UNAUTHORIZED_CANCELLATION"
}
```

### 404 Not Found
```json
{
    "message": "Train not found",
    "name": "TRAIN_NOT_FOUND"
}
```

### 409 Conflict
```json
{
    "message": "No available seats for the requested train, date and coach",
    "name": "NO_SEATS_AVAILABLE"
}
```

### 500 Internal Server Error
```json
{
    "message": "Cancellation failed after step: Ticket Cancellation with error: ...",
    "name": "CANCELLATION_FAILED"
}
```

---

## Authentication Header

For protected endpoints, include the JWT token:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

[← Back to Main README](../README.md)
