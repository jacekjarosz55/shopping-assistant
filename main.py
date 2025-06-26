from functools import reduce
from data.sample_data import load_stores_from_json, save_stores_to_json
from logic.cart import Cart
from logic.utils import sort_products_by_price
from models.product import Product
from models.store import Store
import matplotlib.pyplot as plt  # Dodany import
import numpy as np

def print_cart_sum(cart_items):
    sum = reduce(lambda x,y: x+y, map(lambda x: x.price, cart_items), 0)
    print(f"Łączna suma - {sum}zł")
def show_cart_recursive(cart_items, index=0):
    """Rekurencyjne wyświetlanie zawartości koszyka"""

    if len(cart_items) == 0:
        print("Koszyk jest pusty.\n")
    if index >= len(cart_items):  # Warunek zakończenia rekurencji
        print_cart_sum(cart_items)
        return
    
    assert index < len(cart_items)
    product = cart_items[index]
    print(f"{index+1}. {product.name} {product.model} - {product.price} zł")
    
    # Rekurencyjne wywołanie dla następnego produktu
    show_cart_recursive(cart_items, index + 1)



def generate_price_comparison_chart(product_type: str, stores: list[Store]):
    """Generuje wykres porównania cen dla danego typu produktu z grupowaniem słupków"""
    # Zbierz wszystkie produkty danego typu
    products = []
    for store in stores:
        for product in store.products:
            if product.name.lower() == product_type.lower():
                products.append((store.name, product))
    
    if not products:
        print(f"Nie znaleziono produktów typu '{product_type}' w żadnym sklepie.")
        return
    
    # Przygotuj dane do wykresu
    stores_products = {}
    models = set()
    for store_name, product in products:
        if store_name not in stores_products:
            stores_products[store_name] = []
        stores_products[store_name].append(product)
        models.add(product.model)
    
    models = sorted(models)  # Sortuj modele dla spójności
    num_models = len(models)
    
    # Utwórz wykres z grupowanymi słupkami
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Parametry wykresu
    num_stores = len(stores_products)
    bar_width = 0.8 / num_models  # Szerokość słupka
    indices = np.arange(num_stores)
    
    # Generuj unikalne kolory dla każdego modelu
    colors = plt.cm.get_cmap('tab20', num_models)
    model_colors = {model: colors(i) for i, model in enumerate(models)}
    
    # Rysuj słupki dla każdego modelu w każdym sklepie
    for i, model in enumerate(models):
        model_prices = []
        for store_name in stores_products.keys():
            # Znajdź produkt danego modelu w sklepie
            product = next((p for p in stores_products[store_name] if p.model == model), None)
            price = product.price if product else 0
            model_prices.append(price)
        
        bars = ax.bar(indices + i * bar_width, model_prices, bar_width,
                     color=model_colors[model],
                     label=model)
        
        # Dodaj etykiety cen i modeli na słupkach
        for bar, price in zip(bars, model_prices):
            if price > 0:  # Tylko dla istniejących produktów
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height,
                       f'{model}\n{price:.2f} zł',
                       ha='center', va='bottom', fontsize=8)
    
    # Konfiguracja wykresu
    ax.set_title(f'Porównanie cen produktu: {product_type.capitalize()}')
    ax.set_xlabel('Sklepy')
    ax.set_ylabel('Cena (zł)')
    ax.set_xticks(indices + bar_width * (num_models - 1) / 2)
    ax.set_xticklabels(stores_products.keys(), rotation=45, ha='right')
    
    # Dodaj legendę
    ax.legend(title='Modele', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Znajdź i zaznacz najtańszy produkt
    min_price = min(p.price for p_list in stores_products.values() for p in p_list)
    for bar in ax.patches:
        if bar.get_height() == min_price:
            bar.set_edgecolor('limegreen')
            bar.set_linewidth(2)
            bar.set_hatch('//')
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                   'NAJTAŃSZY',
                   ha='center', va='center', color='black', fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    plt.draw


def sort_query():
    while True:
        sort_mode = input("Cena:\n1.Rosnąco\n2.Malejąco\nWybierz opcję:")
        if sort_mode == "1":
            return False
        if sort_mode == "2":
            return True

def generate_price_comparison_chart_bak(product_type: str, stores: list[Store]):
    """Generuje wykres porównania cen dla danego typu produktu"""
    # Zbierz wszystkie produkty danego typu
    products = []
    for store in stores:
        for product in store.products:
            if product.name.lower() == product_type.lower():
                products.append((store.name, product))
    
    if not products:
        print(f"Nie znaleziono produktów typu '{product_type}' w żadnym sklepie.")
        return
    
    # Przygotuj dane do wykresu
    store_names = []
    prices = []
    models = []
    
    for store_name, product in products:
        store_names.append(store_name)
        prices.append(product.price)
        models.append(product.model)
    
    # Utwórz wykres
    plt.figure(figsize=(12, 6))
    bars = plt.bar(store_names, prices, color='red')
    
    # Dodaj etykiety i tytuł
    plt.title(f'Porównanie cen produktu: {product_type.capitalize()}')
    plt.xlabel('Sklepy')
    plt.ylabel('Cena (zł)')
    plt.xticks(rotation=45, ha='right')
    
    # Dodaj wartości cen na słupkach
    for bar, price, model in zip(bars, prices, models):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{price:.2f} zł - {model}',
                ha='center', va='bottom', fontsize=9)
    
    # Znajdź i zaznacz najtańszy produkt
    min_price = min(prices)
    min_index = prices.index(min_price)
    bars[min_index].set_color('lightgreen')
    
    plt.tight_layout()
    plt.show()

def show_menu():
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

all_products = []

def main():
    stores = load_stores_from_json()
    cart = Cart()
    cart.load_from_json()

    while True:
        show_menu()
        choice = input("Wybierz opcję: ")
        all_products = [p for store in stores for p in store.get_products()]

        if choice == "1":
            category_filter = input("Kategoria (pozostaw puste by nie filtrować):").strip()
            product_filter = input("Rodzaj produktu (pozostaw puste by nie filtrować):").strip()

            products = [p for store in stores for p in store.get_products()]
            
            if len(category_filter) > 0:
                products = filter(lambda p: p.category.lower() == category_filter.lower(), products)

            if len(product_filter) > 0:
                products = filter(lambda p: p.name.lower() == product_filter.lower(), products)

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
                    print(f"{idx+1}. {p}")
                try:
                    sel = int(input("Wybierz numer do dodania do koszyka: ")) - 1
                    cart.add(matches[sel])
                    print("Dodano do koszyka.")
                except (ValueError, IndexError):
                    print("Niepoprawny wybór.")

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
                print(f"{idx+1}. {store.name}")
            
            try:
                store_idx = int(input("Wybierz numer sklepu: ")) - 1
                selected_store = stores[store_idx]
                
                name = input("Typ Produktu: ")
                model = input("Nazwa produktu: ")
                price = float(input("Cena: "))
                category = input("Kategoria: ")

                new_product = Product(name, model, price, category, selected_store.name)
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
            # Wyświetl dostępne typy produktów
            product_types = set(p.name for p in all_products)
            print("\nDostępne typy produktów:")
            for i, p_type in enumerate(sorted(product_types), 1):
                print(f"{i}. {p_type}")
            
            try:
                selection = input("Wybierz numer typu produktu lub wpisz nazwę: ")
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
                    print(f"{idx+1}. {p}")
                try:
                    sel = int(input("Wybierz numer do usunięcia: ")) - 1
                    selected_store = [s for s in stores if matches[sel].store_name == s.name][0]
                    selected_store.remove_product(matches[sel])
                    all_products.remove(matches[sel])
                    print("Dodano do koszyka.")
                except (ValueError, IndexError):
                    print("Niepoprawny wybór.")
        elif choice == "0":
            print("Do zobaczenia!")
            break
        else:
            print("Nieznana opcja.")

if __name__ == "__main__":
    main()
