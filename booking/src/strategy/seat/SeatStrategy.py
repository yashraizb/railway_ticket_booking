from abc import ABC, abstractmethod

class SeatStrategy(ABC):
    @abstractmethod
    def get_available_seats(self):
        pass