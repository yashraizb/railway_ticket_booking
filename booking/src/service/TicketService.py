from booking.models import Ticket


class TicketService:
    def __init__(
        self,
        facade,
    ):
        self.facade = facade

    def save_ticket(self):
        i = 0
        for passenger in self.facade.bookingSerializer.validated_data["passengers"]:
            Ticket.objects.create(
                coach_type=self.facade.bookingSerializer.validated_data["coach_type"],
                seat_number=self.facade.seats[i],
                passenger_name=passenger["name"],
                passenger_age=passenger["age"],
                passenger_gender=passenger["gender"],
                booking_id=self.facade.bookingToInvoice.booking_id,
                status=Ticket.StatusChoices.CONFIRMED if self.facade.seats[i] != "WL" else Ticket.StatusChoices.WAITING,
            )
            i += 1

    def rollback(self):
        print("Rolling back: TicketService")
        Ticket.objects.filter(booking_id=self.bookingToInvoice.booking_id).delete()
    
    def cancelTickets(self):
        passenger_names = [p["name"] for p in self.facade.cancelBookingSerializer.validated_data["passengers"]]
        tickets = Ticket.objects.filter(booking_id=self.facade.booking.booking_id)
        self.facade.isPartial = len(passenger_names) < tickets.count()
        tickets = tickets.filter(passenger_name__in=passenger_names)

        for ticket in tickets:
            ticket.status = Ticket.StatusChoices.CANCELLED
            self.facade.tickets.append(ticket)
            ticket.save()