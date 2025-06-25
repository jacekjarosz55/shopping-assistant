from models.product import Product
from models.store import Store

def get_sample_stores():
    store1 = Store("MediaMarkt")
    store2 = Store("RTV Euro AGD")
    store3 = Store("Komputronik")
    store4 = Store("Neonet")
    store5 = Store("Decathlon")
    store6 = Store("Empik")

    store1.add_product(Product("Telewizor", "Elektronika", 2500, store1.name))
    store1.add_product(Product("Zmywarka", "AGD", 1600, store1.name))
    store1.add_product(Product("Głośnik Bluetooth", "Audio", 400, store1.name))
    store1.add_product(Product("Słuchawki bezprzewodowe", "Audio", 350, store1.name))

    store2.add_product(Product("Lodówka", "AGD", 1800, store2.name))
    store2.add_product(Product("Mikrofalówka", "AGD", 700, store2.name))
    store2.add_product(Product("Kamera sportowa", "Foto/Video", 900, store2.name))
    store2.add_product(Product("Robot sprzątający", "AGD", 1300, store2.name))

    store3.add_product(Product("Karta graficzna", "Elektronika", 2200, store3.name))
    store3.add_product(Product("Router", "Sieci", 300, store3.name))
    store3.add_product(Product("Klawiatura mechaniczna", "Gaming", 400, store3.name))
    store3.add_product(Product("Mysz gamingowa", "Gaming", 200, store3.name))

    store4.add_product(Product("Pralka", "AGD", 1900, store4.name))
    store4.add_product(Product("Odkurzacz", "AGD", 850, store4.name))
    store4.add_product(Product("Smartwatch", "Wearables", 950, store4.name))
    store4.add_product(Product("Opaska fitness", "Wearables", 350, store4.name))

    store5.add_product(Product("Rower górski", "Sport", 2200, store5.name))
    store5.add_product(Product("Buty do biegania", "Sport", 350, store5.name))
    store5.add_product(Product("Piłka nożna", "Sport", 80, store5.name))
    store5.add_product(Product("Hantle 10kg", "Fitness", 120, store5.name))
    store5.add_product(Product("Mata do jogi", "Fitness", 150, store5.name))

    store6.add_product(Product("Książka 'Python dla każdego'", "Książki", 60, store6.name))
    store6.add_product(Product("Puzzle 1000 elementów", "Zabawki", 45, store6.name))
    store6.add_product(Product("Torba na laptopa", "Moda", 120, store6.name))
    store6.add_product(Product("Figurka kolekcjonerska", "Zabawki", 85, store6.name))
    store6.add_product(Product("Koszulka z nadrukiem", "Moda", 70, store6.name))

    return [store1, store2, store3, store4, store5, store6]

