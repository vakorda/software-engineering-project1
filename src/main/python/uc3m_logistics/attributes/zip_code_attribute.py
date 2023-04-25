from .attribute import Attribute
from ..order_management_exception import OrderManagementException


class ZipCode(Attribute):
    def __init__(self, attr_value):
        self._error_message = "zip_code format is not valid"
        self.value = attr_value

    def _validate(self, value):
        if value.isnumeric() and len(value) == 5:
            if int(value) > 52999 or int(value) < 1000:
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException(self._error_message)
