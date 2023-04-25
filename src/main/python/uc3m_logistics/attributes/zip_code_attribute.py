from .attribute import Attribute
from uc3m_logistics import OrderManagementException


class Address(Attribute):
    def __init__(self, attr_value):
        self._error_message = "zip_code is not valid" # También se usa "zip_code format is not valid"
        self._validation_pattern = "??"
        self._attr_value = attr_value
