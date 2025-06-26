import unittest
from models.store import Store
from models.product import Product


class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store("Test Store")
        self.product1 = Product("P1", "M1", 100, "Cat1", "Test Store")
        self.product2 = Product("P2", "M2", 200, "Cat2", "Test Store")

    def test_add_product(self):
        self.store.add_product(self.product1)
        self.assertEqual(len(self.store.products), 1)
        self.assertEqual(self.store.products[0].name, "P1")

    def test_remove_product(self):
        self.store.add_product(self.product1)
        self.store.add_product(self.product2)
        self.store.remove_product(self.product1)
        self.assertEqual(len(self.store.products), 1)
        self.assertEqual(self.store.products[0].name, "P2")

    def test_get_products_no_filter(self):
        self.store.add_product(self.product1)
        self.store.add_product(self.product2)
        products = self.store.get_products()
        self.assertEqual(len(products), 2)

    def test_get_products_with_filter(self):
        self.store.add_product(self.product1)
        self.store.add_product(self.product2)
        products = self.store.get_products("Cat1")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].category, "Cat1")
