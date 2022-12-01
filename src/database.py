from typing import Optional

from src.api import Product


class ProductsDatabaseView:
    def add(self, product: Product):
        """
        :param product: Product. The product to add to the database.
        """

    def get(self, title: str) -> Optional[Product]:
        """
        :param title: str. The title of the required Product.
        :return: Optional[Product]. The required Product, if present. Else none.
        """

    def delete(self, title: str):
        """
        :param title: str. The Product's title to delete.
        """


class ProductsDatabase:
    def create(self) -> ProductsDatabaseView:
        """
        Creates the database file.
        @:return: ProductsDatabaseView. An object to use the database.
        """

    def open(self) -> ProductsDatabaseView:
        """
        Opens the database file.
        @:return: ProductsDatabaseView. An object to use the database.
        """

    def exists(self) -> bool:
        """
        :rtype: bool. If the database file already exists.
        """
        pass

    def delete(self):
        """
        Deletes the database file.
        """
