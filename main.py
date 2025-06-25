from data.sample_data import get_sample_stores
from logic.cart import Cart
from logic.utils import sort_products_by_price

def show_menu():
    print("\n=== Asystent Zakupowy ===")
    #print("-1. Pokaż wszystkie produkty")
    #print("0. Filtruj po kategorii")
    print("1. Pokaż produkty")
    print("2. Dodaj do koszyka")
    print("3. Usuń z koszyka")
    print("4. Pokaż koszyk")
    print("5. Zapisz koszyk")
    print("0. Wyjście")

def main():
    stores = get_sample_stores()
    cart = Cart()
    cart.load_from_json()


    while True:
        show_menu()
        choice = input("Wybierz opcję: ")
        all_products = [p for store in stores for p in store.get_products()]

        # pokaż produkty
        if choice == "1":

            sort_desc = None
            category_filter = ""
            while True:
                sort_mode = input("Cena:\n1.Rosnąco\n2.Malejąco\nWybierz opcję:")
                if sort_mode == "1":
                    sort_desc = False
                    break
                if sort_mode == "2":
                    sort_desc = True
                    break

            category_filter = input("Kategoria (pozostaw puste by nie filtrować):").strip()


            products = [p for store in stores for p in store.get_products()]
            
            if len(category_filter) > 0:
                products = [p for p in products if p.category.lower() == category_filter.lower()]

            if sort_desc is not None:
                products = sort_products_by_price(products, sort_desc)


            for product in products:
                print(product)


        # Dodaj 
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
            cart.show()

            if len(cart.items) < 1:
                print("Pusty koszyk.")
                continue

            try:
                index = int(input("Podaj numer produktu do usunięcia: ")) - 1
                cart.remove(index)
            except ValueError:
                print("Niepoprawna wartość.")
        elif choice == "4":
            cart.show()

        elif choice == "5":
            cart.save_to_json()
            print("Zapisano koszyk do pliku.")

        elif choice == "0":
            print("Do zobaczenia!")
            break
        else:
            print("Nieznana opcja.")

if __name__ == "__main__":
    main()

