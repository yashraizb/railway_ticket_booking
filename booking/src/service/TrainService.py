from django.db import models
from django.db.models import Count, F, Q
from django.http import JsonResponse
from booking.models import Train, Station
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler
from booking.serializer import SearchTrainSerializer


class TrainService:
    def get_trains(self, searchTrainSerializer: SearchTrainSerializer, journey_details: JourneyDetailHandler):
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

        return trains
