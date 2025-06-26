import unittest
from models.product import Product
from logic.utils import sort_products_by_price


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.products = [
            Product("P1", "M1", 300, "Cat1", "Store1"),
            Product("P2", "M2", 100, "Cat2", "Store2"),
            Product("P3", "M3", 200, "Cat3", "Store3"),
        ]

    def test_sort_ascending(self):
        sorted_products = sort_products_by_price(self.products, lambda: False)
        self.assertEqual(sorted_products[0].price, 100)
        self.assertEqual(sorted_products[1].price, 200)
        self.assertEqual(sorted_products[2].price, 300)

    def test_sort_descending(self):
        sorted_products = sort_products_by_price(self.products, lambda: True)
        self.assertEqual(sorted_products[0].price, 300)
        self.assertEqual(sorted_products[1].price, 200)
        self.assertEqual(sorted_products[2].price, 100)
