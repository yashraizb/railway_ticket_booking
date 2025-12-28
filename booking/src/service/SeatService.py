from booking.src.strategy.seat.SeatStrategy import SeatStrategy
from booking.src.factory.SeatFactory import SeatFactory
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler


SEAT_STRATEGY = "simple"


class SeatService:
    def __init__(self):
        self.seatStrategy: SeatStrategy = None
        self.seatFactory: SeatFactory = SeatFactory()
    
    def set_seat_strategy(self, strategy):
        self.seatStrategy = self.seatFactory.get_seat_strategy(strategy)
    
    def get_seats(self, journeyDetails: JourneyDetailHandler):
        self.set_seat_strategy(SEAT_STRATEGY)
        data = {
            "source": journeyDetails.get_src_station(),
            "destination": journeyDetails.get_dest_station(),
            "journey_date": journeyDetails.get_journey_date(),
            "train": journeyDetails.get_train(),
        }
        return self.seatStrategy.get_available_seats(data)