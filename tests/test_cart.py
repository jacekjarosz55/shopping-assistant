import unittest
import os
from models.product import Product
from logic.cart import Cart


class TestCart(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.product1 = Product("P1", "M1", 100, "Cat1", "Store1")
        self.product2 = Product("P2", "M2", 200, "Cat2", "Store2")
        self.test_json = "test_cart.json"

    def tearDown(self):
        if os.path.exists(self.test_json):
            os.remove(self.test_json)

    def test_add_product(self):
        self.cart.add(self.product1)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].name, "P1")

    def test_remove_product(self):
        self.cart.add(self.product1)
        self.cart.add(self.product2)
        self.cart.remove(self.product1)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].name, "P2")

    def test_total(self):
        self.cart.add(self.product1)
        self.cart.add(self.product2)
        self.assertEqual(self.cart.total(), 300)

    def test_save_and_load_json(self):
        self.cart.add(self.product1)
        self.cart.add(self.product2)
        self.cart.save_to_json(self.test_json)

        new_cart = Cart()
        new_cart.load_from_json(self.test_json)

        self.assertEqual(len(new_cart.items), 2)
        self.assertEqual(new_cart.items[0].name, "P1")
        self.assertEqual(new_cart.items[1].name, "P2")

    def test_load_nonexistent_file(self):
        new_cart = Cart()
        new_cart.load_from_json("nonexistent.json")
        self.assertEqual(len(new_cart.items), 0)
