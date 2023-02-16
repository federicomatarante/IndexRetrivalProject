from CollectDocument import collect_document, create_path, RestringiCollezione
from remove_invalid_files import check_for_duplicates
from src.index_filling import createIndex
from index import ProductsIndex
from sentimentanalysis import ReviewsHuggingFaceAnalyzer

if __name__ == "__main__":
    # Creo la collezione di documenti
    collect_document()

    # Rimuovo file duplicati
    n1, n2, n3, n4, directory = create_path()
    check_for_duplicates(directory)

    # Restringo la collezione di documenti per questioni di
    # risparmio di tempo visto che l'indicizzazione è molto lunga
    RestringiCollezione(directory)

    # Creo l'indice sulla text repository
    createIndex(ProductsIndex("indexdir"), ReviewsHuggingFaceAnalyzer(), 'Doc')
