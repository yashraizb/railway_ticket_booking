from booking.src.strategy.refund.CalculationStrategy import CalculationStrategy


class HalfRefund(CalculationStrategy):
    def calculate_refund(self, amount):
        # Half refund logic
        return amount / 2