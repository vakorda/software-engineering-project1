import json
from freezegun import freeze_time
from datetime import datetime
from ..exceptions import OrderManagementException
from ..order_manager_config import JSON_FILES_PATH
from ..attributes import OrderID, Email
from ..models import OrderRequest


class JsonStore:

    def __init__(self, file):
        self._file = file
        self._data_list = []

    def read_json(self):
        full_path = JSON_FILES_PATH + self._file
        try:
            with open(full_path, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            # file is not found, so  init my data_list
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def write_json(self):
        full_path = JSON_FILES_PATH + self._file
        try:
            with open(full_path, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

    def add_dict_item(self, item):
        self._data_list.append(item)

    def find_by_order_id(self, data):
        found = False
        for item in self._data_list:
            if item["_OrderRequest__order_id"] == data.order_id:
                found = True
        if found is False:
            self.add_dict_item(data.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")

    @staticmethod
    def search_order_id(order_id):
        file_store = JSON_FILES_PATH + "orders_store.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == order_id:
                found = True
                # retrieve the orders data
                product_id = item["_OrderRequest__product_id"]
                delivery_address = item["_OrderRequest__delivery_address"]
                order_type = item["_OrderRequest__order_type"]
                phone_number = item["_OrderRequest__phone_number"]
                order_timestamp = item["_OrderRequest__time_stamp"]
                zip_code = item["_OrderRequest__zip_code"]
                # set the time when the order was registered for checking the md5
                with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                    order = OrderRequest(product_id=product_id,
                                         delivery_address=delivery_address,
                                         order_type=order_type,
                                         phone_number=phone_number,
                                         zip_code=zip_code)

                if order.order_id != order_id:
                    raise OrderManagementException("Orders' data have been manipulated")
        if not found:
            raise OrderManagementException("order_id not found")
        return order
