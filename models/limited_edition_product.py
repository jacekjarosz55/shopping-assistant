from models.product import Product


class LimitedProduct(Product):
    def __init__(
        self,
        name,
        model,
        price,
        category,
        store_name,
    ):
        super().__init__(name, model, price * 0.8, category, store_name)

    def __repr__(self):
        return (
            f"[OFERTA LIMITOWANA -20%]"
            f" - {self.name} {self.model} ({self.category})"
            f"- {self.price:.2f} zł w {self.store_name}"
        )
