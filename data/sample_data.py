from dataclasses import asdict
import json
import random
from typing import List
from models.limited_edition_product import LimitedProduct
from models.product import Product
from models.store import Store


def generate_random_model(category: str) -> str:
    """Generuje losową nazwę modelu na podstawie kategorii produktu"""
    model_prefixes = {
        "Elektronika": ["X", "Pro", "Ultra", "Smart", "Master"],
        "AGD": ["Eco", "Power", "Clean", "Fresh", "Quick"],
        "Audio": ["Sound", "Bass", "Acoustic", "Wave", "Audio"],
        "Foto/Video": ["Lens", "Shot", "Focus", "Pixel", "Frame"],
        "Gaming": ["Game", "Pro", "Elite", "Tactical", "Extreme"],
        "Wearables": ["Fit", "Track", "Pulse", "Step", "Health"],
        "Sport": ["Active", "Run", "Jump", "Sport", "Pro"],
        "Fitness": ["Power", "Flex", "Core", "Fit", "Strong"],
        "Książki": ["Edition", "Print", "Volume", "Series", "Collection"],
        "Zabawki": ["Fun", "Play", "Joy", "Kids", "Toy"],
        "Moda": ["Style", "Urban", "Classic", "Trend", "Fashion"],
    }

    numbers = random.randint(100, 999)
    letters = random.choice("ABCDEFGH")
    prefix = random.choice(model_prefixes.get(category, ["Standard"]))
    return f"{prefix}{numbers}{letters}"


def get_sample_products(category: str, count: int):
    """Generuje listę produktów danej kategorii"""
    product_templates = {
        "Elektronika": [
            "Telewizor",
            "Monitor",
            "Laptop",
            "Tablet",
            "Smartfon",
        ],
        "AGD": ["Lodówka", "Pralka", "Zmywarka", "Piekarnik", "Odkurzacz"],
        "Audio": [
            "Słuchawki",
            "Głośnik",
            "Soundbar",
            "System audio",
            "Mikrofon",
        ],
        "Foto/Video": [
            "Aparat",
            "Kamera",
            "Obiektyw",
            "Statyw",
            "Lampa studyjna",
        ],
        "Gaming": [
            "Klawiatura",
            "Mysz",
            "Kontroler",
            "Słuchawki",
            "Podkładka",
        ],
        "Wearables": [
            "Smartwatch",
            "Opaska",
            "Słuchawki",
            "Monitor",
            "Okulary",
        ],
        "Sport": ["Rower", "Buty", "Kask", "Rakieta", "Hulajnoga"],
        "Fitness": ["Hantle", "Mata", "Steper", "Ławka", "Gumy"],
        "Książki": ["Książka", "Podręcznik", "Album", "Poradnik", "Słownik"],
        "Zabawki": ["Lalka", "Samochód", "Klocki", "Gra", "Puzzle"],
        "Moda": ["Koszulka", "Spodnie", "Buty", "Kurtka", "Czapka"],
    }

    products = []
    templates = product_templates.get(category, ["Produkt"])

    for _ in range(count):
        name = random.choice(templates)
        model = generate_random_model(category)
        price = round(
            random.uniform(
                50 if category in ["Książki", "Zabawki"] else 200,
                5000 if category in ["Elektronika", "AGD"] else 1000,
            ),
            2,
        )

        products.append((name, model, price))

    return products


def get_sample_stores() -> List[Store]:
    """Tworzy przykładowe sklepy z produktami"""
    stores = [
        Store("MediaMarkt"),
        Store("RTV Euro AGD"),
        Store("Komputronik"),
        Store("Neonet"),
        Store("Decathlon"),
        Store("Empik"),
    ]

    # Przypisanie produktów do sklepów według kategorii
    categories = {
        "MediaMarkt": ["Elektronika", "AGD", "Audio"],
        "RTV Euro AGD": ["Elektronika", "AGD", "Foto/Video"],
        "Komputronik": ["Elektronika", "Gaming"],
        "Neonet": ["AGD", "Wearables"],
        "Decathlon": ["Sport", "Fitness"],
        "Empik": ["Książki", "Zabawki", "Moda"],
    }

    for store in stores:
        for category in categories[store.name]:
            products_data = get_sample_products(category, random.randint(3, 6))
            for name, model, price in products_data:
                if random.random() < 0.25:
                    store.add_product(
                        LimitedProduct(
                            name, model, price, category, store.name
                        )
                    )
                else:
                    store.add_product(
                        Product(name, model, price, category, store.name)
                    )

    return stores


def save_stores_to_json(
    stores: List[Store], filename: str = "stores_data.json"
):
    """Zapisuje listę sklepów z produktami do pliku JSON"""
    data = {
        "stores": [
            {
                "name": store.name,
                "products": [
                    asdict(product)
                    | {"limited": isinstance(product, LimitedProduct)}
                    for product in store.products
                ],
            }
            for store in stores
        ]
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_stores_from_json(filename: str = "stores_data.json") -> List[Store]:
    """Wczytuje listę sklepów z produktami z pliku JSON"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        stores = []
        for store_data in data["stores"]:
            store = Store(store_data["name"])
            for product_data in store_data["products"]:
                product = Product(
                    name=product_data["name"],
                    model=product_data["model"],
                    category=product_data["category"],
                    price=product_data["price"],
                    store_name=product_data["store_name"],
                )
                store.add_product(product)
            stores.append(store)

        return stores
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje. Używam domyślnych danych.")
        return get_sample_stores()
    except json.JSONDecodeError:
        print(f"Błąd w formacie pliku {filename}. Używam domyślnych danych.")
        return get_sample_stores()
    except KeyError as e:
        print(f"Brak pola w pliku JSON: {e}. Używam domyślnych danych.")
        return get_sample_stores()
