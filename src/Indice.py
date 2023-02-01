from CollectDocument import create_path as Path
import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.writing import AsyncWriter
from textpreprocessing import TextPreprocessor

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



def CreateIndex(dest):
    """ con TEXT memorizzo anche le posizioni delle parole, con il campo ID memorizzo un'informazione
        da non trattare come testo ma da trattere nell'insieme come ad esempio il sentimento, il numero di
        stelle ed il path del file"""

    print(dest)
    schema = Schema(nome_smarthone = TEXT(stored = True),\
                    stelle_recensione = ID(stored = True),
                    sentiment = ID(stored = True),
                    file_path = ID(stored = True),
                    link = ID(stored = True),
                    testo_recensione = TEXT(stored = True),
                    testo_processato = TEXT)

    # Creo la directory indexdir
    if not os.path.exists( "indexdir"):
        os.mkdir("indexdir")

    ix = create_in("indexdir",schema)
    writer = AsyncWriter(ix)

    # Acquisisco i path di tutti i file nella cartella Doc
    #src, dest = Path()
    print(os.listdir(dest))
    files = os.listdir(dest)
    for file in files:

        file_name = dest+"\\"+file
        print(file_name)
        # controllo che un file abbia tutti gli attibuti, se li ha
        # lo inserisco nell'indice

        if CheckAttributi(dest+'\\'+file):
            fd = open(file_name,'r',encoding="utf-8")

            nome = fd.readline().rstrip()
            stelle = fd.readline().rstrip()
            link = fd.readline().rstrip()
            recensione = fd.readlines()

            """TO DO aggiungo il file al database"""

            """ TO DO funzione di sentiment"""
            sentiment = " 0 "
            # text_processato = TextPreprocessor.process(recensione)
            # print(text_processato)

            # aggiungo un documento all'indice
            writer.add_document(nome_smarthone =nome,\
                                stelle_recensione = stelle,\
                                sentiment =sentiment,\
                                link = link,\
                                testo_recensione = recensione,\
                                testo_processato = "")
            fd.close()
    writer.commit()

if __name__ == "__main__":
    print("directory corrente")
    print(os.getcwd())
    CreateIndex(os.getcwd()+"\\"+"Doc")