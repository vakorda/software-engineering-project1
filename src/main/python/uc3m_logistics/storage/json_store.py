import json
from freezegun import freeze_time
from datetime import datetime
from ..exceptions import OrderManagementException
from ..order_manager_config import JSON_FILES_PATH
from ..attributes import OrderID, Email


class JsonStore:

    def __init__(self, file=None):
        self._file = file
        self._data_list = []

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @property
    def data_list(self):
        return self._data_list

    @data_list.setter
    def data_list(self, value):
        self._data_list = value

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

