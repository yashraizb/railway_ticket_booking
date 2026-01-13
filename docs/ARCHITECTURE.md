# 🏗️ Architecture & Design Patterns

[← Back to Main README](../README.md)

This project implements **5+ Gang of Four (GoF) design patterns** to achieve maintainable, extensible, and testable code. Each pattern solves a specific architectural challenge.

---

## 1. Facade Pattern

**Purpose:** Simplify complex subsystem interactions by providing a unified interface.

**Implementation:** `BookingFacade` and `CancelFacade`

```python
# booking/src/facade/BookingFacade.py
class BookingFacade:
    def execute(self):
        # Orchestrates multiple services in sequence
        seatService.book_seat(...)      # Step 1
        bookingInvoiceCmd.create(...)   # Step 2
        ticketService.save_ticket()     # Step 3
        invoiceService.generate(...)    # Step 4
```

**Benefits:**
- Controllers remain thin - single method call handles entire booking
- Easy to add/remove steps without changing API layer
- Centralized rollback logic on failures

---

## 2. Strategy Pattern

**Purpose:** Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Implementations:**
- **Refund Calculation:** `FullRefund`, `HalfRefund`, `QtrRefund`
- **Seat Booking:** `SingleSeat`, `MultipleSeats`
- **Seat Availability:** `SimpleSeat`

```python
# booking/src/strategy/refund/CalculationStrategy.py
class CalculationStrategy(ABC):
    @abstractmethod
    def calculate_refund(self, amount):
        pass

# booking/src/strategy/refund/FullRefund.py
class FullRefund(CalculationStrategy):
    def calculate_refund(self, amount):
        return amount  # 100% refund

# booking/src/strategy/refund/HalfRefund.py
class HalfRefund(CalculationStrategy):
    def calculate_refund(self, amount):
        return amount / 2  # 50% refund
```

**Benefits:**
- Adding new refund policies requires only a new class
- Open/Closed Principle - open for extension, closed for modification
- Runtime algorithm selection based on business rules

---

## 3. Factory Pattern

**Purpose:** Create objects without specifying the exact class, delegating instantiation to factory classes.

**Implementations:** `CalculationFactory`, `BookingFactory`, `SeatFactory`

```python
# booking/src/factory/CalculationFactory.py
class CalculationFactory:
    def __init__(self):
        self.map = {
            "full": FullRefund,
            "half": HalfRefund,
            "qtr": QtrRefund,
        }
    
    def get_refund_strategy(self, strategy):
        if strategy not in self.map:
            raise ValueError(f"Unknown strategy: {strategy}")
        return self.map[strategy]()
```

**Benefits:**
- Decouples client code from concrete implementations
- Single point of change for strategy instantiation
- Easy to add new strategies without modifying client code

---

## 4. Command Pattern

**Purpose:** Encapsulate a request as an object, allowing parameterization and queuing of requests.

**Implementation:** `BookingInvoiceCmd`

```python
# booking/src/command/BookingInvoiceCmd.py
class BookingInvoiceCmd:
    def createBookingToInvoice(self, facade):
        # Encapsulates booking creation logic
        self.bookingToInvoice = Booking.objects.create(...)
    
    def rollback(self):
        # Undo operation
        self.bookingToInvoice.delete()
```

**Benefits:**
- Operations can be undone (rollback support)
- Commands can be stored in a stack for sequential rollback
- Separates the invoker from the executor

---

## 5. Service Layer Pattern

**Purpose:** Define application's boundary with a layer of services that establishes available operations.

**Implementations:** `SeatService`, `TicketService`, `InvoiceService`, `RefundService`, `TrainService`

```python
# booking/src/service/RefundService.py
class RefundService:
    def amountCalculate(self, amount, journey_date):
        # Business logic for refund calculation
        diff = journey_date - datetime.now().date()
        factory = CalculationFactory()
        if timedelta(days=7) < diff:
            return factory.get_refund_strategy("full").calculate_refund(amount)
        # ... more logic
    
    def initiateRefund(self, facade):
        # Orchestrates refund creation
        amount = self.amountCalculate(...)
        Refund.objects.create(...)
```

**Benefits:**
- Clear separation between API layer and business logic
- Services are reusable across different contexts
- Easier to test business logic in isolation

---

## Design Pattern Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer (Views)                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FACADE PATTERN                                │
│         BookingFacade / CancelFacade                            │
│         (Orchestrates the entire workflow)                       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  SERVICE LAYER  │ │  SERVICE LAYER  │ │  SERVICE LAYER  │
│   SeatService   │ │  TicketService  │ │ InvoiceService  │
└────────┬────────┘ └─────────────────┘ └─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FACTORY PATTERN                               │
│              BookingFactory / SeatFactory                        │
│         (Creates appropriate strategy instances)                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ STRATEGY PATTERN│ │ STRATEGY PATTERN│ │ STRATEGY PATTERN│
│   SingleSeat    │ │  MultipleSeats  │ │   FullRefund    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

[← Back to Main README](../README.md)
