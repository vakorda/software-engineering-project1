
class OrderDelivered:
    def __init__(self, tracking_code):
        self._tracking_code = TrackingCode(tracking_code).value
        self._delivery_day = _validate_delivery_day(today.noverysure)

    def _validate_delivery_day(self, delivery_day):
