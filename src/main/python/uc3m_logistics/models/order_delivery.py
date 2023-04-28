from ..attributes import TrackingCode
from datetime import datetime
from ..exceptions import OrderManagementException


class OrderDelivery:
    def __init__(self, tracking_code, delivery_day = None):
        self._tracking_code = TrackingCode(tracking_code).value
        self._delivery_day = delivery_day

    @property
    def tracking_code(self):
        return self._tracking_code

    @tracking_code.setter
    def tracking_code(self, value):
        self._tracking_code = TrackingCode(value).value

    @property
    def delivery_day(self):
        return self._delivery_day

    @delivery_day.setter
    def delivery_day(self, value):
        self._delivery_day = value

    def check_delivery_day(self, delivery_day):
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(delivery_day).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")
        return True