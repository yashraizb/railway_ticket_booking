from django.urls import path
from .views import HealthCheckView, ListTrainsView, SearchTrainsView, BookSeatView, CancelBookingView


urlpatterns = [
    path('health', HealthCheckView.as_view(), name='health_check'),
    path('getTrains', ListTrainsView.as_view(), name='list_trains'),
    path('searchTrains', SearchTrainsView.as_view(), name='search_trains'),
    path('bookSeat', BookSeatView.as_view(), name='book_seat'),
    path('cancelBooking', CancelBookingView.as_view(), name='cancel_booking'),
]