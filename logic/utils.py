def sort_products_by_price(products, sort_func):
    return sorted(products, key=lambda p: p.price, reverse=(sort_func()))

