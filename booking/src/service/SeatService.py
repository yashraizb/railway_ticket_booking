from booking.src.strategy.seat.SeatStrategy import SeatStrategy
from booking.src.factory.SeatFactory import SeatFactory
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler
from booking.models import Seat, Train, Station, RouteStation
from django.db.models import Q, Count
from django.db import transaction


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
    
    def book_seat(self, bookSerializer):
        train_number = bookSerializer.validated_data["train_number"]
        source_name = bookSerializer.validated_data["source"]
        destination_name = bookSerializer.validated_data["destination"]
        journey_date = bookSerializer.validated_data["journey_date"]
        coach_type = bookSerializer.validated_data["coach_type"]

        try:
            train = Train.objects.get(number=train_number)
            source = Station.objects.get(name=source_name)
            destination = Station.objects.get(name=destination_name)
        except Train.DoesNotExist:
            raise Exception("Train not found")
        except Station.DoesNotExist:
            raise Exception("Station not found")

        src_stn_seq = (
            RouteStation.objects.filter(train=train, station=source).first().sequence
        )

        dest_stn_seq = (
            RouteStation.objects.filter(train=train, station=destination)
            .first()
            .sequence
        )

        list_seats = Seat.objects.filter(
            Q(destination_station_sequence__gt=src_stn_seq)
            & Q(destination_station_sequence__lte=dest_stn_seq),
            train=train,
            journey_date=journey_date,
            coach__coach_type=coach_type,
            status="available",
        )

        available_seats = (
            list_seats.values("coach__coach_type", "coach_number", "seat_number")
            .annotate(cnt=Count("id"))
            .filter(cnt=(dest_stn_seq - src_stn_seq))
        )

        if not available_seats.exists():
            raise Exception("No available seats")

        seat_number = list_seats.first().seat_number

        with transaction.atomic():

            Seat.objects.select_for_update().filter(
                Q(destination_station_sequence__gt=src_stn_seq)
                & Q(destination_station_sequence__lte=dest_stn_seq),
                train=train,
                journey_date=journey_date,
                coach__coach_type=coach_type,
                status="available",
                seat_number=seat_number,
            ).update(status="booked")
        
        return seat_number