import traceback as tb
from django.db import transaction
from booking.models import Booking, RouteStation, Refund, Invoice
from booking.src.domain.CustomException import CustomException
from booking.src.service.InvoiceService import InvoiceService
from booking.src.service.SeatService import SeatService
from booking.src.service.TicketService import TicketService
from booking.src.service.RefundService import RefundService


class CancelFacade:
    def __init__(self, cancelBookingSerializer, user):
        self.cancelBookingSerializer = cancelBookingSerializer
        self.user = user
        self.isPartial = False
        self.tickets = []
        self.refund = None

    def execute(self):
        lastProcess = "Initialization"
        refund = None
        
        try:
            # Step 0: Validate booking and create refund record OUTSIDE transaction
            # This ensures refund record persists even if transaction fails
            booking = Booking.objects.get(
                booking_id=self.cancelBookingSerializer.validated_data["pnr"],
                status=Booking.StatusChoices.CONFIRMED,
            )

            if booking.user.email != self.user.email:
                raise CustomException(
                    "Unauthorized to cancel this booking", "UNAUTHORIZED_CANCELLATION"
                )

            self.booking = booking
            self.src_stn = RouteStation.objects.filter(
                station=booking.source_station, train=booking.train
            ).first()
            self.dest_stn = RouteStation.objects.filter(
                station=booking.destination_station, train=booking.train
            ).first()
            
            # Fetch invoice for refund calculation (before transaction)
            self.invoice = Invoice.objects.filter(booking_id=booking.booking_id).first()
            if not self.invoice:
                raise CustomException("Invoice not found", "NOT_FOUND")

            # Create refund record OUTSIDE transaction so it persists on failure
            refundService = RefundService()
            refundService.initiateRefund(self)
            refund = self.refund
            lastProcess = "Refund Initiated"

            # All cancellation operations inside transaction
            with transaction.atomic():
                # Step 1: Cancel Invoice
                invoiceService = InvoiceService()
                invoiceService.cancelInvoice(booking.booking_id)
                lastProcess = "Invoice Cancellation"

                # Step 2: Cancel Tickets
                ticketService = TicketService(self)
                ticketService.cancelTickets()
                lastProcess = "Ticket Cancellation"

                # Step 3: Free Seats
                seatService = SeatService()
                seatService.freeSeats(self)
                lastProcess = "Seat Deallocation"

                # Step 4: Update Booking Status
                booking.status = (
                    Booking.StatusChoices.CANCELLED
                    if not self.isPartial
                    else Booking.StatusChoices.PARTIAL_CANCELLED
                )
                booking.save()
                lastProcess = "Booking Cancellation"

            # Update refund status AFTER successful transaction
            refund.status = Refund.StatusChoices.REQUESTED
            refund.last_process = lastProcess
            refund.save()
            
        except Exception as e:
            print("Exception in CancelFacade:", str(e))
            print(tb.format_exc())
            # Update refund with failure status (refund record exists outside transaction)
            if refund:
                refund.status = Refund.StatusChoices.HALTED
                refund.last_process = lastProcess
                refund.save()
            raise CustomException(
                "Cancellation failed after step: "
                + lastProcess
                + " with error: "
                + str(e),
                "CANCELLATION_FAILED",
            )
