from typing import Union
from booking.src.service.SeatService import SeatService
from booking.src.domain.JourneyDetailHandler import JourneyDetailHandler
from booking.src.service.TicketService import TicketService
from booking.models import Booking
from booking.src.command.BookingInvoiceCmd import BookingInvoiceCmd
from booking.src.service.InvoiceService import InvoiceService

class BookingFacade:

    def __init__(self, bookingSerializer, user, journeyDetails: JourneyDetailHandler):
        self.bookingSerializer = bookingSerializer
        self.seat_numbers = None
        self.user = user
        self.journeyDetails = journeyDetails
        self.stepsStack = []
    
    def execute(self):
        # Step 1: Book Seats
        seatService = SeatService()
        self.seat_numbers = seatService.book_seat(self.bookingSerializer, self.journeyDetails)
        self.stepsStack.append(seatService)

        # Step 2: Create BookingToInvoice instance
        bookingToInvoice = BookingInvoiceCmd()
        bookingToInvoice.createBookingToInvoice(self)
        self.booking_id = bookingToInvoice.bookingToInvoice.booking_id
        self.journeyDetails.set_booking(bookingToInvoice.bookingToInvoice)
        self.stepsStack.append(bookingToInvoice)

        # Step 3: Save Ticket
        ticketService = TicketService(self)
        ticketService.save_ticket()
        self.stepsStack.append(ticketService)

        # Step 4: Generate Invoice
        invoiceService = InvoiceService()
        invoice = invoiceService.generate_invoice(self.bookingSerializer, self.journeyDetails)
        self.stepsStack.append(invoiceService)

        bookingToInvoice.bookingToInvoice.invoice_id = invoice.invoice_id
        bookingToInvoice.bookingToInvoice.save()

        return bookingToInvoice
    
    def rollback(self):
        # Implement rollback logic if needed
        while self.stepsStack:
            step: Union[SeatService, BookingInvoiceCmd, TicketService, InvoiceService] = self.stepsStack.pop()
            # Call rollback method on each step if defined
            step.rollback()