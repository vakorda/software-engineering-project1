"""Module """
import datetime
import json
from datetime import datetime
from freezegun import freeze_time
from .models import OrderRequest
from .exceptions import OrderManagementException
from .models import OrderShipping
from .order_manager_config import JSON_FILES_PATH
from .attributes import Address, EAN13, Email, OrderID,\
    OrderType, PhoneNumber, TrackingCode, ZipCode
from .storage import JsonStore, OrderShippingStore


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
    def save_shipment(cls, shipment):
        """Saves the shipping object into a file"""
        file_name = "shipments_store.json"
        # first read the file
        store = JsonStore(file_name)
        store.read_json()
        # append the shipments list
        store.add_dict_item(shipment.__dict__)
        store.write_json()


    # pylint: disable=too-many-locals
    @classmethod
    def send_product(cls, input_file):
        """Sends the order included in the input_file"""
        store = OrderShippingStore(input_file)
        store.read_json()

        my_shipment = store.get_order_shipping()

        # save the OrderShipping in shipments_store.json
        cls.save_shipment(my_shipment)

        return my_shipment.tracking_code

    @classmethod
    def deliver_product(cls, tracking_code):
        """Register the delivery of the product"""
        TrackingCode(tracking_code)  # TODO
        item = cls.search_tracking_code(tracking_code)

        delivery_day = item["_OrderShipping__delivery_day"]
        cls.check_delivery_day(delivery_day)

        file_name = "shipments_delivered.json"

        store = JsonStore(file_name)
        store.read_json()

        # append the delivery info
        store.add_dict_item(str(tracking_code))
        store.add_dict_item(str(datetime.utcnow()))
        store.write_json()
        return True

    @staticmethod
    def check_delivery_day(delivery_day):
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(delivery_day).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

    @staticmethod
    def search_tracking_code(tracking_code):
        """Check if this tracking_code is in shipments_store"""
        shipments_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shipments_store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException("shipments_store not found") from ex
        # search this tracking_code
        for item in data_list:
            if item["_OrderShipping__tracking_code"] == tracking_code:
                return item
        raise OrderManagementException("tracking_code is not found")

