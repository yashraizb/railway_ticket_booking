from booking.src.strategy.refund.CalculationStrategy import CalculationStrategy


class QtrRefund(CalculationStrategy):
    def calculate_refund(self, amount):
        # Quarter refund logic
        return amount / 4