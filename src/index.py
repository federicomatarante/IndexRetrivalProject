# from src.api import Product
import os
import shutil
from typing import Optional, Iterable, Union
from uuid import UUID

from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.index import create_in, open_dir, exists_in, Index
from whoosh.writing import AsyncWriter

from src.apii import Product, Review
from src.sentimentanalysis import SentimentAnalyzer, ReviewsHuggingFaceAnalyzer
from src.textpreprocessing import TextPreprocessor, FullPreprocessor


class ProductsIndexView:
    _index: Index
    textPreprocessor: TextPreprocessor

    def __init__(self, index: Index, textPreprocessor: TextPreprocessor = FullPreprocessor()):
        self._index = index
        self.textPreprocessor = textPreprocessor

    def query(self, productQuery: str, reviewsQuery: str) -> list[UUID]:
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

    def delete(self, products: Union[Product, Iterable[Product]]):
        """
        :param products: The product to be removed. Can be either a single or a collection.
        """
        if isinstance(products, Product):
            products = [products]
        writer = AsyncWriter(self._index)
        for product in products:
            # TODO vedi come eliminare
            writer.delete_by_term()
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


def _isFileValid(file_name: str):
    """
    Metodo che controlla che un file abbia tutti gli attributi necessari
    dato che non tutti i documenti risultano essere completi
    :param file_name: file di cui controllare la completezza
    :return: true se il file contiene tutti i campi, false altrimenti
    """
    try:
        nome, stelle, link, recensione = "", "", "", "",
        fd = open(file_name, 'r')
        nome = fd.readline()
        stelle = fd.readline().rstrip()
        link = fd.readline()
        recensione = fd.readlines()
        if nome == "" or stelle == "" or link == "" or recensione == "" or not stelle.isdigit():
            return False
        else:
            return True
    except EOFError:
        print("Mancano degli attributi")
        return False


def _getReviews(sentimentAnalyzer: SentimentAnalyzer, directory: str) -> list[Review]:
    reviews: list[Review] = []
    files = os.listdir(directory)

    for file in files:
        file_name = directory + "\\" + file
        # Se il file ha tutti i campi lo inserisco nell'indice
        if _isFileValid(file_name):
            # apro il file e leggo i vari campi
            fd = open(file_name, 'r', encoding="utf-8")
            nome = fd.readline().rstrip()
            stelle = int(fd.readline().rstrip())
            link = fd.readline().rstrip()
            linee_recensione = fd.readlines()
            recensione = ' '.join(linee_recensione).replace("\n", "")
            # Calcola il sentimento
            sentiment = sentimentAnalyzer.getScore(recensione)
            review = Review(text=recensione, stars=stelle, document=file_name, link=link, sentiment=sentiment,
                            product=nome)
            reviews.append(review)

    return reviews


def createIndex(index: ProductsIndex, sentimentAnalyzer: SentimentAnalyzer, directory: str):
    if not index.exists():
        index.create()
    view = index.open()
    reviews = _getReviews(sentimentAnalyzer, directory)
    print(reviews)
    print("Adding reviews")
    view.add(reviews)
    index.close()


createIndex(ProductsIndex("indexdir"), ReviewsHuggingFaceAnalyzer(), 'Doc')
