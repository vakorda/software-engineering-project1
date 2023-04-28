"""Contains the class OrderShipping"""
from datetime import datetime
import hashlib
from ..attributes import EAN13, Email, OrderID, TrackingCode
from ..storage.order_shipping_store import OrderShippingStore, JsonStore


class OrderShipping:
    """Class representing the shipping of an order"""

    def __init__(self, product_id, order_id, delivery_email, order_type):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__product_id = EAN13(product_id).value
        self.__order_id = OrderID(order_id).value
        self.__delivery_email = Email(delivery_email).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        delivery_days = 7 if order_type == "Regular" else 1
        # timestamp is represented in seconds.microseconds
        # __delivery_day must be expressed in seconds to be added to the timestamp
        self.__delivery_day = self.__issued_at + (delivery_days * 24 * 60 * 60)
        self.__tracking_code = TrackingCode(hashlib.sha256(self.__signature_string().encode()).hexdigest()).value

    def save_shipment(self):
        """Saves the shipping object into a file"""
        file_name = "shipments_store.json"
        # first read the file
        store = JsonStore(file_name)
        store.read_json()
        # append the shipments list
        store.add_dict_item(self.__dict__)
        store.write_json()

    @classmethod
    def get_order_shipping(cls, file):
        # check all the information
        store = OrderShippingStore(file)
        store.read_json()
        order = store.find_order_from_shipment()

        return cls(product_id=order.product_id,
                   order_id=store.get_elem("OrderID"),
                   order_type=order.order_type,
                   delivery_email=store.get_elem("ContactEmail"))

    def __signature_string(self):
        """Composes the string to be used for generating the tracking_code"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",order_id:" + \
               self.__order_id + ",issuedate:" + str(self.__issued_at) + \
               ",deliveryday:" + str(self.__delivery_day) + "}"

    @property
    def product_id(self):
        """Property that represents the product_id of the order"""
        return self.__product_id

    @product_id.setter
    def product_id(self, value):
        self.__product_id = value

    @property
    def order_id(self):
        """Property that represents the order_id"""
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = value

    @property
    def email(self):
        """Property that represents the email of the client"""
        return self.__delivery_email

    @email.setter
    def email(self, value):
        self.__delivery_email = value

    @property
    def tracking_code(self):
        """returns the tracking code"""
        return self.__tracking_code

    @property
    def issued_at(self):
        """Returns the issued at value, that is, the time when the order was shipped"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def delivery_day(self):
        """Returns the delivery day for the order"""
        return self.__delivery_day
