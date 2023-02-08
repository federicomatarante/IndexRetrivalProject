# from src.api import Product
import os
import shutil
from typing import Optional, Iterable, Union
from uuid import UUID

from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.index import create_in, open_dir, exists_in, Index
from whoosh.writing import AsyncWriter

from src.apii import Product, Review
from src.docsmanager import DocsDatabase
from src.sentimentanalysis import SentimentAnalyzer, ReviewsHuggingFaceAnalyzer
from src.textpreprocessing import TextPreprocessor, FullPreprocessor


class ProductsIndexView:
    _index: Index
    textPreprocessor: TextPreprocessor

    def __init__(self, index: Index, textPreprocessor: TextPreprocessor = FullPreprocessor()):
        self._index = index
        self.textPreprocessor = textPreprocessor

    def query(self, reviewsQuery: str) -> list[str]:
        """
        :type productQuery: str. The query in natural language to convert into the index for Products.
        :type reviewsQuery: str. The query in natural language to convert into the index for Reviews.
        :rtype: a list of product's ids in decreasing order of score.
        """
        pass

    def add(self, reviews: Union[Review, Iterable[Review]]):
        """
        :param reviews: The reviews to be added. Can be either a single or a collection.
        """
        if isinstance(reviews, Review):
            reviews = [reviews]
        writer = AsyncWriter(self._index)
        for review in reviews:
            writer.add_document(nome_prodotto=review.product,
                                stelle=review.stars,
                                link=review.link,
                                sentiment=review.sentiment,
                                document=review.document,
                                testo_recensione=review.text,
                                testo_processato=self.textPreprocessor.process(review.text))

        writer.commit()

    def delete(self, reviews: Union[Review, Iterable[Review]]):
        """
        : param reviews: The review to be removed. Can be either a single or a collection.
        """
        if isinstance(reviews, Review):
            reviews = [reviews]
        writer = AsyncWriter(self._index)
        for review in reviews:
            writer.delete_by_term(document=review.document)
        writer.commit()


class ProductsIndex:
    _indexDirectoryPath: str
    _schema: Schema
    _index: Optional[Index] = None
    _indexView: Optional[ProductsIndexView] = None

    def __init__(self, indexDirectoryPath: str):
        self._indexDirectoryPath = indexDirectoryPath
        self._schema = Schema(nome_prodotto=TEXT(stored=True),  # nome del prodotto
                              stelle=NUMERIC(stored=True),  # stelle della recensione
                              link=ID(stored=True),  # link amazon al prodotto recensito
                              sentiment=NUMERIC(stored=True),  # sentimento estratto dalla recensione
                              document=ID(stored=True),  # nome del documento contenente la recensione
                              testo_recensione=TEXT(stored=True),  # testo della recensione nella sua interezza
                              testo_processato=TEXT)  # testo della recensione pre-processato

    def create(self) -> ProductsIndexView:

        """
        Creates the index file.
        @:return: ProductsIndexView. An object to use the index.
        """
        if self._index is None:
            if not os.path.exists(self._indexDirectoryPath):
                os.makedirs(self._indexDirectoryPath)
            self._index = create_in(self._indexDirectoryPath, self._schema)
            self._indexView = ProductsIndexView(self._index)
        return self._indexView

    def open(self) -> ProductsIndexView:
        """
        Opens the index file.
        @:return: ProductsIndexView. An object to use the index.
        """
        if self._index is None:
            self._index = open_dir(self._indexDirectoryPath)
            self._indexView = ProductsIndexView(self._index)
        return self._indexView

    def exists(self) -> bool:
        """
        :rtype: bool. If the index file already exists.
        """
        return os.path.exists(self._indexDirectoryPath) and exists_in(self._indexDirectoryPath)

    def delete(self):
        """
        Deletes the index file.
        """
        shutil.rmtree(self._indexDirectoryPath)

    def close(self):
        """
        Closes the index.
        """
        self._index.close()
        self._index = None
        self._indexView = None



def createIndex(index: ProductsIndex, sentimentAnalyzer: SentimentAnalyzer, directory: str):
    if not index.exists():
        index.create()
    view = index.open()
    database = DocsDatabase(directory,sentimentAnalyzer)
    print("Retreiving reviews...")
    reviews = database.getDocs()
    print("Retreived!")
    print("Adding to the index...")
    view.add(reviews)
    print(reviews)
    print("Added!")
    index.close()


#createIndex(ProductsIndex("indexdir"), ReviewsHuggingFaceAnalyzer(), 'Doc')
