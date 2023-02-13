from src.docsmanager import DocsDatabase
from src.index import ProductsIndex
from src.sentimentanalysis import SentimentAnalyzer, ReviewsHuggingFaceAnalyzer


def createIndex(index: ProductsIndex, sentimentAnalyzer: SentimentAnalyzer, directory: str):
    if not index.exists():
        index.create()
    view = index.open()
    database = DocsDatabase(directory, sentimentAnalyzer)
    print("Retreiving reviews...")
    reviews = database.getDocs()
    print("Retreived!")
    print(reviews)

    print("Adding to the index...")
    view.add(reviews)
    print("Added!")
    index.close()


#createIndex(ProductsIndex("indexdir"), ReviewsHuggingFaceAnalyzer(), 'Documents')
