# ------------------------------------------------------------------- #
"""
Modulo che si occupa di estrapolare il contenuto da un file csv per creare
un text repository dal quale poi costruire l'indice
"""
# ------------------------------------------------------------------- #

import csv
import os

half_link = "https://www.amazon.it/s?k="

# ------------------------------------------------------------------- #
# Metodo che crea un link alla pagina amazon a partire da un prodotto
# ------------------------------------------------------------------- #
def create_link(stringa):
    i = stringa.find('(')
    nome = stringa[0:i]   # estraggo i caratteri fino alla parentesi
    nome = nome.replace(" ","+") # sostituisco gli spazi con dei +

    # se l' ultimo carattere è un + lo elimino
    if nome[-1] == "+":
        nome = nome[0:len(nome)-1]
    return half_link+nome

# ------------------------------------------------------------------- #
# Metodo che elimina gli spazi da una stringa
# ------------------------------------------------------------------- #
def delete_space(strina):
    return strina.replace(" ", "")


# ------------------------------------------------------------------- #
# Metodo che estrae il nome del prodotto
# ------------------------------------------------------------------- #
def create_name(stringa):
    i = stringa.find('(')
    nome = stringa[0:i]
    return nome

# ------------------------------------------------------------------- #
# Metodo che crea i path del file sorgente dal quale leggere le
# recensioni e della directory destinazione che diventa poi la
# Document repository
# ------------------------------------------------------------------- #
def create_path():
    s = (os.path.realpath(__file__))
    i = len(s)
    while s[i-1] != "\\": i=i-1
    s = s[0:i]
    return s+"phone_reviews.csv", s+"Doc\\"


# ------------------------------------------------------------------- #
# Classe che si occupa di costruire la Document repository
# ------------------------------------------------------------------- #
class CollectDocument:
    def __init__(self):
        source, dest = create_path()
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

# Per creare una text repository eseguire lo script come programma
if __name__ == '__main__':
    print("Creo la collezione di documenti")
    CollectDocument()