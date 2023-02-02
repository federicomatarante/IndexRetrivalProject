import os
from typing import Optional

from src.apii import Product, Review
from sqlite_database import SQLiteView, TableSchema


class DatabaseError(Exception):
    pass


class ProductsDatabaseView:

    def __init__(self, sqliteView: SQLiteView):
        """
        :param sqliteView: str. The collection where products will be stored.
        """
        self._sqliteView = sqliteView

    def add(self, product: Product):
        """
        Adds a product in the database.
        :param product: Product. The product to add to the database.
        """

        try:
            self._sqliteView.insertOne('Product', {
                'title': product.title,
                'description': product.description
            })
            for review in product.reviews:
                self._sqliteView.insertOne('Review', {
                    'product': product.title,
                    'text': review.text
                })
        except Exception:
            raise DatabaseError(f"Could not add product: {product.title}\n")

    def get(self, title: str) -> Optional[Product]:

        """
        Retrieves a product from the database.
        :param title: str. The title of the required Product.
        :return: Optional[Product]. The required Product, if present. Else none.
        """

        try:
            product_results = self._sqliteView.select('Product', ['title', 'description'], f"title == '{title}'")
            if not product_results:
                return None
            description = product_results[0]["description"]
            review_results = self._sqliteView.select('Review', ['text'], f"product == '{title}'")
            reviews = [Review(review_result['text']) for review_result in review_results]

            return Product(title=title, description=description, reviews=reviews)

        except Exception:
            raise DatabaseError(f"Could not find: {title}")

    def delete(self, title: str):

        """
        Deletes a product from the database.
        :param title: str. The Product's title to delete.
        """

        try:
            self._sqliteView.delete('Product', f"title == '{title}'")
            self._sqliteView.delete('Review', f"product == '{title}'")
        except Exception:
            raise DatabaseError(f"Could not delete: {title}")


class ProductsDatabase:

    def __init__(self, file: str):
        """
        :param file: str. The file path where products will be stored.
        """
        table_schemas = [
            TableSchema(name='Product',
                        attributes={
                            'title': 'TEXT PRIMARY KEY',
                            'description': 'TEXT NULLABLE'}),
            TableSchema(name='Review',
                        attributes={
                            'text': 'TEXT',
                            'product': 'TEXT NOT NULL'},
                        slope=['FOREIGN KEY(product) REFERENCES Product(title)',
                               'PRIMARY KEY(text,product)'])
        ]
        self._sqliteView = SQLiteView(file, table_schemas)
        self._file = file

    def create(self) -> ProductsDatabaseView:
        """
        Creates the database. If it already exist, it throws an Exception.
        @:return: ProductsDatabaseView. An object to use the database.
        """
        self._sqliteView.connect()
        self._sqliteView.createTables()
        return ProductsDatabaseView(self._sqliteView)

    def open(self) -> ProductsDatabaseView:
        """
        Opens the database.
        @:return: ProductsDatabaseView. An object to use the database.
        """
        if self._sqliteView.isConnected():
            raise DatabaseError("Database is already connected!")
        if not self.exists():
            raise DatabaseError("Database does not exist")
        self._sqliteView.connect()
        return ProductsDatabaseView(self._sqliteView)

    def exists(self) -> bool:
        """
        :rtype: bool. If the database already exists.
        """
        return os.path.exists(self._file) and self._doTablesExist()

    def close(self):
        """
        Closes the database.
        """
        self._sqliteView.disconnect()

    def delete(self):
        """
        Deletes the database.
        """
        self.close()
        os.remove(self._file)

    def _doTablesExist(self):
        if self._sqliteView.isConnected():
            result = self._sqliteView.doTablesExist()
        else:
            self._sqliteView.connect()
            result = self._sqliteView.doTablesExist()
            self._sqliteView.disconnect()
        return result
