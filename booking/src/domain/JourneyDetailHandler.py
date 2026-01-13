from booking.models import Booking, Station, RouteStation, Train, Trip


class JourneyDetailHandler:
    def __init__(self):
        self.src_station = None
        self.dest_station = None
        self.journey_date = None
        self.train = None
        self.trip = None
        self.bookingToInvoice = None
        self.src_route_station = None
        self.dest_route_station = None

    def set_src_route_station(self, src_route_station: RouteStation):
        self.src_route_station = src_route_station

    def set_dest_route_station(self, dest_route_station: RouteStation):
        self.dest_route_station = dest_route_station

    def get_src_route_station(self) -> RouteStation:
        return self.src_route_station

    def get_dest_route_station(self) -> RouteStation:
        return self.dest_route_station

    def set_src_station(self, src_station: Station):
        self.src_station = src_station

    def set_dest_station(self, dest_station: Station):
        self.dest_station = dest_station

    def set_journey_date(self, journey_date):
        self.journey_date = journey_date

    def set_train(self, train: Train):
        self.train = train

    def get_src_station(self) -> Station:
        return self.src_station

    def get_dest_station(self) -> Station:
        return self.dest_station

    def get_journey_date(self):
        return self.journey_date

    def get_train(self) -> Train:
        return self.train

    def get_trip(self) -> Trip:
        return self.trip

    def set_trip(self, trip: Trip):
        self.trip = trip

    def get_booking(self) -> Booking:
        return self.bookingToInvoice

    def set_booking(self, booking):
        self.bookingToInvoice = booking
