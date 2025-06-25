def sort_products_by_price(products, reverse=False):
    return sorted(products, key=lambda p: p.price, reverse=reverse)

