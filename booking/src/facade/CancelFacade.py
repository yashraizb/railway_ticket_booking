from booking.models import Booking, RouteStation
from booking.src.domain.CustomException import CustomException
from booking.src.service.InvoiceService import InvoiceService
from booking.src.service.SeatService import SeatService
from booking.src.service.TicketService import TicketService


class CancelFacade:
    def __init__(self, cancelBookingSerializer, user):
        self.cancelBookingSerializer = cancelBookingSerializer
        self.user = user
        self.isPartial = False
        self.tickets = []

    def execute(self):
        booking = Booking.objects.get(
            booking_id=self.cancelBookingSerializer.validated_data["pnr"],
            status=Booking.StatusChoices.CONFIRMED
        )
        
        if booking.user.email != self.user.email:
            raise CustomException(
                "Unauthorized to cancel this booking", "UNAUTHORIZED_CANCELLATION"
            )

        self.booking = booking
        self.src_stn = RouteStation.objects.filter(
            station=booking.source_station, 
            train=booking.train
        ).first()
        self.dest_stn = RouteStation.objects.filter(
            station=booking.destination_station, 
            train=booking.train
        ).first()

        # Step 1: Delete Invoice
        invoiceService = InvoiceService()
        invoiceService.cancelInvoice(booking.booking_id)

        # Step 2: Delete Tickets
        ticketService = TicketService(self)
        ticketService.cancelTickets()

        # Step 3: Delete Seats
        seatService = SeatService()
        seatService.freeSeats(self)

        # Step 4: Delete Booking
        booking.status = Booking.StatusChoices.CANCELLED if not self.isPartial else Booking.StatusChoices.PARTIAL_CANCELLED
        booking.save()
