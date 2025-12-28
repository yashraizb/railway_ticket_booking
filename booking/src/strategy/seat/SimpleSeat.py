from booking.models import RouteStation, Seat, Train, Station
from django.db.models import Count, Q, OuterRef, Exists
from booking.src.strategy.seat.SeatStrategy import SeatStrategy


class SimpleSeat(SeatStrategy):
    def get_available_seats(self, data):
        train: Train = data["train"]
        source: Station = data["source"]
        destination: Station = data["destination"]
        journey_date = data["journey_date"]

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
            status="available",
        )

        available_seats = (
            list_seats.values("coach__coach_type", "coach_number", "seat_number")
            .annotate(cnt=Count("id"))
            .filter(cnt=(dest_stn_seq - src_stn_seq))
        )

        available_seats_subq = available_seats.filter(
            coach_number=OuterRef("coach_number"),
            seat_number=OuterRef("seat_number"),
        )

        final_seats = (
            list_seats.filter(Exists(available_seats_subq))
            .values("coach__coach_name", "seat_number")
            .distinct()
        )

        count_seats = {}
        for seat in final_seats:
            if seat["coach__coach_name"] in count_seats:
                count_seats[seat["coach__coach_name"]] += 1
            else:
                count_seats[seat["coach__coach_name"]] = 1

        return count_seats