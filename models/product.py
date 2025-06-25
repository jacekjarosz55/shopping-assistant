class Product:
    def __init__(self, name, category, price, store_name):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Cena musi być liczbą dodatnią.")
        self.name = name
        self.category = category
        self.price = price
        self.store_name = store_name

    def __repr__(self):
        return f"{self.name} ({self.category}) - {self.price:.2f} zł w {self.store_name}"

