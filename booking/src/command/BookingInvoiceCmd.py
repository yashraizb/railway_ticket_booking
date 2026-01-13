from booking.models import Booking


class BookingInvoiceCmd:
    def __init__(self):
        self.bookingToInvoice = None

    def createBookingToInvoice(self, facade):
        status = ""

        if len(facade.bookingSerializer.validated_data.get("passengers")) == len(
            facade.seat_numbers
        ):
            status = "CONFIRMED"
        else:
            status = "PartialConfirmed"

        self.bookingToInvoice = Booking.objects.create(
            user=facade.user,
            source_station=facade.journeyDetails.get_src_station(),
            destination_station=facade.journeyDetails.get_dest_station(),
            journey_date=facade.journeyDetails.get_journey_date(),
            status=(
                Booking.StatusChoices.CONFIRMED
                if len(facade.bookingSerializer.validated_data.get("passengers"))
                == len(facade.seat_numbers)
                else Booking.StatusChoices.PARTIAL_CONFIRMED
            ),
            train=facade.journeyDetails.get_train(),
        )

    def rollback(self):
        print("Rolling back: BookingInvoiceCmd")
        self.bookingToInvoice.delete()
