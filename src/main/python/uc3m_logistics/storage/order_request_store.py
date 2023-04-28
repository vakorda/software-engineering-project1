import json
from ..exceptions import OrderManagementException
from .json_store import JsonStore
from ..order_manager_config import JSON_FILES_PATH


class OrderRequestStore:
    def __init__(self):
        pass

    @staticmethod
    def save_order(data):
        """Method for saving the order in store"""
        file_name = "orders_store.json"
        # first read the file
        store = JsonStore(file_name)
        store.read_json()

        store.find_by_order_id(data)

        store.write_json()
        return True

    @staticmethod
    def save_order_without_check(data):
        """Method for saving the orders store"""
        orders_store = JSON_FILES_PATH + "orders_store.json"
        with open(orders_store, "r+", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
            data_list.append(data.__dict__)
            file.seek(0)
            json.dump(data_list, file, indent=2)
