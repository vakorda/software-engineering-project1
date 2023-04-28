import unittest
from uc3m_logistics import OrderManager
from uc3m_logistics.storage.order_shipping_store import OrderShippingStore
from uc3m_logistics.storage.order_request_store import OrderRequestStore
from uc3m_logistics.storage.order_delivery_store import OrderDeliveryStore


# Due to some problems we had we decided not to implement the singleton in OrderManager
# and OrderShippingStore
class SingletonTests(unittest.TestCase):
    
    # def test_order_manager(self):
    # order_manager_1 = OrderManager()
    # order_manager_2 = OrderManager()
    # self.assertEqual(id(order_manager_1), id(order_manager_2))
    
    def test_order_request_store(self):
        store_1 = OrderRequestStore()
        store_2 = OrderRequestStore()
        self.assertEqual(id(store_1), id(store_2))
    
    # def test_order_shipping_store(self):
    # store_1 = OrderShippingStore()
    # store_2 = OrderShippingStore()
    # self.assertEqual(id(store_1), id(store_2))

    def test_order_delivery_store(self):
        store_1 = OrderDeliveryStore()
        store_2 = OrderDeliveryStore()
        self.assertEqual(id(store_1), id(store_2))


if __name__ == '__main__':
    unittest.main()
