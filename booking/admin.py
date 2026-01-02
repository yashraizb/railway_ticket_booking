from django.contrib import admin
from .models import (
    Trip,
    Seat,
    Coach,
    Train,
    Station,
    RouteStation,
    Bookings,
    BookingToInvoice,
    Invoice,
)

# Register your models here

admin.site.register(Train)
admin.site.register(Coach)
admin.site.register(Seat)
admin.site.register(Trip)
admin.site.register(Station)
admin.site.register(RouteStation)
admin.site.register(Bookings)
admin.site.register(BookingToInvoice)
admin.site.register(Invoice)
