from booking.models import Invoice, Trip
from booking.serializer import BookSeatSerializer
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler


class InvoiceService:
    def __init__(self):
        pass

    def generate_invoice(self, bookingSerializer: BookSeatSerializer, journeyDetails: JourneyDetailHandler):
        trip = Trip.objects.get(
            train__number=bookingSerializer.validated_data["train_number"],
            journey_date=bookingSerializer.validated_data["journey_date"],
        )

        amount = trip.rate_per_km * (
            journeyDetails.get_dest_station().distance_from_source - journeyDetails.get_src_station().distance_from_source)

        return Invoice.objects.create(
            train_number=bookingSerializer.validated_data["train_number"],
            source_name=bookingSerializer.validated_data["source"],
            destination_name=bookingSerializer.validated_data["destination"],
            journey_date=bookingSerializer.validated_data["journey_date"],
            amount=amount,
            booking_id=journeyDetails.get_booking().booking_id,
        )