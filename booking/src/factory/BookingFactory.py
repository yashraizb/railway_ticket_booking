from booking.src.strategy.book_seat.SingleSeat import SingleSeat
from booking.src.strategy.book_seat.MultipleSeats import MultipleSeats


class BookingFactory:

    def __init__(self):
        self.map = {
            "single": SingleSeat,
            "multiple": MultipleSeats
        }
    
    def get_booking_strategy(self, strategy):
        return self.map[strategy]()