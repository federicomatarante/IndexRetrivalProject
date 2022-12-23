from src.api import Product
from src.database.database import ProductsDatabaseView
from src.index import ProductsIndexView


class ProductSearcher:
    _databaseView: ProductsDatabaseView
    _indexView: ProductsIndexView

    def __init__(self, databaseView: ProductsDatabaseView, indexView: ProductsIndexView):
        self._databaseView = databaseView
        self._indexView = indexView

    def retrive(self, query: str) -> list[Product]:
        """
        :param query: str. The query in natural language.
        :return: list[Product]. A list of required products in decreasing order of importance.
        """
        titles: list[str] = self._indexView.query(query)
        return [self._databaseView.get(title) for title in titles]
