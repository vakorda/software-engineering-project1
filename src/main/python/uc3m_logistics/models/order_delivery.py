from datetime import datetime
from ..attributes import TrackingCode
from ..storage import OrderDeliveryStore, OrderShippingStore


class OrderDelivery:
    def __init__(self, tracking_code, delivery_day):
        self._tracking_code = TrackingCode(tracking_code).value
        self._delivery_day = delivery_day #str(datetime.utcnow())

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

    def save_to_store(self):
        OrderDeliveryStore().add_item(self)

    @classmethod
    def search_tracking_code(cls, tracking_code):
        """Check if this tracking_code is in shipments_store"""
        TrackingCode(tracking_code)
        item = OrderShippingStore().get_item_from_tracking_code(tracking_code)
        my_delivery = cls(tracking_code=item["_OrderShipping__tracking_code"],
                          delivery_day=item["_OrderShipping__delivery_day"])
        OrderDeliveryStore.check_delivery_day(my_delivery.delivery_day)
        return cls(tracking_code, my_delivery.delivery_day)

