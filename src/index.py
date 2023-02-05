# from src.api import Product
import os
import shutil
from typing import Optional, Iterable, Union
from uuid import UUID

from whoosh.fields import Schema, ID, TEXT
from whoosh.index import create_in, open_dir, exists_in, Index
from whoosh.writing import AsyncWriter

from IndexRetrivalProject.src.apii import Product


class ProductsIndexView:
    _index: Index

    def __init__(self, index: Index):
        self._index = index

    def query(self, productQuery: str, reviewsQuery: str) -> list[UUID]:
        """
        :type productQuery: str. The query in natural language to convert into the index for Products.
        :type reviewsQuery: str. The query in natural language to convert into the index for Reviews.
        :rtype: a list of product's ids in decreasing order of score.
        """
        pass

    def add(self, products: Union[Product, Iterable[Product]]):
        """
        :param products: The product to be added. Can be either a single or a collection.
        """
        if isinstance(products, Product):
            products = [products]
        with AsyncWriter(self._index) as writer:
            for product in products:
                for rewiew in product.reviews:
                        writer.add_document(nome=product.title, nome_doc = rewiew.id, id_prodotto = product.id,stelle=rewiew.stars, sentiment=rewiew.sentiment, testo=rewiew.text)
            writer.commit()

    def delete(self, products: Union[Product, Iterable[Product]]):
        """
        :param products: The product to be removed. Can be either a single or a collection.
        """
        if isinstance(products, Product):
            products = [products]
        with AsyncWriter(self._index) as writer:
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
        self._schema = Schema(nome=ID(stored=True),  # nome dello smartphone
                              nome_doc=ID(stored=True), # nome del documento
                              id_prodotto=ID(stored=True), # id del prodotto, per cercare nel DB
                              stelle=ID(stored=True),  # stelle della recensione
                              sentiment=ID(stored=True),  # sentimento della recensione
                              testo=TEXT(stored=True))  # testo della recensione

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

