import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.writing import AsyncWriter
from textpreprocessing import FullPreprocessor
from sentimentanalysis import AmazonHuggingFaceAnalyzer, ReviewsHuggingFaceAnalyzer


def CheckAttributi(file_name):
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
        stelle = fd.readline()
        link = fd.readline()
        recensione = fd.readlines()

        if nome == "" or stelle == "" or link == "" or recensione == "":
            return False
        else:
            return True
    except EOFError:
        print("mancano degli attributi")
    except Exception:
        print(Exception)


def list_to_string(lista):
    """
    Metodo che converte una lista in una stringa
    :param lista: lista di stringhe
    :return: le stringhe contenute nella lista
    """
    s = ''.join(str(char) for char in lista)
    return s


def CreateIndex(dest):
    """
    Metodo che si occupa della costruzione di un indice a partire
    dai documenti presenti nella
    :param dest: text repository contenente tutti i file da indicizzare
    :return: None
    """
    schema = Schema(nome_prodotto=TEXT(stored=True),  # nome del prodotto
                    stelle=ID(stored=True),  # stelle della recensione
                    link=ID(stored=True),  # link amazon al prodotto recensito
                    sentiment=ID(stored=True),  # sentimento estratto dalla recensione
                    document=ID(stored=True),  # nome del documento contenente la recensione
                    testo_recensione=TEXT(stored=True),  # testo della recensione nella sua interezza
                    testo_processato=TEXT)  # testo della recensione pre-processato

    # Se non esiste la directory indexdir la creo
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    ix = create_in("indexdir", schema)
    writer = AsyncWriter(ix)
    analyzer = ReviewsHuggingFaceAnalyzer()

    # Acquisisco il path di ogni file nel text repository
    files = os.listdir(dest)
    for file in files:
        file_name = dest + "\\" + file

        # Se il file ha tutti i campi lo inserisco nell'indice
        if CheckAttributi(file_name):
            # apro il file e leggo i vari campi
            fd = open(file_name, 'r', encoding="utf-8")
            nome = fd.readline().rstrip()
            stelle = fd.readline().rstrip()
            link = fd.readline().rstrip()
            rec = fd.readlines()
            recensione = list_to_string(rec)

            # Calcola il sentimento
            sentiment = analyzer.getScore(recensione)
            sentiment = str(sentiment)
            # Pre-processa il testo della recensione
            pre = FullPreprocessor.process(recensione)
            pre = ' '.join(pre)
            # Aggiungo un documento all'indice
            print(recensione)
            writer.add_document(nome_prodotto=nome,
                                stelle=stelle,
                                link=link,
                                sentiment=sentiment,
                                document=file,
                                testo_recensione=recensione,
                                testo_processato=pre)
            fd.close()

    writer.commit()


if __name__ == "__main__":
    print("creo l'indice")
    CreateIndex(os.getcwd() + "\\" + "Doc")