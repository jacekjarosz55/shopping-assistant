import unittest
from models.product import Product
from models.limited_edition_product import LimitedProduct


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product(
            "Telewizor", "X123", 1999.99, "Elektronika", "MediaMarkt"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Telewizor")
        self.assertEqual(self.product.model, "X123")
        self.assertEqual(self.product.price, 1999.99)
        self.assertEqual(self.product.category, "Elektronika")
        self.assertEqual(self.product.store_name, "MediaMarkt")

    def test_price_conversion(self):
        product = Product("Test", "M1", 1500, "Test", "TestStore")
        self.assertIsInstance(product.price, float)
        self.assertEqual(product.price, 1500.0)

    def test_repr(self):
        expected = "Telewizor X123 (Elektronika - 1999.99 zł w MediaMarkt"
        self.assertIn(expected, repr(self.product))


class TestLimitedProduct(unittest.TestCase):
    def setUp(self):
        self.product = LimitedProduct(
            "Smartfon", "S20", 3000, "Elektronika", "MediaMarkt"
        )

    def test_discount_applied(self):
        self.assertEqual(self.product.price, 2400)  # 3000 * 0.8

    def test_repr(self):
        self.assertIn("[OFERTA LIMITOWANA -20%]", repr(self.product))
        self.assertIn("2400.00 zł", repr(self.product))
