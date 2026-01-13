from django.contrib import admin
from .models import (
    Trip,
    Seat,
    Coach,
    Train,
    Station,
    RouteStation,
    Ticket,
    Booking,
    Invoice,
)

# Register your models here

admin.site.register(Train)
admin.site.register(Coach)
admin.site.register(Seat)
admin.site.register(Trip)
admin.site.register(Station)
admin.site.register(RouteStation)
admin.site.register(Ticket)
admin.site.register(Booking)
admin.site.register(Invoice)
