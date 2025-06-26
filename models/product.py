from dataclasses import dataclass


@dataclass
class Product:
    name: str
    model: str
    price: float
    category: str
    store_name: str

    def __init__(
        self,
        name: str,
        model: str,
        price: float,
        category: str,
        store_name: str,
    ):
        self.name = name
        self.model = model
        self.price = float(price)
        self.category = category
        self.store_name = store_name

    def __repr__(self):
        return f"{self.name} {self.model} ({self.category}) - {self.price:.2f} zł w {self.store_name}"
