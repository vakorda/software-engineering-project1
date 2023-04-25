from .attribute import Attribute
from uc3m_logistics import OrderManagementException


class Address(Attribute):
    def __init__(self, attr_value):
        self._error_message = "order_type is not valid"
        self._validation_pattern = r"(Regular|Premium)"
        self._attr_value = attr_value
        