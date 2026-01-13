# 📁 Project Structure

[← Back to Main README](../README.md)

```
railway_ticket_booking/
├── manage.py                          # Django management script
├── README.md                          # Project documentation
│
├── docs/                              # Documentation files
│   ├── ARCHITECTURE.md                # Design patterns documentation
│   ├── PROJECT_STRUCTURE.md           # This file
│   ├── DATABASE.md                    # Database schema
│   ├── API.md                         # API endpoints
│   ├── BUSINESS_LOGIC.md              # Business logic details
│   └── SETUP.md                       # Installation guide
│
├── railway_ticket_booking/            # Project configuration
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py                        # WSGI entry point
│   └── asgi.py                        # ASGI entry point
│
├── accounts/                          # User management app
│   ├── models.py                      # CustomUser model
│   ├── manager.py                     # Custom user manager
│   └── admin.py                       # Admin registration
│
├── authentication/                    # Auth app
│   ├── views.py                       # Login, Register views
│   ├── serializer.py                  # Auth serializers
│   └── urls.py                        # Auth endpoints
│
├── booking/                           # Core booking app
│   ├── models.py                      # Train, Seat, Booking, Ticket, Invoice, Refund
│   ├── views.py                       # API views (Search, Book, Cancel)
│   ├── serializer.py                  # Request/Response serializers
│   ├── urls.py                        # Booking endpoints
│   ├── admin.py                       # Admin registration
│   │
│   └── src/                           # Business logic layer
│       ├── command/                   # Command Pattern
│       │   └── BookingInvoiceCmd.py   # Booking creation command
│       │
│       ├── domain/                    # Domain objects
│       │   ├── CustomException.py     # Custom exception handling
│       │   └── JourneyDetailHandler.py # Journey context handler
│       │
│       ├── facade/                    # Facade Pattern
│       │   ├── BookingFacade.py       # Booking orchestrator
│       │   └── CancelFacade.py        # Cancellation orchestrator
│       │
│       ├── factory/                   # Factory Pattern
│       │   ├── BookingFactory.py      # Booking strategy factory
│       │   ├── CalculationFactory.py  # Refund strategy factory
│       │   └── SeatFactory.py         # Seat strategy factory
│       │
│       ├── service/                   # Service Layer
│       │   ├── SeatService.py         # Seat management
│       │   ├── TicketService.py       # Ticket management
│       │   ├── InvoiceService.py      # Invoice management
│       │   ├── RefundService.py       # Refund management
│       │   └── TrainService.py        # Train search
│       │
│       └── strategy/                  # Strategy Pattern
│           ├── book_seat/             # Booking strategies
│           │   ├── BookingStrategy.py # Abstract strategy
│           │   ├── SingleSeat.py      # Single seat booking
│           │   └── MultipleSeats.py   # Multiple seats booking
│           │
│           ├── refund/                # Refund strategies
│           │   ├── CalculationStrategy.py # Abstract strategy
│           │   ├── FullRefund.py      # 100% refund
│           │   ├── HalfRefund.py      # 50% refund
│           │   └── QtrRefund.py       # 25% refund
│           │
│           └── seat/                  # Seat availability strategies
│               ├── SeatStrategy.py    # Abstract strategy
│               └── SimpleSeat.py      # Simple availability check
│
└── scripts/                           # Utility scripts
    ├── populate.py                    # Database seeding script
    └── railways_data.json             # Sample data
```

---

## Directory Responsibilities

| Directory | Responsibility |
|-----------|----------------|
| `accounts/` | User model with email-based authentication |
| `authentication/` | JWT login/register endpoints |
| `booking/` | Core booking functionality |
| `booking/src/command/` | Encapsulated operations with rollback |
| `booking/src/domain/` | Domain objects and exceptions |
| `booking/src/facade/` | Workflow orchestration |
| `booking/src/factory/` | Strategy instantiation |
| `booking/src/service/` | Business logic layer |
| `booking/src/strategy/` | Interchangeable algorithms |
| `scripts/` | Database seeding utilities |

---

## Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation Layer                      │
│                  (views.py, serializer.py)                  │
├─────────────────────────────────────────────────────────────┤
│                      Application Layer                       │
│                   (facade/, command/)                        │
├─────────────────────────────────────────────────────────────┤
│                       Business Layer                         │
│                (service/, strategy/, factory/)               │
├─────────────────────────────────────────────────────────────┤
│                        Domain Layer                          │
│                    (models.py, domain/)                      │
├─────────────────────────────────────────────────────────────┤
│                    Infrastructure Layer                      │
│                  (Django ORM, Database)                      │
└─────────────────────────────────────────────────────────────┘
```

---

[← Back to Main README](../README.md)
