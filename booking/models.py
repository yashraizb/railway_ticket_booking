from django.db import models

# Create your models here.


class Train(models.Model):
    name = models.CharField(max_length=50)
    number = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"{self.number} - {self.name}"


class Coach(models.Model):

    class CoachType(models.TextChoices):
        SL = "SL", "Sleeper"
        A3 = "3A", "AC 3 Tier"
        A2 = "2A", "AC 2 Tier"
        FC = "1A", "First Class"
        CC = "CC", "Chair Car"

    coach_type = models.CharField(max_length=2, choices=CoachType.choices)
    coach_name = models.CharField(max_length=10)


class Seat(models.Model):
    """
    This class definition defines a 
    Seat model in Django. It has the following fields:

    seat_number: An integer field representing the seat number.
    coach: A foreign key field that links to the 
    Coach
    model.
    coach_number: A positive integer field representing the coach number.
    train: A foreign key field that links to the 
    Train
    model.
    journey_date: A date field representing the journey date.
    status: A character field representing the seat status (default is "available").
    destination_station_sequence: A positive integer field representing the destination station sequence.
    The 
    Meta
    class within the 
    Seat
    model specifies that the combination of seat_number, coach, journey_date, and train fields must be unique.

    Here is a list of what each class method does:

    No class methods are defined in this class.
    """
    seat_number = models.IntegerField()
    coach = models.ForeignKey(
        Coach, on_delete=models.CASCADE, related_name="seats"
    )
    coach_number = models.PositiveIntegerField(default=0)
    train = models.ForeignKey(
        Train, on_delete=models.CASCADE, related_name="train_seats"
    )
    journey_date = models.DateField()
    status = models.CharField(max_length=20, default="available")
    destination_station_sequence = models.PositiveIntegerField(default=0)


class Station(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Trip(models.Model):
    train = models.ForeignKey(
        Train, on_delete=models.CASCADE, related_name="trips"
    )
    journey_date = models.DateField(default=None)
    rate_per_km = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00
    )
    source = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="source", default=None
    )

    class Meta:
        unique_together = ("train", "journey_date")


class RouteStation(models.Model):
    train = models.ForeignKey(
        Train, on_delete=models.CASCADE, related_name="route_stations"
    )
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()
    distance_from_source = models.DecimalField(
        max_digits=6, decimal_places=2
    )

    class Meta:
        unique_together = ("train", "station")
        ordering = ["sequence"]

class Bookings(models.Model):
    booking_id = models.BigIntegerField(default=0)
    train_number = models.BigIntegerField()
    source_name = models.CharField(max_length=50)
    destination_name = models.CharField(max_length=50)
    journey_date = models.DateField()
    coach_type = models.CharField(max_length=2)
    seat_number = models.IntegerField()
    passenger_name = models.CharField(max_length=50)
    passenger_age = models.IntegerField()
    passenger_gender = models.CharField(max_length=1)


class BookingToInvoice(models.Model):
    booking_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    invoice_id = models.BigIntegerField(default=0)


class Invoice(models.Model):
    invoice_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    train_number = models.BigIntegerField()
    source_name = models.CharField(max_length=50)
    destination_name = models.CharField(max_length=50)
    journey_date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    booking_id = models.BigIntegerField()