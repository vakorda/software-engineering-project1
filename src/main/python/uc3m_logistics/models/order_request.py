"""MODULE: order_request. Contains the order request class"""
import hashlib
import json
from datetime import datetime
from freezegun import freeze_time
from ..exceptions import OrderManagementException
from ..order_manager_config import JSON_FILES_PATH
from ..attributes import Address, EAN13, OrderID,\
    OrderType, PhoneNumber, ZipCode
from ..storage import OrderRequestStore, JsonStore


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

    def save_to_store(self):
        OrderRequestStore.save_order(self)

    def save_to_store_without_check(self):
        OrderRequestStore.save_order_without_ckeck(self)

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