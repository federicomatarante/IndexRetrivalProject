from unittest import TestCase

from src.api import Product, Review
from src.database.database import ProductsDatabase


class Test(TestCase):

    def test_creation(self):
        database = ProductsDatabase(file='producstDatabase.sqlite')
        print(f"Exists: {database.exists()}")
        print("Creating database...")
        database.create()
        print(f"Exists: {database.exists()}")
        print("Deleting database...")
        database.delete()
        print(f"Exists: {database.exists()}")

    def test_open_creation(self):  # Run twice
        database = ProductsDatabase(file='producstDatabase.sqlite')
        if not database.exists():
            database.create()
        else:
            database.open()

        database.close()

    def test_add_delete_get(self):
        database = ProductsDatabase(file='producstDatabase.sqlite')
        if not database.exists():
            view = database.create()
        else:
            view = database.open()

        a_product = Product(title='Iphone', description='Boh', reviews=[
            Review("Gross"),
            Review("Nice"),
            Review("I don't know bro")
        ])
        view.delete('Iphone')
        print("Adding product...")
        view.add(a_product)
        print("Getting product...")
        product = view.get('Iphone')
        print(f"Product: {product}")
        print("Deleting product...")
        view.delete('Iphone')
        database.close()
        assert (a_product.__dict__ == product.__dict__)

