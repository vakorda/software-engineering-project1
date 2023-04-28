from datetime import datetime
from ..exceptions import OrderManagementException


class OrderDeliveryStore:
    def __init__(self):
        pass

    @staticmethod
    def check_delivery_day(delivery_day):
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(delivery_day).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")
