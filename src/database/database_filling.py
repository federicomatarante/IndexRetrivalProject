import os

from src.apii import Product, Review
from src.database.database import ProductsDatabase


def get_products(directory: str):
    # Dict[Title,Product]
    products: dict[str, Product] = {}
    current_product_name = None
    current_product_link = None
    current_product_reviews = []

    file_names = os.listdir(directory)
    file_names.sort()
    for file_name in file_names:
        with open(directory + "\\" + file_name) as file:
            # Legge il nome del prodotto e va avanti nel loop se non è valido
            name = file.readline()
            if name is None or name == '':
                continue

            # Legge il n.o. di stelle della recensione e va avanti nel loop se non è valido
            stars_string = file.readline()
            if stars_string is None or stars_string == '' or not stars_string.rstrip().isdigit():
                continue
            stars = int(stars_string.rstrip())

            # Legge il link del prodotto e va avanti nel loop se non è valido
            link = file.readline()
            if link is None or link == '':
                continue

            # Legge la prima riga della recensione e va avanti nel loop se non è valido
            review_line = file.readline()
            if review_line is None or review_line == '':
                continue

            # Legge le successive righe della recensione concatenandole in un'unica variabile, formando una singola
            # stringa
            review = ""
            while review_line is not None and review_line != "":
                review = review + ' ' + review_line
                review_line = file.readline()

            # Aggiunge la recensione
            review = Review(stars=stars, text=review)
            current_product_reviews.append(review)

            # Se il nome del prodotto attuale è diverso dallo scorso vuol dire che ha iniziato a leggere le
            # recensioni di un altro prodotto. Per questo salva il prodotto attuale e inizia a "studiarne" un altro.
            if name != current_product_name:
                # Salva prodotto
                if current_product_name is not None:
                    if current_product_name in products.keys():
                        products[current_product_name].reviews.extend(current_product_reviews)
                    else:
                        product = Product(title=current_product_name, link=current_product_link,
                                          reviews=current_product_reviews)
                        products[current_product_name] = product

                # Resetta le variabili
                current_product_name = name
                current_product_link = link
                current_product_reviews = []

    if current_product_name is not None:
        if current_product_name in products.keys():
            products[current_product_name].reviews.extend(current_product_reviews)
        else:
            product = Product(title=current_product_name, link=current_product_link,
                              reviews=current_product_reviews)
            products[current_product_name] = product

    return list(products.values())


def populateDatabase(products: list[Product], databasePath: str):
    database = ProductsDatabase(databasePath)

    if database.exists():
        dbview = database.open()
    else:
        dbview = database.create()

    dbview.add(products)

    database.close()


database_path = "C:\\Users\\feder\\PycharmProjects\\IndexRetrivalProject\\src\\Doc"
folder_path = 'db.sqlite'

print("Prendo i prodotti dai file...")
p = get_products(database_path)
print(f"Presi {len(p)} prodotti!")
print("Inserisco prodotti nel database...")
populateDatabase(p, folder_path)
print("Prodotti inseriti!")
