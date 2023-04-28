"""Module """
import datetime
import json
from datetime import datetime
from freezegun import freeze_time
from .models.order_request import OrderRequest
from .models.order_delivery import OrderDelivery
from .exceptions import OrderManagementException
from .models import OrderShipping
from .order_manager_config import JSON_FILES_PATH
from .attributes import Address, EAN13, Email, OrderID,\
    OrderType, PhoneNumber, TrackingCode, ZipCode
from .storage import JsonStore, OrderDeliveryStore
from .storage.order_shipping_store import OrderShippingStore


class OrderManager:
    """Class for providing the methods for managing the orders process"""
    def __init__(self):
        pass

    @staticmethod
    def register_order(product_id: str = None,
                       order_type: str = None,
                       address: str = None,
                       phone_number: str = None,
                       zip_code: str = None):
        """Register the orders into the order's file"""
        my_order_request = OrderRequest(product_id=product_id,
                                        order_type=order_type,
                                        delivery_address=address,
                                        phone_number=phone_number,
                                        zip_code=zip_code)

        my_order_request.save_to_store()

        return my_order_request.order_id


    @classmethod
    def send_product(cls, input_file):
        """Sends the order included in the input_file"""
        store = OrderShippingStore(input_file)
        store.read_json()

        my_shipment = OrderShipping.get_order_shipping(input_file)

        # save the OrderShipping in shipments_store.json
        my_shipment.save_shipment()

        return my_shipment.tracking_code

    @classmethod
    def deliver_product(cls, tracking_code):
        """Register the delivery of the product"""
        my_delivery = OrderDelivery(tracking_code)
        item = OrderDeliveryStore().search_tracking_code(tracking_code)
        my_delivery.check_delivery_day(item["_OrderShipping__delivery_day"])
        OrderDeliveryStore().add_delivery(tracking_code)
        return True