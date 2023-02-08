from index import ProductsIndexView

from src.docsmanager import DocsDatabase


class ProductSearcher:
    _docsDatabase: DocsDatabase
    _indexView: ProductsIndexView

    def __init__(self, docsDatabase: DocsDatabase, indexView: ProductsIndexView):
        self._docsDatabase = docsDatabase
        self._indexView = indexView

    def retrive(self, query): # TODO migliore query
        titles: list[str] = self._indexView.query(query)
        return self._docsDatabase.getDocs(titles)
