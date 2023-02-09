"""
File completamente inutile usato solo per creare i campi dell'interfaccia grafica
dove mostro i risultati della ricerca
"""
import os.path

from whoosh import scoring, qparser
from whoosh.index import open_dir

# apro la cartella dell'indice
from whoosh.qparser import MultifieldParser

from IndexRetrivalProject.src.docsmanager import DocsDatabase
from IndexRetrivalProject.src.sentimentanalysis import ReviewsHuggingFaceAnalyzer


def switcher(sentiment) -> tuple:  # |[-1,1]|=2/5: 0.4
    """
    Metodo per passare da una stringa acquisita dalla gui ad un intervallo
    di float per cercare all'interno dell'indie i documenti che soddisfano
    il sentiment
    :param sentiment: stringa contenente il sentimento
    :return: tupla (a,b); l'intervallo del sentiment rispettivo.
    """
    if sentiment == "molto negativo":  # [-1,-0.6]
        return -1, -0.6
    if sentiment == "negativo":  # [-0.6,-0.2]
        return -0, 6, -0, 2
    if sentiment == "neutro":  # [-0.2,0.2]
        return -0.2, 0.2
    if sentiment == "positivo":  # [0.2,0.6]
        return 0.2, 0.6
    if sentiment == "molto positivo":  # [0.6,1]
        return 0.6, 1
    if sentiment == "tutti":
        return -1, 1


def MySearch(user_query: str, sentiment: str, query_type: str = ""):
    """
    Metodo per passare query all'indice
    :param ix: riferimento all'indice, prima della chiamata ix = open_dir("indexdir")
    :param user_query: testo acquisito dal campo di testo dall'interfaccia grafica
    :param sentiment: sentimento acquisito da interfaccia grafica
    :param query_type: parametro che indica il tipo di query, AND, OR o phrasal
    :return: lista di documenti che contiene tutti i termini
    """
    ix = open_dir("indexdir")
    searcher = ix.searcher()

    # La ricerca la faccio sul prodotto della recensione
    # e sul testo preprocessato della recensione
    # il sentiment lo controllo a ricerca fatta

    # ----------------------------------------------------- #
    # Metto la query in AND o in OR
    # ----------------------------------------------------- #
    type_parser = ""
    if query_type == "AND":
        #type_parser = qparser.AndGroup.factory(["nome_prodotto", "testo_processato"])
        type_parser = qparser.AndGroup
    else:
        #type_parser = qparser.OrGroup.factory(["nome_prodotto", "testo_processato"])
        type_parser = qparser.OrGroup

    # Creo la query
    parser = MultifieldParser(["nome_prodotto", "testo_processato"], schema=ix.schema, group=type_parser)
    query = parser.parse(user_query)

    """
    sentiment_filter = query.NumericRange("sentiment", 0, 1)  # TODO
    query = query.And([query, sentiment_filter])
    """

    # Cerco la query
    results = searcher.search(query, limit=50)

    documents = [result["document"] for result in results]
    print(documents)
    d = DocsDatabase("C:\\Users\\amndr\\Desktop\\ProgettoGestion\\IndexRetrivalProject\\src\\Doc",sentimentAnalyzer=ReviewsHuggingFaceAnalyzer())
    r = d.getDocs(documents)
    for rev in r:
        print(rev.__dict__)




if __name__ == "__main__":
    MySearch("camera", "tutti")
