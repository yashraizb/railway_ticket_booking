import traceback as tb
from datetime import datetime, timedelta
from booking.models import Refund
from booking.src.factory.CalculationFactory import CalculationFactory


class RefundService:
        
    def amountCalculate(self, amount, journey_date):
        diff = journey_date - datetime.now().date()
        factory = CalculationFactory()
        if timedelta(days=7) < diff:
            return factory.get_refund_strategy("full").calculate_refund(amount)
        elif timedelta(days=3) < diff:
            return factory.get_refund_strategy("half").calculate_refund(amount)
        elif timedelta(days=1) < diff:
            return factory.get_refund_strategy("qtr").calculate_refund(amount)
        else:
            return 0

    def initiateRefund(self, facade):
        # Logic to process refund
        try:
            amount = self.amountCalculate(facade.invoice.amount, facade.booking.journey_date)
            refund = Refund.objects.create(
                invoice=facade.invoice,
                booking=facade.booking,
                amount=facade.invoice.amount,
                approved_amount=amount,
                requested_date=datetime.now(),
                refund_date=None,
            )
            facade.refund = refund
        except Exception as e:
            print("Exception in RefundService:", str(e))
            print(tb.format_exc())
            raise e
