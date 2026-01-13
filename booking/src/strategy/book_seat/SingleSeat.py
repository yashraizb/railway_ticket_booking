from .BookingStrategy import BookingStrategy
from django.db import transaction
from django.db.models import Q, Count
from booking.serializer import BookSeatSerializer
from booking.models import Seat, Train, Station, RouteStation
from booking.src.domain.CustomException import CustomException
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler


class SingleSeat(BookingStrategy):
    def book(self, bookSerializer: BookSeatSerializer, journeyDetails: JourneyDetailHandler):
        train_number = bookSerializer.validated_data["train_number"]
        source_name = bookSerializer.validated_data["source"]
        destination_name = bookSerializer.validated_data["destination"]
        journey_date = bookSerializer.validated_data["journey_date"]
        coach_type = bookSerializer.validated_data["coach_type"]
        passenger_count = len(bookSerializer.validated_data["passengers"])

        if passenger_count != 1:
            raise CustomException("Passenger count must be 1", "INVALID_PASSENGER_COUNT")

        try:
            train = Train.objects.get(number=train_number)
            source = Station.objects.get(name=source_name)
            destination = Station.objects.get(name=destination_name)
        except Train.DoesNotExist:
            raise CustomException("Train not found", "TRAIN_NOT_FOUND")
        except Station.DoesNotExist:
            raise CustomException("Station not found", "STATION_NOT_FOUND")

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
            raise CustomException("No available seats", "NO_SEATS_AVAILABLE")

        seat_number = list_seats.first().seat_number

        with transaction.atomic():

            Seat.objects.select_for_update().filter(
                Q(destination_station_sequence__gt=src_stn.sequence)
                & Q(destination_station_sequence__lte=dest_stn.sequence),
                train=train,
                journey_date=journey_date,
                coach__coach_type=coach_type,
                status="available",
                seat_number=seat_number,
            ).update(status="booked")
        
        journeyDetails.seat_numbers = [seat_number]
        
        return [seat_number]
    
    def rollback(self, bookSerializer: BookSeatSerializer, journeyDetails: JourneyDetailHandler):
        with transaction.atomic():
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
                raise CustomException("Train not found", "TRAIN_NOT_FOUND")
            except Station.DoesNotExist:
                raise CustomException("Station not found", "STATION_NOT_FOUND")

            src_stn = (
                RouteStation.objects.filter(train=train, station=source).first()
            )
            dest_stn = (
                RouteStation.objects.filter(train=train, station=destination).first()
            )

            Seat.objects.select_for_update().filter(
                Q(destination_station_sequence__gt=src_stn.sequence)
                & Q(destination_station_sequence__lte=dest_stn.sequence),
                train=train,
                journey_date=journey_date,
                coach__coach_type=coach_type,
                status="booked",
                seat_number__in=journeyDetails.seat_numbers,
            ).update(status="available")