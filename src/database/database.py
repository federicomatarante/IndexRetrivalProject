import collections
import os
import uuid
from typing import Optional, Iterable, Union, List

from src.apii import Review, Product
from sqlite_database import SQLiteView, TableSchema
from src.database.databasecreator import ProductQueryCreator, ProductCreator


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
                'id': str(product.id),
                'title': product.title,
                'link': product.link
            })
            for review in product.reviews:
                self._sqliteView.insertOne('Review', {
                    'id': str(review.id),
                    'product_id': str(product.id),
                    'text': review.text,
                    'stars': review.stars
                })
        except Exception as e:
            raise DatabaseError(f"Could not add product: {product}\n")

    def get(self, productIds: Union[Union[str, uuid.UUID], List[Union[str, uuid.UUID]]] = None) -> List[Product]:

        """

        Retrieves a product from the database. :param productIds: the id of a product, can be single or an iterable.
        If left empty it retreives every product. of IDs. It can be a string or a UUID. :return: List[Product]: the
        list of required Products. It's given in the same order as required in the parameter productIds.

        """

        products = []

        try:
            query_creator = ProductQueryCreator(productIds)
            where = query_creator.where
            product_results = self._sqliteView.select('Product', ['title', 'link', 'id'], where)

            for product_result in product_results:
                product_creator = ProductCreator(product_result)
                review_results = self._sqliteView.select('Review', ['text', 'id', 'stars'],
                                                         f"product_id == '{product_creator.product_id}'")
                product_creator.setReviews(review_results)
                product = product_creator.product
                products.append(product)

        except Exception:
            raise DatabaseError(f"Could not find: {productIds}")

        if isinstance(productIds, Iterable):
            products = sorted(products, key=lambda x: productIds.index(x.id))
        return products

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
                            'id': 'TEXT PRIMARY KEY',
                            'title': 'TEXT NOT NULL',
                            'link': 'TEXT NULLABLE'
                        }),
            TableSchema(name='Review',
                        attributes={
                            'id': 'TEXT NOT NULL',
                            'text': 'TEXT',
                            'product_id': 'TEXT NOT NULL',
                            'stars': 'UNSIGNED INTEGER NOT NULL'
                        },
                        slope=['FOREIGN KEY(product_id) REFERENCES Product(id)',
                               'PRIMARY KEY(id,product_id)'])
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
