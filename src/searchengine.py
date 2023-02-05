from uuid import UUID

from database.database import ProductsDatabaseView
from index import ProductsIndexView


class ProductSearcher:
    _databaseView: ProductsDatabaseView
    _indexView: ProductsIndexView

    def __init__(self, databaseView: ProductsDatabaseView, indexView: ProductsIndexView):
        self._databaseView = databaseView
        self._indexView = indexView

    def retrive(self, productQuery: str = None, reviewsQuery: str = None):
        product_ids: list[UUID] = self._indexView.query(productQuery=productQuery, reviewsQuery=reviewsQuery)
        return self._databaseView.get(product_ids)
