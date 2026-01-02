import traceback as tb
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Train, BookingToInvoice
from .serializer import TrainSerializer, SearchTrainSerializer, BookSeatSerializer
from rest_framework.permissions import AllowAny
from .src.service.SeatService import SeatService
from .src.service.TrainService import TrainService
from .src.service.TicketService import TicketService
from .src.service.InvoiceService import InvoiceService
from .src.domain.JourneyDetailHandler import JourneyDetailHandler


# Create your views here.
class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "ok"}, status=200)


class ListTrainsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # Logic to list trains would go here
        all_trains = Train.objects.all()
        serializer = TrainSerializer(all_trains, many=True)
        return JsonResponse({"trains": serializer.data}, status=200)


class SearchTrainsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        journey_details = JourneyDetailHandler()
        searchTrainSerializer = SearchTrainSerializer(data=request.query_params)
        if not searchTrainSerializer.is_valid():
            return JsonResponse(
                {"errors": searchTrainSerializer.errors, "message": "Search failed"}, status=400
            )

        trainService = TrainService()
        trains = trainService.get_trains(searchTrainSerializer, journey_details)

        if not trains.exists():
            return JsonResponse(
                {"message": "No trains found for given criteria"}, status=404
            )

        trainSerializer = TrainSerializer(trains, many=True)

        # ------------------------
        # Get available seats
        # ------------------------
        seatService = SeatService()

        for i, train in enumerate(trains):
            journey_details.set_train(train)
            trainSerializer.data[i]["available_seats"] = seatService.get_seats(
                journey_details
            )

        return JsonResponse({"trains": trainSerializer.data}, status=200)


class BookSeatView(APIView):

    def post(self, request):
        try:
            # Logic to book a seat would go here
            bookSerializer = BookSeatSerializer(data=request.data)
            journey_details = JourneyDetailHandler()

            if not bookSerializer.is_valid():
                return JsonResponse(
                    {"errors": bookSerializer.errors, "message": "Invalid request"},
                    status=400,
                )

            seatService = SeatService()
            seat_numbers = seatService.book_seat(bookSerializer, journey_details)

            ticketService = TicketService()
            bookingToInvoice: BookingToInvoice = ticketService.save_ticket(bookSerializer, seat_numbers)
            journey_details.set_booking(bookingToInvoice)

            invoiceService = InvoiceService()
            invoice = invoiceService.generate_invoice(bookSerializer, journey_details)
            
            bookingToInvoice.invoice_id = invoice.invoice_id
            bookingToInvoice.save()

            return JsonResponse(
                {
                    "message": "Seat booked successfully",
                    "seat_number": seat_numbers,
                    "coach_type": bookSerializer.validated_data["coach_type"],
                    "train_number": bookSerializer.validated_data["train_number"],
                    "source": bookSerializer.validated_data["source"],
                    "destination": bookSerializer.validated_data["destination"],
                    "pnr": bookingToInvoice.booking_id
                },
                status=200,
            )

        except Exception as e:
            print(e)
            print(tb.format_exc())
            return JsonResponse({"message": str(e)}, status=400)
