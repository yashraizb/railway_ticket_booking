from booking.src.strategy.seat.SeatStrategy import SeatStrategy
from booking.src.factory.SeatFactory import SeatFactory
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler
from booking.models import Seat, Train, Station, RouteStation
from django.db.models import Q, Count
from django.db import transaction
from booking.src.strategy.book_seat.BookingStrategy import BookingStrategy
from booking.src.strategy.book_seat.SingleSeat import SingleSeat
from booking.src.factory.BookingFactory import BookingFactory


SEAT_STRATEGY = "simple"
BOOKING_STRATEGY = "multiple"


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
    
    def book_seat(self, bookSerializer, journeyDetails: JourneyDetailHandler):
        bookingFactory = BookingFactory()
        bookingStrategy: BookingStrategy = bookingFactory.get_booking_strategy(BOOKING_STRATEGY)
        return bookingStrategy.book(bookSerializer, journeyDetails)