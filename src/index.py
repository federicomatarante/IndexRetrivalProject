# from src.api import Product
from CollectDocument import create_path as Path
import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.writing import AsyncWriter
import sys


class ProductsIndexView:
    _textPreprocessor: TextPreprocessor

    def __init__(self, textPreprocessor: TextPreprocessor):
        self._textPreprocessor = textPreprocessor

    def query(self, query: str) -> list[str]:
        """
        :type query: str. The query in natural language to convert into the index.
        :rtype: a list of product's titles in decreasing order of score.
        """
        pass

    def add(self, product: Product):
        """
        :param product: Prodouct. The product to be added.
        :return: None
        """
        pass

    def delete(self, title: str):
        """
        :param title: str. The Product's title to delete.
        """


class ProductsIndex:

    def create(self) -> ProductsIndexView:
        """
        Creates the index file.
        @:return: ProductsIndexView. An object to use the index.
        """


    def open(self) -> ProductsIndexView:
        """
        Opens the index file.
        @:return: ProductsIndexView. An object to use the index.
        """

    def exists(self) -> bool:
        """
        :rtype: bool. If the index file already exists.
        """
        pass

    def delete(self):
        """
        Deletes the index file.
        """

def CheckAttributi(file_name):
    try:
        nome,titolo,stelle,link, recensione = "","","","",""
        fd = open(file_name, 'r')
        nome = fd.readline()
        titolo = fd.readline()
        stelle = fd.readline()
        link = fd.readline()
        recensione = fd.readlines()

        if nome == "" or titolo == "" or stelle == "" or link == "" or recensione == "" :
            return None
        else:
            return file_name
    except EOFError:
        print("mancano degli attributi")
    except Exception:
        print (Exception)





    # Creo la directory indexdir
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

