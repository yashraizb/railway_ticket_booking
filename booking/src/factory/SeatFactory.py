from booking.src.strategy.seat.SimpleSeat import SimpleSeat


class SeatFactory:
    def __init__(self):
        self.map = {
            "simple": SimpleSeat
        }
    

    def get_seat_strategy(self, seat_type):
        return self.map[seat_type]()