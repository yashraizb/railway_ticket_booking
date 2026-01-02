from booking.serializer import BookSeatSerializer
from booking.models import Bookings, BookingToInvoice


class TicketService:
    def __init__(self):
        pass

    def save_ticket(self, bookingSerializer: BookSeatSerializer, seats: list):
        bookingToInvoice = BookingToInvoice.objects.create()
        i = 0
        for passenger in bookingSerializer.validated_data["passengers"]:
            Bookings.objects.create(
                train_number=bookingSerializer.validated_data["train_number"],
                source_name=bookingSerializer.validated_data["source"],
                destination_name=bookingSerializer.validated_data["destination"],
                journey_date=bookingSerializer.validated_data["journey_date"],
                coach_type=bookingSerializer.validated_data["coach_type"],
                seat_number=seats[i],
                passenger_name=passenger["name"],
                passenger_age=passenger["age"],
                passenger_gender=passenger["gender"],
                booking_id=bookingToInvoice.booking_id
            )
            i += 1
        
        return bookingToInvoice