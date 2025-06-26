import json

from models.product import Product


class Cart:

    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def remove(self, product):
        self.items.remove(product)

    def total(self):
        return sum(p.price for p in self.items)

    def save_to_file(self, filename="cart.txt"):
        with open(filename, "w") as f:
            for p in self.items:
                f.write(f"{p}\n")
            f.write(f"\nRazem: {self.total():.2f} zł")

    def save_to_json(self, filename="cart.json"):
        data = [
            {
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "store_name": p.store_name,
            }
            for p in self.items
        ]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def show(self):
        for p in self.items:
            print(p)
        print(f"\nRazem: {self.total():.2f} zł")

    def load_from_json(self, filename="cart.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.items = [Product(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.items = []  # Brak koszyka to nie błąd
