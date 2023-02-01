from apii import Product
from database.database import ProductsDatabaseView
from index import ProductsIndexView
from whoosh.index import open_dir
from whoosh.fields import *

class ProductSearcher:
    _databaseView: ProductsDatabaseView
    _indexView: ProductsIndexView

    def __init__(self, databaseView: ProductsDatabaseView, indexView: ProductsIndexView):
        self._databaseView = databaseView
        self._indexView = indexView

    def retrive(self, query):


        titles: list[str] = self._indexView.query(query)
        return [self._databaseView.get(title) for title in titles]
