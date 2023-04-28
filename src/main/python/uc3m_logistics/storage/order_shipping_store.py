from .json_store import JsonStore
import json
from ..exceptions import OrderManagementException
from ..attributes import OrderID, Email
from ..models import OrderShipping


class OrderShippingStore(JsonStore):

    def read_json(self):
        try:
            with open(self._file, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def find_order_from_shipment(self):
        try:
            OrderID(self._data_list["OrderID"])  # TODO
            Email(self._data_list["ContactEmail"])  # TODO
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex
        order = self.search_order_id(self._data_list["OrderID"])
        return order


    def get_order_shipping(self):
        # check all the information
        order = self.find_order_from_shipment()

        return OrderShipping(product_id=order.product_id,
                                    order_id=self._data_list["OrderID"],
                                    order_type=order.order_type,
                                    delivery_email=self._data_list["ContactEmail"])