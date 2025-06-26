class Store:
    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_products(self, category_filter=None):
        if category_filter:
            return [p for p in self.products if p.category == category_filter]
        return self.products
