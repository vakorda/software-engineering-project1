from .attribute import Attribute
from uc3m_logistics import OrderManagementException


class Address(Attribute):
    def __init__(self, attr_value):
        self._error_message = "address is not valid"
        self._validation_pattern = r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$"
        self._attr_value = attr_value
