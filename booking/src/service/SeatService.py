from booking.src.strategy.seat.SeatStrategy import SeatStrategy
from booking.src.factory.SeatFactory import SeatFactory
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler
from booking.models import Seat, Train, Station, RouteStation
from django.db.models import Q, Count
from django.db import transaction
from booking.src.strategy.book_seat.BookingStrategy import BookingStrategy
from booking.src.strategy.book_seat.SingleSeat import SingleSeat
from booking.src.factory.BookingFactory import BookingFactory
from booking.serializer import BookSeatSerializer


SEAT_STRATEGY = "simple"
BOOKING_STRATEGY = "multiple"


class SeatService:
    def __init__(self):
        self.bookSerializer = None
        self.journeyDetails = None
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
    
    def book_seat(self, bookSerializer: BookSeatSerializer, journeyDetails: JourneyDetailHandler):
        bookingFactory = BookingFactory()
        bookingStrategy: BookingStrategy = bookingFactory.get_booking_strategy(BOOKING_STRATEGY)
        self.bookSerializer = bookSerializer
        self.journeyDetails = journeyDetails
        return bookingStrategy.book(bookSerializer, journeyDetails)
    
    def rollback(self):
        print("Rolling back: SeatService")
        bookingFactory = BookingFactory()
        bookingStrategy: BookingStrategy = bookingFactory.get_booking_strategy(BOOKING_STRATEGY)
        bookingStrategy.rollback(self.bookSerializer, self.journeyDetails)
    
    def freeSeats(self, facade):
        seat_numbers = [s.seat_number for s in facade.tickets]
        Seat.objects.filter(
            train=facade.booking.train,
            journey_date=facade.booking.journey_date,
            seat_number__in=seat_numbers,
            destination_station_sequence__gt=facade.src_stn.sequence,
            destination_station_sequence__lte=facade.dest_stn.sequence
        ).update(status=Seat.StatusChoices.AVAILABLE)
        