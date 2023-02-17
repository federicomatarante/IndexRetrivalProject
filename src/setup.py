from CollectDocument import collect_document, create_path
from index_filling import createIndex
from index import ProductsIndex
from sentimentanalysis import ReviewsHuggingFaceAnalyzer

if __name__ == "__main__":
    # Creo la collezione di documenti
    collect_document()

    # Rimuovo file duplicati
    n1, directory = create_path()

    # Creo l'indice sulla text repository
    createIndex(ProductsIndex("indexdir"), ReviewsHuggingFaceAnalyzer(), 'Doc')
