import json
from datetime import datetime
from .json_store import JsonStore
from ..exceptions import OrderManagementException
from ..order_manager_config import JSON_FILES_PATH
from ..singleton_metaclass import SingletonMeta


class OrderDeliveryStore(JsonStore, metaclass=SingletonMeta):

    @staticmethod
    def search_tracking_code(tracking_code):
        """Check if this tracking_code is in shipments_store"""
        shipments_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shipments_store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException("shipments_store not found") from ex
        # search this tracking_code
        for item in data_list:
            if item["_OrderShipping__tracking_code"] == tracking_code:
                return item
        raise OrderManagementException("tracking_code is not found")

    @classmethod
    def add_delivery(cls, tracking_code):
        file_name = "shipments_delivered.json"
        store = JsonStore(file_name)
        store.read_json()
        # append the delivery info
        store.add_dict_item(str(tracking_code))
        store.add_dict_item(str(datetime.utcnow()))
        store.write_json()

