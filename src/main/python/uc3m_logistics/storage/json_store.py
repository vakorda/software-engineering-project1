import json
from uc3m_logistics.exceptions.order_management_exception import OrderManagementException
from ..order_manager_config import JSON_FILES_PATH
from uc3m_logistics.singleton_metaclass import SingletonMeta
from uc3m_logistics.order_manager_config import JSON_FILES_PATH


class JsonStore(metaclass=SingletonMeta):

    # singleton> class __JsonStore:  # all the code of the class inside
    # singleton>
    # singleton> instance = None # no instance of the inner class
    # singleton>     def __new__(cls):
    # singleton>         if not JsonStore.instance:
    # singleton>             JsonStore.instance = JsonStore.__JsonStore()
    # singleton>         return JsonStore.instance

    # P> _FILE_PATH = None
    def __init__(self, file):
        self._file = JSON_FILES_PATH + file
        self._data_list = []
        self.read_json()
        pass

    # P> not static
    def write_json(self):  # P> save
        try:
            with open(self._file, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

    def read_json(self):
        try:
            with open(self._file, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            # file is not found, so  init my data_list
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        # return data_list

    def read_shipment(self):
        try:
            with open(self._file, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def add_item_dict(self, item):
        self._data_list.append(item.__dict__)

    def add_item(self, item):
        self._data_list.append(item)