import csv
import os
import nltk

half_link = "https://www.amazon.it/s?k="
def replace (stringa:str):
    """
    Metodo che estrae il nome del prodotto, ultile per i link
    :param stringa: nome del device con caratteristiche tra parentesi
    :return: nome del device
    """
    i = stringa.find('(')
    stringa2 = stringa[0:i]
    stringa2=stringa2.replace(" ", '+')
    if stringa2[-1] == '+':
        stringa2 = stringa2[0:len(stringa2)-1]
    return half_link+stringa2

def create_path():
    """
    metodo che cra i path del sorgente con i device e le recensioni
    e della directory di destinazione con tutti i file estratti
    :return: path del sorgente e della destinazione
    """
    s = (os.path.realpath(__file__))
    i = len(s)
    while s[i-1] != "\\": i=i-1
    s = s[0:i]
    return s+"phone_reviews.csv", s+"Doc\\"

def create_file_name(string:str) -> str:
    """
    metodo che estrae il nome del prodotto dalla recensione
    :param string: recensione intera contenente nome del prodotto e dati
    :return: nome del prodotto
    """
    i = string.find('(')
    string2 = string[0:i]
    return string2

"""------------------------------------------------------------------------- """
class CollectDocument:
    def __init__(self):
        source, dest = create_path()
        if not os.path.exists(dest):
            os.mkdir(dest)

        """ APRO IL FILE CSV, PER OGNI RIGA CREO UN FILE CON LA RELATIVA RECENSIONE DI 
            UN PRODOTTO """
        k = 0
        with open(source, newline="", encoding="ISO-8859-1") as filecsv:
            while (csv.reader(filecsv, delimiter=",") and k <= 17248 ):
                k = k+1
                try:
                    lettore = csv.reader(filecsv, delimiter=",")
                    header = next(lettore)
                    file_name = create_file_name(header[1])
                    fd = open(dest+"Rev"+str(k)+file_name+".txt",'w')
                    fd.write(header[1])     # Nome del prodotto
                    fd.write(header[3])     # Titolo della recensione
                    fd.write(header[5]+"\n")    # Stelle della recensione
                    link = replace(header[1])
                    fd.write(link+'\n')       # link amazon del prodotto
                    text = header[4]
                    token_for_word=0
                    text = nltk.word_tokenize(text)
                    for t in text:              # recensione splittata su più righe
                        fd.write(t+" ")
                        token_for_word=token_for_word+1
                        if token_for_word == 15:
                            fd.write('\n')
                            token_for_word=0
                    fd.close()
                except: pass
        filecsv.close()