# ------------------------------------------------------------------- #
"""
Modulo che si occupa di estrapolare il contenuto da un file csv per creare
un text repository dal quale poi costruire l'indice
"""
# ------------------------------------------------------------------- #

import csv
import os

half_link = "https://www.amazon.it/s?k="


def create_link(stringa):
    """
    Metodo che crea un link alla pagina amazon a partire da un prodotto
    """
    i = stringa.find('(')
    nome = stringa[0:i]   # estraggo i caratteri fino alla parentesi
    nome = nome.replace(" ","+") # sostituisco gli spazi con dei +

    # se l' ultimo carattere è un + lo elimino
    if nome[-1] == "+":
        nome = nome[0:len(nome)-1]
    return half_link+nome


def delete_space(strina):
    """
    Metodo che elimina gli spazi da una stringa
    """
    return strina.replace(" ", "")


def replace(stringa):
    stringa = stringa.replace("*", " ")
    return stringa

def create_name(stringa):
    """
    Metodo che estrae il nome del prodotto
    """
    i = stringa.find('(')
    nome = stringa[0:i]
    return nome


def create_path():
    """
    Metodo che crea i path dei file sorgente dai quali leggere le recensioni
    e della direcgtory di destinazione che diventa la text repository
    """
    s = (os.path.realpath(__file__))
    i = len(s)
    while s[i-1] != "\\": i=i-1
    s = s[0:i]
    return s+"Amazon_Unlocked_Mobile11.csv",s+"Amazon_Unlocked_Mobile12.csv",\
           s+"Amazon_Unlocked_Mobile21.csv",s+"Amazon_Unlocked_Mobile22.csv",s+"Doc\\"


# ------------------------------------------------------------------- #
# Metodo che si occupa di costruire la Document repository
# ------------------------------------------------------------------- #
def collect_document():

    # Creo i path dei file sorgenti e della text repository
    s1,s2,s3,s4, dest = create_path()

    if not os.path.exists(dest):
        os.mkdir(dest)

    # Numero che uso per incrementare i nomi deo dei documenti
    k=0

    # Per ogni file lo apro in lettura
    input_file = [s1,s2,s3,s4]
    for filen in input_file:
        with open(filen,'r',encoding = 'ISO-8859-1')as file:


            reader = csv.reader(file)

            # Per ogni riga letta creo un file testuale
            for riga in reader:
                half_name = replace(str(riga[0]))
                half_name = delete_space(half_name)
                nome_prodotto = str(riga[1]+" "+half_name)
                print(nome_prodotto)
                recensione = riga[4]
                stelle = riga[3]

                # Creo il file testuale e ci scrivo dentro
                fd=open(dest + "Rev" + str(k) + ".txt", 'w',encoding="utf-8")
                k=k+1
                fd.write(nome_prodotto+"\n")
                fd.write(stelle+"\n")
                fd.write(create_link(nome_prodotto)+"\n")

                # Per una questione di leggibilità del file scrivo la recensione
                # splittata su più righe
                token_for_word = 0
                recensione = str(recensione)
                recensione = recensione.split()
                for t in recensione:
                    fd.write(t + " ")
                    token_for_word = token_for_word + 1
                    if token_for_word == 15:
                        fd.write('\n')
                        token_for_word = 0
                fd.close()

    """
class CollectDocument:
    def __init__(self):
        s1,s2,s3,s4,dest = create_path()
        if not os.path.exists(dest):
            os.mkdir(dest)
        k = 0




        with open(source, newline="", encoding="ISO-8859-1") as filecsv:
            while (csv.reader(filecsv, delimiter=",") and k <= 17248):
                k = k + 1
                try:
                    lettore = csv.reader(filecsv, delimiter=",")
                    header = next(lettore)
                    file_name = create_name(header[1])
                    file_name = delete_space(file_name)
                    fd = open(dest + "Rev" + str(k) + file_name + ".txt", 'w')

                    fd.write(header[1] + "\n")  # Nome del prodotto
                    fd.write(header[5] + "\n")  # Stelle della recensione
                    link = create_link(header[1])
                    fd.write(link + '\n')  # link amazon del prodotto
                    text = header[4]

                    token_for_word = 0
                    text = str(text)
                    text = text.split()
                    for t in text:  # recensione separata su più righe
                        fd.write(t + " ")
                        token_for_word = token_for_word + 1
                        if token_for_word == 15:
                            fd.write('\n')
                            token_for_word = 0
                    fd.close()
                except:
                    pass
        filecsv.close()
"""

# Per creare una text repository eseguire lo script come programma
if __name__ == '__main__':
    print("Creo la collezione di documenti")
    collect_document()
