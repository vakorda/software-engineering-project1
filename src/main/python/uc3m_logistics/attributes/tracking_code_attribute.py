from .attribute import Attribute
from uc3m_logistics import OrderManagementException


class Address(Attribute):
    def __init__(self, attr_value):
        self._error_message = "tracking_code format is not valid"
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._attr_value = attr_value
