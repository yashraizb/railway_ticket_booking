from booking.models import BookingToInvoice


class JourneyDetailHandler:
    def __init__(self):
        self.src_station = None
        self.dest_station = None
        self.journey_date = None
        self.train = None
        self.trip = None
        self.booking = None
    
    def set_src_station(self, src_station):
        self.src_station = src_station
    
    def set_dest_station(self, dest_station):
        self.dest_station = dest_station
    
    def set_journey_date(self, journey_date):
        self.journey_date = journey_date
    
    def set_train(self, train):
        self.train = train
    
    def get_src_station(self):
        return self.src_station
    
    def get_dest_station(self):
        return self.dest_station
    
    def get_journey_date(self):
        return self.journey_date
    
    def get_train(self):
        return self.train

    def get_trip(self):
        return self.trip

    def set_trip(self, trip):
        self.trip = trip
    
    def get_booking(self) -> BookingToInvoice:
        return self.booking

    def set_booking(self, booking):
        self.booking = booking