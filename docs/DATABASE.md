# 🗄️ Database Schema

[← Back to Main README](../README.md)

## Entity Relationship Overview

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  CustomUser  │───────│   Booking    │───────│    Ticket    │
└──────────────┘  1:N  └──────────────┘  1:N  └──────────────┘
                              │
                              │ 1:1
                              ▼
                       ┌──────────────┐       ┌──────────────┐
                       │   Invoice    │───────│    Refund    │
                       └──────────────┘  1:N  └──────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    Train     │───────│ RouteStation │───────│   Station    │
└──────────────┘  1:N  └──────────────┘  N:1  └──────────────┘
       │
       │ 1:N
       ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│     Trip     │       │     Seat     │───────│    Coach     │
└──────────────┘       └──────────────┘  N:1  └──────────────┘
```

---

## Models Description

| Model | Purpose | Key Fields |
|-------|---------|------------|
| **Train** | Train information | `name`, `number` |
| **Station** | Railway stations | `name`, `code` |
| **RouteStation** | Train route with sequence | `train`, `station`, `sequence`, `distance_from_source` |
| **Trip** | Train schedule per date | `train`, `journey_date`, `rate_per_km` |
| **Coach** | Coach types | `coach_type` (SL, 3A, 2A, 1A, CC), `coach_name` |
| **Seat** | Seat inventory | `seat_number`, `coach`, `train`, `journey_date`, `status`, `destination_station_sequence` |
| **Booking** | User reservations | `booking_id` (PNR), `user`, `train`, `source_station`, `destination_station`, `journey_date`, `status` |
| **Ticket** | Individual passenger tickets | `booking_id`, `seat_number`, `passenger_name`, `passenger_age`, `status` |
| **Invoice** | Payment records | `invoice_id`, `booking_id`, `amount`, `status` |
| **Refund** | Refund requests | `refund_id`, `invoice`, `booking`, `amount`, `approved_amount`, `status`, `last_process` |

---

## Status Enums

### Booking Status
```python
class Booking.StatusChoices:
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    WAITING = "Waiting"
    PARTIAL_CONFIRMED = "PartialConfirmed"
    PARTIAL_CANCELLED = "PartialCancelled"
```

### Refund Status
```python
class Refund.StatusChoices:
    PENDING = "Pending"
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    HALTED = "Halted"  # When cancellation fails mid-process
```

### Seat Status
```python
class Seat.StatusChoices:
    AVAILABLE = "available"
    BOOKED = "booked"
```

### Invoice Status
```python
class Invoice.StatusChoices:
    PAID = "Paid"
    CANCELLED = "Cancelled"
```

### Ticket Status
```python
class Ticket.StatusChoices:
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    WAITING = "Waiting"
```

### Coach Types
```python
class Coach.CoachType:
    SL = "SL"   # Sleeper
    A3 = "3A"   # AC 3 Tier
    A2 = "2A"   # AC 2 Tier
    FC = "1A"   # First Class
    CC = "CC"   # Chair Car
```

---

## Key Relationships

### User → Booking (1:N)
```python
user = models.ForeignKey(
    'accounts.CustomUser', 
    on_delete=models.CASCADE, 
    related_name="bookings"
)
```

### Booking → Ticket (1:N)
- Linked by `booking_id` field in Ticket model
- Multiple passengers per booking

### Booking → Invoice (1:1)
- One invoice per booking
- Linked by `booking_id` field

### Invoice → Refund (1:N)
```python
invoice = models.ForeignKey(
    Invoice, 
    on_delete=models.CASCADE, 
    related_name="refunds"
)
```

### Train → RouteStation → Station
- Many-to-many through RouteStation
- Includes sequence and distance

### Seat Unique Constraint
```python
class Meta:
    unique_together = (
        "seat_number", 
        "coach", 
        "journey_date", 
        "train", 
        "destination_station_sequence"
    )
```

---

## Segment-Based Seat Availability

The `destination_station_sequence` field enables **segment-based booking**:

```
Station A (seq=1) → B (seq=2) → C (seq=3) → D (seq=4)

Passenger 1: A → C (uses segments 1-2, 2-3)
Passenger 2: C → D (uses segment 3-4)

Same seat can be booked by both passengers!
```

This allows maximum seat utilization by tracking which segments are booked rather than marking the entire journey as unavailable.

---

[← Back to Main README](../README.md)
