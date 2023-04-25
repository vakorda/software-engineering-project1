from .attribute import Attribute


class Email(Attribute):
    def __init__(self, attr_value):
        self._error_message = "contact email is not valid"
        self._validation_pattern = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
        self.value = attr_value