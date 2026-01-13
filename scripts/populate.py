import os
import django
import json
from django.db import transaction
from datetime import date, datetime

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railway_ticket_booking.settings")
django.setup()

from booking.models import Train, Station, RouteStation, Trip, Coach, Seat, Ticket, Booking, Invoice

Seat.objects.all().delete()
Coach.objects.all().delete()
RouteStation.objects.all().delete()
Trip.objects.all().delete()
Train.objects.all().delete()
Station.objects.all().delete()
Ticket.objects.all().delete()
Invoice.objects.all().delete()
Booking.objects.all().delete()

# Read JSON data
with open("scripts/railways_data.json", "r") as file:
    data = json.load(file)

with transaction.atomic():

    # ------------------------
    # Create stations
    # ------------------------
    stations = []
    station_lookup = {}
    for s in data["stations"]:
        station = Station(name=s["name"], code=s["code"])
        stations.append(station)
        station_lookup[s["code"]] = station

    Station.objects.bulk_create(stations, ignore_conflicts=True)

    station_map = {
        s.code: s for s in Station.objects.filter(code__in=station_lookup.keys())
    }

    # ------------------------
    # Create trains
    # ------------------------
    trains = []
    train_lookup = {}
    for t in data["trains"]:
        train = Train(name=t["name"], number=t["number"])
        trains.append(train)
        train_lookup[t["number"]] = train

    Train.objects.bulk_create(trains, ignore_conflicts=True)

    train_map = {
        t.number: t for t in Train.objects.filter(number__in=train_lookup.keys())
    }

    # ------------------------
    # Create trips
    # ------------------------
    trips = []
    trip_map = {}
    for tr in data["trips"]:
        train = train_map[tr["train_number"]]
        source_station = station_map[tr["source_code"]]

        if tr["train_number"] not in trip_map:
            trip_map[tr["train_number"]] = [tr["journey_date"]]
        else:
            trip_map[tr["train_number"]].append(tr["journey_date"])

        trip = Trip(
            train=train,
            journey_date=date.fromisoformat(tr["journey_date"]),
            rate_per_km=tr["rate_per_km"],
            source=source_station,
        )
        trips.append(trip)

    Trip.objects.bulk_create(trips, ignore_conflicts=True)

    # ------------------------
    # Create route stations
    # ------------------------
    route_stations = []
    route_map = {}
    for rs in data["route_stations"]:
        train = train_map[rs["train_number"]]
        station = station_map[rs["station_code"]]
        if rs["train_number"] not in route_map:
            route_map[rs["train_number"]] = [rs["sequence"]]
        else:
            route_map[rs["train_number"]].append(rs["sequence"])

        route_station = RouteStation(
            train=train,
            station=station,
            sequence=rs["sequence"],
            distance_from_source=rs["distance_from_source"],
        )
        route_stations.append(route_station)
    
    for train_num in route_map:
        route_map[train_num].sort()

    RouteStation.objects.bulk_create(route_stations, ignore_conflicts=True)

    # ------------------------
    # Create coaches
    # ------------------------
    # ----- Coaches -----
    coach_objs = []
    coach_map = {}
    for c in data["coaches"]:
        ctype = c["coach_type"]

        coach_objs.append(
            Coach(
                coach_name=c["coach_name"],
                coach_type=ctype
            )
        )

    Coach.objects.bulk_create(coach_objs)


    # ------------------------
    # Create seats
    # ------------------------

    seats = []

    for train_obj in Train.objects.all():
        coach_num = 1
        for coach_obj in Coach.objects.all():
            for i in range(1, 4):
                for destination_station_sequence in route_map[train_obj.number][1:]:
                    for trip_date in trip_map[train_obj.number]:
                        seats.append(
                            Seat(
                                train=train_obj,
                                coach=coach_obj,
                                seat_number=i,
                                coach_number=coach_num,
                                journey_date=date.fromisoformat(trip_date),
                                status="available",
                                destination_station_sequence=destination_station_sequence
                            )
                        )
            coach_num += 1

    Seat.objects.bulk_create(seats)

print("All data populated successfully including coaches and seats.")
