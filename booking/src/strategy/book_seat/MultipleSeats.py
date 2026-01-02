from .BookingStrategy import BookingStrategy
from django.db import transaction
from django.db.models import Q, Count
from booking.serializer import BookSeatSerializer
from booking.models import Seat, Train, Station, RouteStation
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler


class MultipleSeats(BookingStrategy):
    def book(self, bookSerializer: BookSeatSerializer, journeyDetails: JourneyDetailHandler):
        train_number = bookSerializer.validated_data["train_number"]
        source_name = bookSerializer.validated_data["source"]
        destination_name = bookSerializer.validated_data["destination"]
        journey_date = bookSerializer.validated_data["journey_date"]
        coach_type = bookSerializer.validated_data["coach_type"]
        passenger_count = len(bookSerializer.validated_data["passengers"])

        try:
            train = Train.objects.get(number=train_number)
            source = Station.objects.get(name=source_name)
            destination = Station.objects.get(name=destination_name)
        except Train.DoesNotExist:
            raise Exception("Train not found")
        except Station.DoesNotExist:
            raise Exception("Station not found")

        src_stn = (
            RouteStation.objects.filter(train=train, station=source).first()
        )

        dest_stn = (
            RouteStation.objects.filter(train=train, station=destination)
            .first()   
        )

        journeyDetails.set_journey_date(journey_date)
        journeyDetails.set_src_station(src_stn)
        journeyDetails.set_dest_station(dest_stn)

        list_seats = Seat.objects.filter(
            Q(destination_station_sequence__gt=src_stn.sequence)
            & Q(destination_station_sequence__lte=dest_stn.sequence),
            train=train,
            journey_date=journey_date,
            coach__coach_type=coach_type,
            status="available",
        )

        available_seats = (
            list_seats.values("coach__coach_type", "coach_number", "seat_number")
            .annotate(cnt=Count("id"))
            .filter(cnt=(dest_stn.sequence - src_stn.sequence))
        )

        if not available_seats.exists():
            raise Exception("No available seats")
        
        if available_seats.count() < passenger_count:
            raise Exception("Not enough available seats")

        seat_numbers = []
        for i in range(passenger_count):
            seat_numbers.append(available_seats[i]["seat_number"])

        with transaction.atomic():

            Seat.objects.select_for_update().filter(
                Q(destination_station_sequence__gt=src_stn.sequence)
                & Q(destination_station_sequence__lte=dest_stn.sequence),
                train=train,
                journey_date=journey_date,
                coach__coach_type=coach_type,
                status="available",
                seat_number__in=seat_numbers,
            ).update(status="booked")
        
        for request in bookSerializer.validated_data["passengers"]:
            request["status"] = "assigned"
        
        return seat_numbers