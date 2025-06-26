import unittest
from models.product import Product
from models.limited_edition_product import LimitedProduct
from models.store import Store
from data.sample_data import get_sample_stores


class TestStoreProductIntegration(unittest.TestCase):
    def setUp(self):
        self.store = Store("Test Store")
        self.regular_product = Product(
            "TV", "X100", 2000, "Electronics", "Test Store"
        )
        self.limited_product = LimitedProduct(
            "Laptop", "Y200", 3000, "Electronics", "Test Store"
        )

    def test_add_both_product_types_to_store(self):
        self.store.add_product(self.regular_product)
        self.store.add_product(self.limited_product)

        products = self.store.get_products()
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].price, 2000)
        self.assertEqual(products[1].price, 2400)  # 3000 * 0.8

    def test_sample_data_integration(self):
        stores = get_sample_stores()
        electronics_store = next(s for s in stores if "MediaMarkt" in s.name)

        # Verify store has products
        self.assertGreater(len(electronics_store.get_products()), 0)

        # Verify some products might be limited edition
        has_limited = any(
            "[OFERTA LIMITOWANA" in repr(p)
            for p in electronics_store.get_products()
        )
        self.assertTrue(has_limited)
