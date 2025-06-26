import unittest
import os
from data.sample_data import (
    generate_random_model,
    get_sample_products,
    get_sample_stores,
    save_stores_to_json,
    load_stores_from_json,
)


class TestSampleData(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_stores.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_generate_random_model(self):
        model = generate_random_model("Elektronika")
        self.assertTrue(
            model.startswith(("X", "Pro", "Ultra", "Smart", "Master"))
        )
        self.assertTrue(len(model) >= 4)

    def test_get_sample_products(self):
        products = get_sample_products("Elektronika", 3)
        self.assertEqual(len(products), 3)
        for name, model, price in products:
            self.assertIn(
                name, ["Telewizor", "Monitor", "Laptop", "Tablet", "Smartfon"]
            )
            self.assertTrue(isinstance(price, float))

    def test_get_sample_stores(self):
        stores = get_sample_stores()
        self.assertEqual(len(stores), 6)
        self.assertTrue(any(store.name == "MediaMarkt" for store in stores))
        self.assertTrue(all(len(store.products) >= 3 for store in stores))

    def test_save_and_load_stores(self):
        stores = get_sample_stores()
        save_stores_to_json(stores, self.test_file)
        loaded_stores = load_stores_from_json(self.test_file)

        self.assertEqual(len(stores), len(loaded_stores))
        self.assertEqual(stores[0].name, loaded_stores[0].name)
        self.assertEqual(
            len(stores[0].products), len(loaded_stores[0].products)
        )

    def test_load_nonexistent_file(self):
        stores = load_stores_from_json("nonexistent.json")
        self.assertEqual(len(stores), 6)  # Should return sample data
