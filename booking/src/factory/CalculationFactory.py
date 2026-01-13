from booking.src.strategy.refund.FullRefund import FullRefund
from booking.src.strategy.refund.HalfRefund import HalfRefund
from booking.src.strategy.refund.QtrRefund import QtrRefund


class CalculationFactory:
    def __init__(self):
        self.map = {
            "full": FullRefund,
            "half": HalfRefund,
            "qtr": QtrRefund,
        }
    
    def get_refund_strategy(self, strategy):
        if strategy not in self.map:
            raise ValueError(f"Unknown strategy: {strategy}")
        return self.map[strategy]()