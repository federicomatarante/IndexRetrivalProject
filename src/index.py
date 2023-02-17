import os
import shutil
from enum import Enum
from typing import Optional, Iterable, Union

from whoosh import qparser
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.index import create_in, open_dir, exists_in, Index
from whoosh.qparser import MultifieldParser
from whoosh.query import NumericRange, And
from whoosh.writing import AsyncWriter

from src.apii import Review
from src.textpreprocessing import TextPreprocessor, FullPreprocessor


class Sentiment(Enum):
    ALL = 1
    VERY_POSITIVE = 2
    POSITIVE = 3
    NEUTRAL = 4
    NEGATIVE = 5
    VERY_NEGATIVE = 6


def _getSentimentInterval(sentiment: Sentiment) -> tuple:
    """
    :param sentiment: The sentiment to be converted into an interval.
    :return: A tuple (a,b) representing the interval of the sentiment.
    """
    if sentiment == Sentiment.VERY_NEGATIVE:  # [-1,-0.6]
        return -1, -0.6
    if sentiment == Sentiment.NEGATIVE:  # [-0.6,-0.2]
        return -0.6, -0.2
    if sentiment == Sentiment.NEUTRAL:  # [-0.2,0.2]
        return -0.2, 0.2
    if sentiment == Sentiment.POSITIVE:  # [0.2,0.6]
        return 0.2, 0.6
    if sentiment == Sentiment.VERY_POSITIVE:  # [0.6,1]
        return 0.6, 1
    if sentiment == Sentiment.ALL:
        return -1, 1


class ProductsIndexView:
    _index: Index
    textPreprocessor: TextPreprocessor

    def __init__(self, index: Index, textPreprocessor: TextPreprocessor = FullPreprocessor()):
        """
        :param index: The index to be used.
        :param textPreprocessor: The text preprocessor to be used.
        """
        self._index = index
        self.textPreprocessor = textPreprocessor

    def query(self, query: str, sentiment: Sentiment = Sentiment.ALL, limit: int = 50, orSearch: bool = True) -> \
            list[str]:
        """
        :type query: str. The query in natural language to convert into the index for Reviews.
        :type sentiment: Sentiment. The sentiment of the reviews to be searched.
        :type limit: int. The maximum number of reviews to be returned.
        :type orSearch: bool. If the query is an OR search or an AND search.
        :rtype: a list of product's ids in decreasing order of score.
        """
        if orSearch:
            type_parser = qparser.OrGroup
        else:
            type_parser = qparser.AndGroup

        with self._index.searcher() as searcher:
            # Creo la query
            parser = MultifieldParser(["nome_prodotto", "testo_processato"], schema=self._index.schema,
                                      group=type_parser)
            # TODO valuta se mettere dei boost
            query = parser.parse(query)

            min_sentiment, max_sentiment = _getSentimentInterval(sentiment)
            sentiment_filter = NumericRange("sentiment", min_sentiment, max_sentiment)
            query = And([query, sentiment_filter])
            # Cerco la query
            results = searcher.search(query, limit=limit)
            documents = [(result["document"]) for result in results]
        return documents

    def add(self, reviews: Union[Review, Iterable[Review]]):
        """
        :param reviews: The reviews to be added. Can be either a single or a collection.
        """
        if isinstance(reviews, Review):
            reviews = [reviews]
        writer = AsyncWriter(self._index)
        for review in reviews:
            writer.add_document(nome_prodotto=review.product,
                                sentiment=review.sentiment,
                                document=review.document,
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
        """
        :param indexDirectoryPath: The path of the directory where the index will be stored.
        """
        self._indexDirectoryPath = indexDirectoryPath
        # TODO valuta se none_prodotto può essere ID
        self._schema = Schema(nome_prodotto=TEXT(stored=True),  # nome del prodotto
                              sentiment=NUMERIC(stored=True),  # sentimento estratto dalla recensione
                              document=ID(stored=True),  # nome del documento contenente la recensione
                              testo_processato=TEXT(stored=True))  # testo della recensione pre-processato

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
