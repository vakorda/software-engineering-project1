"""Module """
import datetime
import re
import json
from datetime import datetime
from freezegun import freeze_time
from .order_request import OrderRequest
from .order_management_exception import OrderManagementException
from .order_shipping import OrderShipping
from .order_manager_config import JSON_FILES_PATH


class OrderManager:
    """Class for providing the methods for managing the orders process"""
    def __init__(self):
        pass

    def validate_ean13(self, ean13):
        """Method for validating a ean13 code"""
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE EAN13
        # RETURN TRUE IF THE EAN13 IS RIGHT, OR FALSE IN OTHER CASE
        checksum = 0
        code_read = -1
        valid = False
        self.check_regex(ean13, r'^[0-9]{13}$', "Invalid EAN13 code string")

        for i, digit in enumerate(reversed(ean13)):
            try:
                current_digit = int(digit)
            except ValueError as v_e:
                raise OrderManagementException("Invalid EAN13 code string") from v_e
            if i == 0:
                code_read = current_digit
            else:
                checksum += current_digit * 3 if (i % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10

        if (code_read != -1) and (code_read == control_digit):
            valid = True
        else:
            raise OrderManagementException("Invalid EAN13 control digit")
        return valid

    def validate_tracking_code(self, tracking_code):
        """Method for validating sha256 values"""
        self.check_regex(tracking_code, r"[0-9a-fA-F]{64}$", "tracking_code format is not valid")

    def save_order(self, data):
        """Method for saving the order in store"""
        file_name = "orders_store.json"
        # first read the file
        data_list = self.read_json(file_name)

        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == data.order_id:
                found = True
        if found is False:
            data_list.append(data.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")

        self.write_json(file_name, data_list)
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

    def save_shipment(self, shipment):
        """Saves the shipping object into a file"""
        file_name = "shipments_store.json"
        # first read the file
        data_list = self.read_json(file_name)
        # append the shipments list
        data_list.append(shipment.__dict__)
        self.write_json(file_name, data_list)

    # pylint: disable=too-many-arguments
    def register_order(self, product_id,  # TODO: TOO MANY ARGUMENTS
                       order_type,
                       address,
                       phone_number,
                       zip_code):
        """Register the orders into the order's file"""
        self.validate_order_type(order_type)
        self.validate_address(address)
        self.validate_phone_number(phone_number)
        self.validate_zip_code(zip_code)
        if self.validate_ean13(product_id):
            my_order = OrderRequest(product_id,
                                    order_type,
                                    address,
                                    phone_number,
                                    zip_code)

        self.save_order(my_order)  # TODO: my_order may be referenced before asignament

        return my_order.order_id

    @staticmethod
    def validate_zip_code(zip_code):
        if zip_code.isnumeric() and len(zip_code) == 5:
            if int(zip_code) > 52999 or int(zip_code) < 1000:
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")

    def validate_phone_number(self, phone_number):
        self.check_regex(phone_number, r"^(\+)[0-9]{11}", "phone number is not valid")

    def validate_address(self, address):
        regex_address = r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$"
        self.check_regex(address, regex_address, "address is not valid")

    def validate_order_type(self, order_type):
        self.check_regex(order_type, r"(Regular|Premium)", "order_type is not valid")

    # pylint: disable=too-many-locals
    def send_product(self, input_file):
        """Sends the order included in the input_file"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # check all the information
        try:
            self.validate_order_id(data["OrderID"])
            self.validate_email(data["ContactEmail"])
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex

        order = self.search_order_id(data["OrderID"])

        my_shipment = OrderShipping(product_id=order.product_id,
                                    order_id=data["OrderID"],
                                    order_type=order.order_type,
                                    delivery_email=data["ContactEmail"])

        # save the OrderShipping in shipments_store.json
        self.save_shipment(my_shipment)

        return my_shipment.tracking_code

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

    def validate_email(self, email):
        regex_email = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
        self.check_regex(email, regex_email, "contact email is not valid")

    def validate_order_id(self, order_id):
        self.check_regex(order_id, r"[0-9a-fA-F]{32}$", "order id is not valid")

    def deliver_product(self, tracking_code):
        """Register the delivery of the product"""
        self.validate_tracking_code(tracking_code)
        item = self.search_tracking_code(tracking_code)

        delivery_day = item["_OrderShipping__delivery_day"]
        self.check_delivery_day(delivery_day)

        file_name = "shipments_delivered.json"

        data_list = self.read_json(file_name)

        # append the delivery info
        data_list.append(str(tracking_code))
        data_list.append(str(datetime.utcnow()))
        self.write_json(file_name, data_list)
        return True

    @staticmethod
    def check_delivery_day(delivery_day):
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(delivery_day).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

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

    @staticmethod
    def read_json(file_name):
        full_path = JSON_FILES_PATH + file_name
        try:
            with open(full_path, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found, so  init my data_list
            data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data_list

    @staticmethod
    def write_json(file_name, data_list):
        full_path = JSON_FILES_PATH + file_name
        try:
            with open(full_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

    @staticmethod
    def check_regex(variable, regex, message):
        my_regex = re.compile(regex)
        valid = my_regex.fullmatch(variable)
        if not valid:
            raise OrderManagementException(message)
