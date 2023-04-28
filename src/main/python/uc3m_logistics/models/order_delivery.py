from ..attributes import TrackingCode

class OrderDelivery:
    def __init__(self, tracking_code, delivery_day):
        self._tracking_code = TrackingCode(tracking_code).value
        self._delivery_day = delivery_day # str(datetime.utcnow())