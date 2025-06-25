import unittest
import os
import json

from logic.cart import Cart
from models.product import Product
from logic.utils import sort_products_by_price

class TestCart(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.product1 = Product("Laptop", "Elektronika", 3000.0, "Sklep A")
        self.product2 = Product("Telefon", "Elektronika", 1500.0, "Sklep B")
        self.filename = "test_cart.json"

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_product(self):
        self.cart.add(self.product1)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].name, "Laptop")

    def test_total_price(self):
        self.cart.add(self.product1)
        self.cart.add(self.product2)
        self.assertEqual(self.cart.total(), 4500.0)

    def test_save_and_load_json(self):
        self.cart.add(self.product1)
        self.cart.save_to_json(self.filename)

        # nowy koszyk, sprawdź czy wczyta dane
        new_cart = Cart()
        new_cart.load_from_json(self.filename)

        self.assertEqual(len(new_cart.items), 1)
        self.assertEqual(new_cart.items[0].name, "Laptop")

    def test_sort_products_by_price(self):
        p1 = Product("A", "Kat", 200.0, "Sklep A")
        p2 = Product("B", "Kat", 50.0, "Sklep B")
        p3 = Product("C", "Kat", 300.0, "Sklep C")
        sorted_list = sort_products_by_price([p1, p2, p3])
        self.assertEqual([p.name for p in sorted_list], ["B", "A", "C"])

if __name__ == "__main__":
    unittest.main()

