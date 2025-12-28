from django.http import JsonResponse
from django.db.models import Q, Count, F, OuterRef, Subquery, Exists
from django.db import models, transaction
from rest_framework.views import APIView
from .models import Train, RouteStation, Station, Seat
from .serializer import TrainSerializer, SearchTrainSerializer, BookSeatSerializer
from rest_framework.permissions import AllowAny
from .src.service.SeatService import SeatService
from .src.domain.JourneyDetailHandler import JourneyDetailHandler


# Create your views here.
class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "ok"}, status=200)


class ListTrainsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # Logic to list trains would go here
        all_trains = Train.objects.all()
        serializer = TrainSerializer(all_trains, many=True)
        return JsonResponse({"trains": serializer.data}, status=200)


class SearchTrainsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        journey_details = JourneyDetailHandler()
        searchTrainSerializer = SearchTrainSerializer(data=request.query_params)
        if not searchTrainSerializer.is_valid():
            return JsonResponse(
                {"errors": searchTrainSerializer.errors, "message": "Search failed"}, status=400
            )

        source = searchTrainSerializer.validated_data["source"]
        destination = searchTrainSerializer.validated_data["destination"]
        journey_date = searchTrainSerializer.validated_data["journey_date"]
        journey_details.set_journey_date(journey_date)

        try:
            src_station = Station.objects.get(name=source)
            journey_details.set_src_station(src_station)
            dest_station = Station.objects.get(name=destination)
            journey_details.set_dest_station(dest_station)
        except Station.DoesNotExist:
            return JsonResponse({"message": "Station not found"}, status=404)

        trains = (
            Train.objects.filter(
                trips__journey_date=journey_date,  # must run on date
                route_stations__station__in=[src_station, dest_station],
            )
            .annotate(
                matching_stops=Count(
                    "route_stations",
                    filter=Q(route_stations__station__in=[src_station, dest_station]),
                )
            )
            .filter(matching_stops=2)  # must contain both stops
            .annotate(
                src_seq=models.Min(
                    "route_stations__sequence",
                    filter=Q(route_stations__station=src_station),
                ),
                dest_seq=models.Min(
                    "route_stations__sequence",
                    filter=Q(route_stations__station=dest_station),
                ),
            )
            .filter(src_seq__lt=F("dest_seq"))  # must go in correct order
            .distinct()
        )

        if not trains.exists():
            return JsonResponse(
                {"message": "No trains found for given criteria"}, status=404
            )

        trainSerializer = TrainSerializer(trains, many=True)
        

        # ------------------------
        # Get available seats
        # ------------------------
        seatService = SeatService()

        for i, train in enumerate(trains):
            journey_details.set_train(train)
            trainSerializer.data[i]["available_seats"] = seatService.get_seats(
                journey_details
            )

        return JsonResponse({"trains": trainSerializer.data}, status=200)


class BookSeatView(APIView):

    def post(self, request):
        # Logic to book a seat would go here
        bookSerializer = BookSeatSerializer(data=request.data)

        if not bookSerializer.is_valid():
            return JsonResponse(
                {"errors": bookSerializer.errors, "message": "Invalid request"},
                status=400,
            )

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
            return JsonResponse({"message": "Train not found"}, status=404)
        except Station.DoesNotExist:
            return JsonResponse({"message": "Station not found"}, status=404)

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
            return JsonResponse({"message": "No seats available"}, status=404)

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

        return JsonResponse(
            {
                "message": "Seat booked successfully",
                "seat_number": seat_number,
                "coach_type": coach_type,
                "train_number": train_number,
                "source": source_name,
                "destination": destination_name,
            },
            status=200,
        )
