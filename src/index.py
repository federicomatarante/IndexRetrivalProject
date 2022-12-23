from src.api import Product
from src.textpreprocessing import TextPreprocessor


class ProductsIndexView:
    _textPreprocessor: TextPreprocessor

    def __init__(self, textPreprocessor: TextPreprocessor):
        self._textPreprocessor = textPreprocessor

    def query(self, query: str) -> list[str]:
        """
        :type query: str. The query in natural language to convert into the index.
        :rtype: a list of product's titles in decreasing order of score.
        """
        pass

    def add(self, product: Product):
        """
        :param product: Prodouct. The product to be added.
        :return: None
        """
        pass

    def delete(self, title: str):
        """
        :param title: str. The Product's title to delete.
        """


class ProductsIndex:

    def create(self) -> ProductsIndexView:
        """
        Creates the index file.
        @:return: ProductsIndexView. An object to use the index.
        """

    def open(self) -> ProductsIndexView:
        """
        Opens the index file.
        @:return: ProductsIndexView. An object to use the index.
        """

    def exists(self) -> bool:
        """
        :rtype: bool. If the index file already exists.
        """
        pass

    def delete(self):
        """
        Deletes the index file.
        """
