import unittest
from models.product import Product
from models.store import Store
from logic.cart import Cart


class TestCartIntegration(unittest.TestCase):
    def setUp(self):
        self.store = Store("Test Store")
        self.product1 = Product(
            "TV", "X100", 2000, "Electronics", "Test Store"
        )
        self.product2 = Product(
            "Laptop", "Y200", 3000, "Electronics", "Test Store"
        )
        self.store.add_product(self.product1)
        self.store.add_product(self.product2)
        self.cart = Cart()

    def test_add_product_from_store_to_cart(self):
        # Get product from store
        store_product = self.store.get_products()[0]

        # Add to cart
        self.cart.add(store_product)

        # Verify
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].name, "TV")
        self.assertEqual(self.cart.total(), 2000)

    def test_remove_product_and_verify_in_store(self):
        # Add both products to cart
        self.cart.add(self.store.get_products()[0])
        self.cart.add(self.store.get_products()[1])

        # Remove one product
        self.cart.remove(self.cart.items[0])

        # Verify
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].name, "Laptop")

        # Verify store still has both products
        self.assertEqual(len(self.store.get_products()), 2)

    def test_cart_total_with_multiple_products(self):
        # Add products to cart
        self.cart.add(self.product1)
        self.cart.add(self.product2)

        # Verify total
        self.assertEqual(self.cart.total(), 5000)
