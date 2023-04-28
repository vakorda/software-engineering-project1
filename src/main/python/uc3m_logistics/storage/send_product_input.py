import json
from ..exceptions import OrderManagementException
from ..attributes import Email, OrderID
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from ..storage import JsonStore


class SendProductInput:
    def __init__(self, input_file):
        self.data = self.get_data_from_input(input_file)
        self._email = Email(self.data["ContactEmail"]).value
        self._order_id = OrderID(self.data["OrderID"]).value

    @staticmethod
    def get_data_from_input(input_file):
        data = JsonStore(input_file).read_shipment()

        # check all the information
        try:
            OrderID(data["OrderID"])
            Email(data["ContactEmail"])
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex
        return data


    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = Email(value).value

    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def order_id(self, value):
        self._order_id = OrderID(value)