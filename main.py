from functools import reduce
from typing import List
from data.sample_data import load_stores_from_json, save_stores_to_json
from logic.cart import Cart
from logic.utils import sort_products_by_price
from models.product import Product
from models.store import Store
import matplotlib.pyplot as plt
import numpy as np
from time import time


def add_done_message(func):
    """Adds a done message to a function"""

    def wrapper():
        func()
        print("Done!")
    return wrapper


def print_cart_sum(cart_items: List[Product]) -> None:
    """Calculate and print the total sum of products in the cart.

    Args:
        cart_items: List of Product objects in the cart
    """
    # using a reduce function to add functional code
    total = reduce(lambda x, y: x + y, map(lambda x: x.price, cart_items), 0)
    print(f"Łączna suma - {total}zł")


def show_cart_recursive(cart_items: List[Product], index: int = 0) -> None:
    """Recursively display the contents of the shopping cart.

    Args:
        cart_items: List of Product objects in the cart
        index: Current index for recursion (default 0)
    """
    if len(cart_items) == 0:
        print("Koszyk jest pusty.\n")
    if index >= len(cart_items):
        print_cart_sum(cart_items)
        return

    assert index < len(cart_items)
    product = cart_items[index]
    print(f"{index + 1}. {product.name} {product.model} - {product.price} zł")

    show_cart_recursive(cart_items, index + 1)


def generate_price_comparison_chart(product_type: str, stores: List[Store]):
    """Generate a price comparison chart for a given product type.

    Args:
        product_type: Name of the product type to compare
        stores: List of Store objects to compare prices from
    """
    products = []
    for store in stores:
        for product in store.products:
            if product.name.lower() == product_type.lower():
                products.append((store.name, product))

    if not products:
        print(
            f"""
        Nie znaleziono produktów typu '{product_type}' w żadnym sklepie.
              """
        )
        return

    stores_products = {}
    models = set()
    for store_name, product in products:
        if store_name not in stores_products:
            stores_products[store_name] = []
        stores_products[store_name].append(product)
        models.add(product.model)

    models = sorted(models)
    num_models = len(models)

    fig, ax = plt.subplots(figsize=(12, 6))
    num_stores = len(stores_products)
    bar_width = 0.8 / num_models
    indices = np.arange(num_stores)

    colors = plt.cm.get_cmap("tab20", num_models)
    model_colors = {model: colors(i) for i, model in enumerate(models)}

    for i, model in enumerate(models):
        model_prices = []
        for store_name in stores_products.keys():
            product = next(
                (p for p in stores_products[store_name] if p.model == model),
                None,
            )
            price = product.price if product else 0
            model_prices.append(price)

        bars = ax.bar(
            indices + i * bar_width,
            model_prices,
            bar_width,
            color=model_colors[model],
            label=model,
        )

        for bar, price in zip(bars, model_prices):
            if price > 0:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f"{model}\n{price:.2f} zł",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

    ax.set_title(f"Porównanie cen produktu: {product_type.capitalize()}")
    ax.set_xlabel("Sklepy")
    ax.set_ylabel("Cena (zł)")
    ax.set_xticks(indices + bar_width * (num_models - 1) / 2)
    ax.set_xticklabels(stores_products.keys(), rotation=45, ha="right")
    ax.legend(title="Modele", bbox_to_anchor=(1.05, 1), loc="upper left")

    min_price = min(
        p.price for p_list in stores_products.values() for p in p_list
    )
    for bar in ax.patches:
        if bar.get_height() == min_price:
            bar.set_edgecolor("limegreen")
            bar.set_linewidth(2)
            bar.set_hatch("//")
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2,
                "NAJTAŃSZY",
                ha="center",
                va="center",
                color="black",
                fontweight="bold",
            )

    plt.tight_layout()
    plt.savefig(f"Wykres_{time()}.png", format="png")
    print("Wygenerowano wykres")
    plt.show()


@add_done_message
def sort_query() -> bool:
    """Get user input for sorting preference.

    Returns:
        bool: False for ascending, True for descending
    """
    while True:
        sort_mode = input("Cena:\n1.Rosnąco\n2.Malejąco\nWybierz opcję:")
        if sort_mode == "1":
            return False
        if sort_mode == "2":
            return True


def show_menu() -> None:
    """Display the main menu options."""
    print("\n=== Asystent Zakupowy ===")
    print("1. Pokaż produkty")
    print("2. Dodaj do koszyka")
    print("3. Usuń z koszyka")
    print("4. Pokaż koszyk")
    print("5. Zapisz koszyk")
    print("6. Dodaj produkt do sklepu")
    print("7. Dodaj sklep")
    print("8. Wygeneruj porównanie dla produktu")
    print("9. Zapisz zmienione dane sklepu")
    print("10. Usuń produkt")
    print("0. Wyjście")


def main() -> None:
    """Main function to run the shopping assistant program."""
    stores = load_stores_from_json()
    cart = Cart()
    cart.load_from_json()

    while True:
        show_menu()
        choice = input("Wybierz opcję: ")
        all_products = [p for store in stores for p in store.get_products()]

        if choice == "1":
            category_filter = input(
                "Kategoria (pozostaw puste by nie filtrować):"
            ).strip()
            product_filter = input(
                "Rodzaj produktu (pozostaw puste by nie filtrować):"
            ).strip()

            products = [p for store in stores for p in store.get_products()]

            if category_filter:
                products = filter(
                    lambda p: p.category.lower() == category_filter.lower(),
                    products,
                )

            if product_filter:
                products = filter(
                    lambda p: p.name.lower() == product_filter.lower(),
                    products,
                )

            products = sort_products_by_price(products, sort_query)

            for product in products:
                print(product)

        elif choice == "2":
            name = input("Podaj nazwę produktu: ").lower()
            matches = [p for p in all_products if p.name.lower() == name]
            if not matches:
                print("Nie znaleziono produktu.")
            else:
                for idx, p in enumerate(matches):
                    print(f"{idx + 1}. {p}")
                try:
                    sel = (
                        int(input("Wybierz numer do dodania do koszyka: ")) - 1
                    )
                    cart.add(matches[sel])
                    print("Dodano do koszyka.")
                except (ValueError, IndexError):
                    print("Niepoprawny wybór.")
                finally:
                    print("Koniec")

        elif choice == "3":
            show_cart_recursive(cart.items)

            if len(cart.items) < 1:
                print("Pusty koszyk.")
                continue

            try:
                index = int(input("Podaj numer produktu do usunięcia: ")) - 1
                cart.remove(index)
            except ValueError:
                print("Niepoprawna wartość.")

        elif choice == "4":
            show_cart_recursive(cart.items)

        elif choice == "5":
            cart.save_to_json()
            print("Zapisano koszyk do pliku.")

        elif choice == "6":
            print("Dostępne sklepy:")
            for idx, store in enumerate(stores):
                print(f"{idx + 1}. {store.name}")

            try:
                store_idx = int(input("Wybierz numer sklepu: ")) - 1
                selected_store = stores[store_idx]

                name = input("Typ Produktu: ")
                model = input("Nazwa produktu: ")
                price = float(input("Cena: "))
                category = input("Kategoria: ")

                new_product = Product(
                    name, model, price, category, selected_store.name
                )
                selected_store.add_product(new_product)
                print(f"Dodano produkt {name} do sklepu {selected_store.name}")
            except (ValueError, IndexError):
                print("Niepoprawny wybór.")

        elif choice == "7":
            name = ""
            while name == "":
                name = input("Podaj nazwę nowego sklepu: ").strip()
                if name == "":
                    print("Proszę podać nazwę")
                elif len([x for x in stores if x.name == name]) > 0:
                    print("Sklep już istnieje")
                    name = ""

            new_store = Store(name)
            stores.append(new_store)
            print(f"Dodano nowy sklep: {name}")

        elif choice == "8":
            product_types = set(p.name for p in all_products)
            print("\nDostępne typy produktów:")
            for i, p_type in enumerate(sorted(product_types), 1):
                print(f"{i}. {p_type}")

            try:
                selection = input(
                    "Wybierz numer typu produktu lub wpisz nazwę: "
                )
                if selection.isdigit():
                    selection = int(selection) - 1
                    selected_type = sorted(product_types)[selection]
                else:
                    selected_type = selection

                generate_price_comparison_chart(selected_type, stores)
            except (ValueError, IndexError):
                print("Niepoprawny wybór.")

        elif choice == "9":
            save_stores_to_json(stores)
            break

        elif choice == "10":
            name = input("Podaj nazwę produktu: ").lower()
            matches = [p for p in all_products if p.name.lower() == name]
            if not matches:
                print("Nie znaleziono produktu.")
            else:
                for idx, p in enumerate(matches):
                    print(f"{idx + 1}. {p}")
                try:
                    sel = int(input("Wybierz numer do usunięcia: ")) - 1
                    selected_store = [
                        s for s in stores if matches[sel].store_name == s.name
                    ][0]
                    selected_store.remove_product(matches[sel])
                    all_products.remove(matches[sel])
                except (ValueError, IndexError):
                    print("Niepoprawny wybór.")
        elif choice == "0":
            print("Do zobaczenia!")
            break
        else:
            print("Nieznana opcja.")


if __name__ == "__main__":
    main()
