from abc import ABC, abstractmethod


class BookingStrategy(ABC):
    @abstractmethod
    def book(self):
        pass