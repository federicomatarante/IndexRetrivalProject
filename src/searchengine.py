from index import ProductsIndexView, Sentiment, ProductsIndex
from src.apii import Review

from src.docsmanager import DocsDatabase
from src.sentimentanalysis import ReviewsHuggingFaceAnalyzer


class ProductSearcher:
    _docsDatabase: DocsDatabase
    _indexView: ProductsIndexView

    def __init__(self, docsDatabase: DocsDatabase, indexView: ProductsIndexView):
        self._docsDatabase = docsDatabase
        self._indexView = indexView

    def retrive(self, query: str, sentiment: Sentiment = Sentiment.ALL, limit: int = 50, orSearch: bool = True) -> list[
        Review]:
        titles: list[str] = self._indexView.query(query, sentiment, limit, orSearch)
        return self._docsDatabase.getDocs(titles)


""" # How to use code example
index = ProductsIndex("C:\\Users\\feder\\PycharmProjects\\IndexRetrivalProject\\src\\indexdir")
if not index.exists():
    index.create()
indexView = index.open()
docsDatabase = DocsDatabase("C:\\Users\\feder\\PycharmProjects\\IndexRetrivalProject\\src\\DOc",
                            ReviewsHuggingFaceAnalyzer())
searcher: ProductSearcher = ProductSearcher(docsDatabase=docsDatabase, indexView=indexView)
while True:
    print("Query: ")
    query = input()
    reviews = searcher.retrive(query)
    for review in reviews:
        print(str(review.sentiment) + " -> " + review.text)

"""
