import unittest
from models.product import Product
from models.store import Store
from main import generate_price_comparison_chart
import matplotlib.pyplot as plt


class TestPriceComparisonIntegration(unittest.TestCase):
    def setUp(self):
        # Create test stores with products
        self.store1 = Store("Store A")
        self.store2 = Store("Store B")

        # Add same product type with different prices
        self.store1.add_product(
            Product("TV", "X100", 2000, "Electronics", "Store A")
        )
        self.store1.add_product(
            Product("TV", "X200", 2500, "Electronics", "Store A")
        )
        self.store2.add_product(
            Product("TV", "X100", 1800, "Electronics", "Store B")
        )
        self.store2.add_product(
            Product("TV", "X300", 2200, "Electronics", "Store B")
        )

        self.stores = [self.store1, self.store2]

    def test_chart_generation(self):
        # Verify function runs without errors
        try:
            generate_price_comparison_chart("TV", self.stores)
            plt.close("all")  # Clean up plots
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Chart generation failed: {str(e)}")

    def test_chart_with_no_products(self):
        # Verify empty case handling
        try:
            generate_price_comparison_chart("Nonexistent", self.stores)
            plt.close("all")
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Empty case handling failed: {str(e)}")
