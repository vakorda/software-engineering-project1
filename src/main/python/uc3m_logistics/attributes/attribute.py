import re
from uc3m_logistics import OrderManagementException

class Attribute():
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self, value):
        my_regex = re.compile(self._validation_pattern)
        valid = my_regex.fullmatch(value)
        if not valid:
            raise OrderManagementException(self._error_message)

    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._validate(attr_value)
        self._attr_value = attr_value