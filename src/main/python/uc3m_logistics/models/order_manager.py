"""Module """
import datetime
import json
from datetime import datetime
from freezegun import freeze_time
from uc3m_logistics.models.order_request import OrderRequest
from uc3m_logistics.exceptions.order_management_exception import OrderManagementException
from uc3m_logistics.models.order_shipping import OrderShipping
from .order_delivery import OrderDelivery
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.attributes import Address, EAN13, Email, OrderID,\
    OrderType, PhoneNumber, TrackingCode, ZipCode
from uc3m_logistics.storage import JsonStore
from ..storage import OrderDeliveryStore


class OrderManager:
    """Class for providing the methods for managing the orders process"""
    def __init__(self):
        pass

    # pylint: disable=too-many-arguments
    @classmethod
    def register_order(cls, product_id: str = None,  # DONE
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
    def send_product(cls, input_file): # DONE
        """Sends the order included in the input_file"""

        my_shipment = OrderShipping.shipping_from_file(input_file)

        # save the OrderShipping in shipments_store.json
        my_shipment.save_to_store()

        return my_shipment.tracking_code

    @classmethod
    def deliver_product(cls, tracking_code):
        """Register the delivery of the product"""
        # TODO
        item = OrderDelivery(tracking_code).search_tracking_code(tracking_code)

        delivery_day = item["_OrderShipping__delivery_day"]
        OrderDeliveryStore.check_delivery_day(delivery_day)

        file_name = "shipments_delivered.json"

        store = JsonStore(file_name).read_json()

        # append the delivery info
        store.add_item(str(tracking_code))
        store.add_item(str(datetime.utcnow()))
        store.write_json()
        return True
