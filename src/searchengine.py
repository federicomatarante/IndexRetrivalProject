from src.api import Product
from src.database.database import ProductsDatabaseView
from src.index import ProductsIndexView


class ProductSearcher:
    databaseView: ProductsDatabaseView
    indexView: ProductsIndexView

    def retrive(self, query: str) -> list[Product]:
        """
        :param query: str. The query in natural language.
        :return: list[Product]. A list of required products in decreasing order of importance.
        """
        titles: list[str] = self.indexView.query(query)
        return [self.databaseView.get(title) for title in titles]
