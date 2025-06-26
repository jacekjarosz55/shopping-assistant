import unittest
import io
import sys
from unittest.mock import patch
from main import main as shopping_main


class TestMenuFlowIntegration(unittest.TestCase):
    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def simulate_input(self, inputs):
        with patch("builtins.input", side_effect=inputs):
            try:
                shopping_main()
            except StopIteration:  # For when we simulate exit
                pass

    def test_add_to_cart_flow(self):
        inputs = [
            "2",
            "Laptop",  # Add to cart
            "1",  # Select first product
            "4",  # Show cart
            "0",  # Exit
        ]

        self.simulate_input(inputs)
        output = self.held_output.getvalue()

        # Verify cart contains added product
        self.assertIn("Dodano do koszyka", output)
        self.assertIn("Łączna suma", output)

    def test_product_comparison_flow(self):
        inputs = [
            "8",  # Price comparison
            "1",  # Select first product type
            "0",  # Exit
        ]

        self.simulate_input(inputs)
        output = self.held_output.getvalue()

        # Verify comparison was attempted
        self.assertIn("Wygenerowano wykres", output)
