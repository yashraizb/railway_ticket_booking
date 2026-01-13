from abc import ABC, abstractmethod


class CalculationStrategy(ABC):

    @abstractmethod
    def calculate_refund(self, booking_details):
        pass