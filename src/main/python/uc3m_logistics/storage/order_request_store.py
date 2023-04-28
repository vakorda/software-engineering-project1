import json
from freezegun import freeze_time
from ..exceptions import OrderManagementException
from datetime import datetime
from .json_store import JsonStore
from uc3m_logistics.order_manager_config import JSON_FILES_PATH


class OrderRequestStore:
    def __init__(self):
        pass

    @staticmethod
    def save_order(data):
        """Method for saving the order in store"""
        file_name = "orders_store.json"
        # first read the file
        data_list = JsonStore.read_json(file_name)

        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == data.order_id:
                found = True
        if found is False:
            data_list.append(data.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")

        JsonStore.write_json(file_name, data_list)
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