import json
from freezegun import freeze_time
from datetime import datetime
from .json_store import JsonStore
from ..exceptions import OrderManagementException
from ..attributes import TrackingCode
from uc3m_logistics.order_manager_config import JSON_FILES_PATH


class OrderShippingStore:

    def __init__(self):
        pass

    @staticmethod
    def save_shipment(shipment):
        """Saves the shipping object into a file"""
        file_name = "shipments_store.json"
        # first read the file
        data_list = JsonStore(file_name).read_json()
        # append the shipments list
        data_list.add_item_dict(shipment)
        data_list.write_json()

    @classmethod
    def get_item_from_tracking_code(cls, tracking_code):  # search item by kwy
        """Check if this tracking_code is in shipments_store"""
        TrackingCode(tracking_code)
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