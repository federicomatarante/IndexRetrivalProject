"""
File completamente inutile usato solo per creare i campi dell'interfaccia grafica
dove mostro i risultati della ricerca
"""
from whoosh import scoring, qparser
from whoosh.index import open_dir


# apro la cartella dell'indice
from whoosh.qparser import MultifieldParser


def switcher(sentiment):
    if sentiment == "negativo":
        pass
    if sentiment == "positivo":
        pass
    if sentiment == "tutti":
        pass


def MySearch(user_query,sentiment, query_type):
    """
    Metodo per passare query all'indice
    :param ix: riferimento all'indice, prima della chiamata ix = open_dir("indexdir")
    :param user_query: testo acquisito dal campo di testo dall'interfaccia grafica
    :param sentiment: sentimento acquisito da interfaccia grafica
    :param query_type: parametro che indica il tipo di query, AND, OR o phrasal
    :return: lista di documenti che contiene tutti i termini
    """
    ix = open_dir("indexdir")
    searcher = ix.searcher(weighting=scoring.TF_IDF())

    # La ricerca la faccio sul prodotto della recensione
    # e sul testo preprocessato della recensione
    # il sentiment lo controllo a ricerca fatta

    # ----------------------------------------------------- #
    # Metto la query in AND o in OR
    # ----------------------------------------------------- #
    type_parser = ""
    if query_type == "AND":
        type_parser = qparser.AndGroup(["nome_prodotto","testo_processato"])
    if query_type == "OR":
        type_parser = qparser.OrGroup(["nome_prodotto","testo_processato"])

    parser = MultifieldParser(["nome_prodotto","testo_processato"],schema=ix.schema, group=type_parser)
    query = parser.parse()





