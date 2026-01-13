from booking.models import Invoice, Trip
from booking.serializer import BookSeatSerializer
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler
from booking.src.domain.CustomException import CustomException


class InvoiceService:
    def __init__(self):
        self.invoice = None

    def generate_invoice(
        self,
        bookingSerializer: BookSeatSerializer,
        journeyDetails: JourneyDetailHandler,
    ):
        trip = Trip.objects.get(
            train__number=bookingSerializer.validated_data["train_number"],
            journey_date=bookingSerializer.validated_data["journey_date"],
        )

        amount = (
            trip.rate_per_km
            * (
                journeyDetails.get_dest_route_station().distance_from_source
                - journeyDetails.get_src_route_station().distance_from_source
            )
            * len(bookingSerializer.validated_data["passengers"])
        )

        self.invoice = Invoice.objects.create(
            amount=amount,
            booking_id=journeyDetails.get_booking().booking_id,
            status=Invoice.StatusChoices.PAID,
        )

        return self.invoice

    def rollback(self):
        print("Rolling back: InvoiceService")
        self.invoice.delete()
    
    def cancelInvoice(self, booking_id):
        self.invoice = Invoice.objects.filter(booking_id=booking_id).first()
        if not self.invoice:
            raise CustomException("Invoice not found", "NOT_FOUND")
        self.invoice.status = Invoice.StatusChoices.CANCELLED
        self.invoice.save()
