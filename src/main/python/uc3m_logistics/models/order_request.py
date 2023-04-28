"""MODULE: order_request. Contains the order request class"""
import hashlib
import json
from datetime import datetime
from freezegun import freeze_time
from uc3m_logistics.exceptions.order_management_exception import OrderManagementException
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.attributes import Address, EAN13, OrderID,\
    OrderType, PhoneNumber, ZipCode
from uc3m_logistics.storage import OrderRequestStore


class OrderRequest:
    """Class representing the register of the order in the system"""
    # pylint: disable=too-many-arguments
    def __init__(self, product_id: str = None, order_type: str = "Regular",
                 delivery_address: str = None, phone_number: str = None, zip_code: str = None):
        self.__product_id = EAN13(product_id).value
        self.__delivery_address = Address(delivery_address).value
        self.__order_type = OrderType(order_type).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__zip_code = ZipCode(zip_code).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        self.__order_id = OrderID(hashlib.md5(self.__str__().encode()).hexdigest()).value

    def __str__(self):
        return "OrderRequest:" + json.dumps(self.__dict__)

    @property
    def delivery_address(self):
        """Property representing the address where the product
        must be delivered"""
        return self.__delivery_address

    @delivery_address.setter
    def delivery_address(self, value):
        self.__delivery_address = value

    @property
    def order_type(self):
        """Property representing the type of order: REGULAR or PREMIUM"""
        return self.__order_type

    @order_type.setter
    def order_type(self, value):
        self.__order_type = value

    @property
    def phone_number(self):
        """Property representing the clients' phone number"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @property
    def product_id(self):
        """Property representing the products  EAN13 code"""
        return self.__product_id

    @product_id.setter
    def product_id(self, value):
        self.__product_id = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def order_id(self):
        """Returns the md5 signature"""
        return self.__order_id

    @property
    def zip_code(self):
        """Returns the order's zip_code"""
        return self.__zip_code

    @classmethod
    def search_order_id(cls, order_id):  # find_item_by_key
        file_store = JSON_FILES_PATH + "orders_store.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == order_id:
                found = True
                # retrieve the orders data
                product_id = item["_OrderRequest__product_id"]
                delivery_address = item["_OrderRequest__delivery_address"]
                order_type = item["_OrderRequest__order_type"]
                phone_number = item["_OrderRequest__phone_number"]
                order_timestamp = item["_OrderRequest__time_stamp"]
                zip_code = item["_OrderRequest__zip_code"]
                # set the time when the order was registered for checking the md5
                with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                    order = cls(product_id=product_id,
                                delivery_address=delivery_address,
                                order_type=order_type,
                                phone_number=phone_number,
                                zip_code=zip_code)

                if order.order_id != order_id:
                    raise OrderManagementException("Orders' data have been manipulated")
        if not found:
            raise OrderManagementException("order_id not found")
        return order

    def save_to_store(self):
        OrderRequestStore.save_order(self)
