import traceback as tb
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from .models import Train, Booking
from .serializer import TrainSerializer, SearchTrainSerializer, BookSeatSerializer, CancelBookingSerializer
from rest_framework.permissions import AllowAny
from .src.service.SeatService import SeatService
from .src.service.TrainService import TrainService
from .src.service.TicketService import TicketService
from .src.service.InvoiceService import InvoiceService
from .src.domain.JourneyDetailHandler import JourneyDetailHandler
from .src.facade.BookingFacade import BookingFacade
from .src.facade.CancelFacade import CancelFacade
from accounts.models import CustomUser
from booking.src.domain.CustomException import CustomException


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

        try:
            # Logic to search trains would go here
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
        except CustomException as ce:
            return JsonResponse(
                ce.getErrorJson(), status=ce.code
            )
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)


class BookSeatView(APIView):

    def post(self, request):
        try:

            user = request.user
            # Logic to book a seat would go here
            bookSerializer = BookSeatSerializer(data=request.data)
            journey_details = JourneyDetailHandler()

            if not bookSerializer.is_valid():
                return JsonResponse(
                    {"errors": bookSerializer.errors, "message": "Invalid request"},
                    status=400,
                )

            bookingFacade: BookingFacade = BookingFacade(bookSerializer, user, journey_details)

            bookingFacade.execute()

            return JsonResponse(
                {
                    "message": "Seat booked successfully",
                    "seat_number": bookingFacade.seat_numbers,
                    "coach_type": bookSerializer.validated_data["coach_type"],
                    "train_number": bookSerializer.validated_data["train_number"],
                    "source": bookSerializer.validated_data["source"],
                    "destination": bookSerializer.validated_data["destination"],
                    "pnr": bookingFacade.booking_id
                },
                status=200,
            )
        
        except CustomException as ce:
            if 'bookingFacade' in locals():
                bookingFacade.rollback()
            return JsonResponse(
                ce.getErrorJson(), status=ce.code
            )

        except Exception as e:
            print(e)
            print(tb.format_exc())
            if 'bookingFacade' in locals():
                print("Rolling back from BookSeatView")
                bookingFacade.rollback()
            return JsonResponse({"message": str(e)}, status=500)


class CancelBookingView(APIView):
    def delete(self, request):
        try:
            cancelBookingSerializer = CancelBookingSerializer(data=request.data)
            if not cancelBookingSerializer.is_valid():
                return JsonResponse(
                    {"errors": cancelBookingSerializer.errors, "message": "Invalid request"},
                    status=400,
                )

            cancelFacade = CancelFacade(cancelBookingSerializer, request.user)
            cancelFacade.execute()
            return JsonResponse({"message": "Booking cancelled successfully"}, status=200)
        except CustomException as ce:
            print(ce)
            print(tb.format_exc())
            return JsonResponse(
                ce.getErrorJson(), status=ce.code
            )
        except ObjectDoesNotExist as oe:
            print(oe)
            print(tb.format_exc())
            return JsonResponse({"message": "Invalid request", "error": str(oe)}, status=404)
        except Exception as e:
            print(e)
            print(tb.format_exc())
            return JsonResponse({"message": str(e)}, status=500)