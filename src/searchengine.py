from index import ProductsIndexView, Sentiment
from apii import Review

from docsmanager import DocsDatabase


class ProductSearcher:
    _docsDatabase: DocsDatabase
    _indexView: ProductsIndexView

    def __init__(self, docsDatabase: DocsDatabase, indexView: ProductsIndexView):
        """
        :param docsDatabase: the database where the documents are stored.
        :param indexView: the index view where to search.
        """
        self._docsDatabase = docsDatabase
        self._indexView = indexView

    def retrieve(self, query: str, sentiment: Sentiment = Sentiment.ALL, limit: int = 50, orSearch: bool = True) -> \
            list[Review]:
        """
        :param query: the query to search.
        :param sentiment: the sentiment of the reviews to search.
        :param limit: the maximum number of reviews to retrieve.
        :param orSearch: if true, the query is searched as an OR query, otherwise as an AND query.
        :return: the list of reviews that match the query.
        """
        results: list[str] = self._indexView.query(query, sentiment, limit, orSearch)
        return self._docsDatabase.getDocs(results)


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
