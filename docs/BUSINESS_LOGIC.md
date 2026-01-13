# 💡 Business Logic Highlights

[← Back to Main README](../README.md)

## Seat Booking Algorithm

The system uses a **segment-based availability** algorithm that maximizes seat utilization.

### How It Works

```
Train Route: A → B → C → D → E
             (1)  (2)  (3)  (4)  (sequence numbers)

Seat #15 availability:
┌─────────────────────────────────────────────┐
│  Segment:    A→B    B→C    C→D    D→E      │
│  Booked:     ✅      ✅      ❌      ❌       │
│              (Passenger 1: A→C)             │
└─────────────────────────────────────────────┘

Passenger 2 wants C→E: ✅ ALLOWED (different segments)
Passenger 3 wants A→D: ❌ DENIED (overlapping segments)
```

### Implementation

```python
# booking/src/strategy/book_seat/MultipleSeats.py
available_seats = (
    list_seats.values("coach__coach_type", "coach_number", "seat_number")
    .annotate(cnt=Count("id"))
    .filter(cnt=(dest_stn.sequence - src_stn.sequence))
)
```

The query counts available segment records for each seat. If a seat has all required segments available, it's bookable.

### Concurrent Booking Safety

```python
with transaction.atomic():
    Seat.objects.select_for_update().filter(
        Q(destination_station_sequence__gt=src_stn.sequence)
        & Q(destination_station_sequence__lte=dest_stn.sequence),
        train=train,
        journey_date=journey_date,
        seat_number__in=seat_numbers,
    ).update(status="booked")
```

- `select_for_update()` acquires row-level locks
- Prevents race conditions when multiple users book simultaneously
- Transaction ensures atomicity

---

## Refund Calculation

Dynamic refund policy based on days remaining before journey.

### Policy Table

| Days Before Journey | Refund Percentage | Strategy Class |
|---------------------|-------------------|----------------|
| > 7 days | 100% | `FullRefund` |
| 3-7 days | 50% | `HalfRefund` |
| 1-3 days | 25% | `QtrRefund` |
| < 1 day | 0% | No refund |

### Implementation

```python
# booking/src/service/RefundService.py
def amountCalculate(self, amount, journey_date):
    diff = journey_date - datetime.now().date()
    factory = CalculationFactory()
    
    if timedelta(days=7) < diff:
        return factory.get_refund_strategy("full").calculate_refund(amount)
    elif timedelta(days=3) < diff:
        return factory.get_refund_strategy("half").calculate_refund(amount)
    elif timedelta(days=1) < diff:
        return factory.get_refund_strategy("qtr").calculate_refund(amount)
    else:
        return 0
```

### Adding New Refund Policy

To add a new policy (e.g., 75% refund):

1. Create strategy class:
```python
# booking/src/strategy/refund/ThreeQuarterRefund.py
class ThreeQuarterRefund(CalculationStrategy):
    def calculate_refund(self, amount):
        return amount * 0.75
```

2. Register in factory:
```python
# booking/src/factory/CalculationFactory.py
self.map["three_quarter"] = ThreeQuarterRefund
```

3. Use in service - no changes needed to existing code!

---

## Transaction Management

### Booking Flow with Rollback

```python
# booking/src/facade/BookingFacade.py
def execute(self):
    # Each step is added to a stack for potential rollback
    seatService.book_seat(...)
    self.stepsStack.append(seatService)
    
    bookingInvoiceCmd.create(...)
    self.stepsStack.append(bookingInvoiceCmd)
    
    ticketService.save_ticket()
    self.stepsStack.append(ticketService)
    
    invoiceService.generate(...)
    self.stepsStack.append(invoiceService)

def rollback(self):
    # Rollback in reverse order (LIFO)
    while self.stepsStack:
        step = self.stepsStack.pop()
        step.rollback()
```

### Cancellation Flow with Transaction

```python
# booking/src/facade/CancelFacade.py
def execute(self):
    lastProcess = "Initialization"
    refund = None
    
    try:
        # Create refund OUTSIDE transaction (persists on failure)
        refundService.initiateRefund(self)
        refund = self.refund
        
        # All cancellation inside transaction
        with transaction.atomic():
            invoiceService.cancelInvoice(...)     # Step 1
            ticketService.cancelTickets()         # Step 2
            seatService.freeSeats(...)            # Step 3
            booking.status = "Cancelled"          # Step 4
            booking.save()
        
        # Update refund status after success
        refund.status = "Requested"
        refund.save()
        
    except Exception as e:
        # Refund record exists - update with failure state
        if refund:
            refund.status = "Halted"
            refund.last_process = lastProcess
            refund.save()
        raise
```

### Why This Design?

1. **Refund record persists** even if transaction fails
2. **Failure tracking** - know exactly which step failed
3. **Transaction rollback** - partial state is never saved
4. **Audit trail** - refund with "Halted" status indicates failed attempt

---

## Error Handling

### Custom Exception with HTTP Code Mapping

```python
# booking/src/domain/CustomException.py
class CustomException(Exception):
    def __init__(self, message, name="CustomException"):
        self.message = message
        self.name = name
        self.code = self.codeResolver()
    
    def codeResolver(self):
        mapping = {
            "STATION_NOT_FOUND": 400,
            "TRAIN_NOT_FOUND": 400,
            "NO_SEATS_AVAILABLE": 409,
            "NOT_ENOUGH_SEATS": 409,
            "UNAUTHORIZED_CANCELLATION": 403,
            "CANCELLATION_FAILED": 500,
        }
        return mapping.get(self.name, 500)
```

### Usage in Views

```python
# booking/views.py
try:
    bookingFacade.execute()
except CustomException as ce:
    bookingFacade.rollback()
    return JsonResponse(ce.getErrorJson(), status=ce.code)
```

---

## Pricing Calculation

```python
# booking/src/service/InvoiceService.py
amount = (
    trip.rate_per_km                              # ₹/km rate
    * (dest_route.distance_from_source            # Destination distance
       - src_route.distance_from_source)          # Source distance
    * len(passengers)                             # Number of passengers
)
```

Example:
- Rate: ₹2.50/km
- Source distance from origin: 100 km
- Destination distance from origin: 500 km
- Passengers: 2
- **Total**: ₹2.50 × (500 - 100) × 2 = **₹2,000**

---

[← Back to Main README](../README.md)
