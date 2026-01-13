from booking.src.strategy.refund.CalculationStrategy import CalculationStrategy


class FullRefund(CalculationStrategy):
    def calculate_refund(self, amount):
        # Full refund logic
        return amount