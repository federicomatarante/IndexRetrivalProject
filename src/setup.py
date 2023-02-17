from CollectDocument import collect_document,create_path,RestringiCollezione
from remove_invalid_files import check_for_duplicates
from index_filling import createIndex
from docsmanager import DocsDatabase
from index import ProductsIndex
from sentimentanalysis import SentimentAnalyzer, ReviewsHuggingFaceAnalyzer

if __name__ == "__main__":

    # Creo la collezione di documenti
    collect_document()

    # Rimuovo file duplicati
    n1,directory = create_path()
    check_for_duplicates(directory)

    # Creo l'indice sulla text repository
    createIndex(ProductsIndex("indexdir"), ReviewsHuggingFaceAnalyzer(), 'Doc')
