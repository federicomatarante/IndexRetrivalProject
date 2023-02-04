from CollectDocument import create_path as Path
import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.writing import AsyncWriter

from IndexRetrivalProject.src.database.database import ProductsDatabase
from textpreprocessing import TextPreprocessor
from sentimentanalysis import SentimentAnalyzer as s

def CheckAttributi(file_name):
    try:
        nome,stelle,link, recensione = "","","","",
        fd = open(file_name, 'r')
        nome = fd.readline()
        stelle = fd.readline()
        link = fd.readline()
        recensione = fd.readlines()

        if nome == "" or stelle == "" or link == "" or recensione == "" :
            return False
        else:
            return True
    except EOFError:
        print("mancano degli attributi")
    except Exception:
        print(Exception)

def list_to_string(lista):
    """Metodo che converte una lista in una stringa"""
    s = ''.join(str(char) for char in lista)
    return s


def CreateIndex(dest):
    """ con TEXT memorizzo anche le posizioni delle parole, con il campo ID memorizzo un'informazione
        da non trattare come testo ma da trattere nell'insieme come ad esempio il sentimento, il numero di
        stelle ed il path del file"""

    schema = Schema(nome = ID(stored = True),  # nome dello smartphone
                    stelle = ID(stored = True), # stelle della recensione
                    sentiment = ID(stored = True), # sentimento della recensione
                    testo = TEXT(stored=True)) #testo della recensione

    # Creo la directory indexdir
    if not os.path.exists( "indexdir"):
        os.mkdir("indexdir")

    ix = create_in("indexdir",schema)
    writer = AsyncWriter(ix)

    # Acquisisco i path di tutti i file nella cartella Doc
    files = os.listdir(dest)
    for file in files:

        file_name = dest+"\\"+file
        # controllo che un file abbia tutti gli attibuti, se li ha
        # lo inserisco nell'indice

        if CheckAttributi(dest+'\\'+file):
            fd = open(file_name,'r',encoding="utf-8")

            nome = fd.readline().rstrip()
            stelle = fd.readline().rstrip()
            link = fd.readline().rstrip()
            rec = fd.readlines()
            recensione = list_to_string(rec)

            pre = TextPreprocessor.process(recensione)
            recensione = list_to_string(pre)

            """TO DO aggiungo il file al database"""
            d = ProductsDatabase("database.sqlite")
            if not d.exists():
                database = d.create()
            else:
                database = d.open()



            """ TO DO funzione di sentiment"""
            #sentiment = s.getScore(testo)

            # aggiungo un documento all'indice
            writer.add_document(nome =nome,
                                stelle= stelle,
                                sentiment ='0.0',
                                testo= recensione)
            fd.close()
    writer.commit()

if __name__ == "__main__":
    CreateIndex(os.getcwd()+"\\"+"Doc")