import os.path

import PySimpleGUI as sg
from src.docsmanager import DocsDatabase
from src.index import ProductsIndex, Sentiment
from src.searchengine import ProductSearcher
from src.CollectDocument import create_path

def switcher(sentiment) -> Sentiment:  # |[-1,1]|=2/5: 0.4
    """
    Metodo per passare da una stringa acquisita dalla gui ad un intervallo
    di float per cercare all'interno dell'indie i documenti che soddisfano
    il sentiment
    :param sentiment: stringa contenente il sentimento
    :return: tupla (a,b); l'intervallo del sentiment rispettivo.
    """
    if sentiment == "very bad":  # [-1,-0.6]
        return Sentiment.VERY_NEGATIVE
    if sentiment == "bad":  # [-0.6,-0.2]
        return Sentiment.NEGATIVE
    if sentiment == "neuter":  # [-0.2,0.2]
        return Sentiment.NEUTRAL
    if sentiment == "positive":  # [0.2,0.6]
        return Sentiment.POSITIVE
    if sentiment == "very positive":  # [0.6,1]
        return Sentiment.VERY_POSITIVE
    if sentiment == "all":
        return Sentiment.ALL


def remouve_doppi(result):
    posizioni = []
    for i in range(len(result) - 1):
        if result[i].text == result[i + 1].text:
            posizioni.append(i)
    for i in range(0, len(posizioni)):
        result.pop(posizioni[i])
        for j in range(i, len(posizioni)):
            posizioni[j] = posizioni[j] - 1


# aggiorna il campo i facendogli mostrare il risultato r
def aggiorna_campo(i, risultato):
    window['-COLUMN' + str(i) + '-'].update(visible=True)
    window['-FIELD' + str(i) + '-'].update("")
    window['-FIELD' + str(i) + '-'].print(
        str(i + 1) + "  " + risultato.product + "," + str(risultato.stars) + " " + risultato.document,
        background_color='#475841', text_color='white')
    window['-FIELD' + str(i) + '-'].print(str(risultato.sentiment) + risultato.text + "...")


def hideField(i):
    # Ho finito i risultati da mostrare: il campo verrà nascosto e svuotato
    window['-COLUMN' + str(i) + '-'].update(visible=False)
    window['-FIELD' + str(i) + '-'].update("")


# ad ogni risultato il "bottone vai alla pagina"
def fieldSingle(i):
    return [[sg.MLine("", key='-FIELD' + str(i) + '-', size=(82, 6), disabled=True, autoscroll=False),
             sg.Button("Vai alla pagina amazon", key='-BUTTON' + str(i) + '-', size=(6, 5)), ]]


def fieldCol(i):
    return [sg.Column(layout=fieldSingle(i), key='-COLUMN' + str(i) + '-', visible=False)]


# L'intera colonna dei risultati (inizializzata separatamente per essere scrollabile
resCol = [fieldCol(i) for i in range(0, 10)]

layoutRicerca = [[sg.Image(filename=("sm4.png"))],
                 [sg.Text("                  Search smartphone reviews", font=(2, 25))],
                 [sg.InputText(size=(65, 2), font=16)],
                 [sg.Text("                   Review opinion", font=22),
                  sg.OptionMenu(("all", "very bad", "negative", "neuter", "positive", "very positive"), size=(12, 3))],
                 [sg.Text("                                                     "), sg.Button("Search", font=16),
                  sg.Button("Cancel", font=16)],
                 [sg.Text("", key='-OutputStart-', size=(100, 1))],
                 [sg.Column(resCol, size=(690, 330), scrollable=True, key='-COLUMN-', vertical_scroll_only=True)]]

window = sg.Window("Search window", layoutRicerca, element_justification='l', size=(840, 580))



index = ProductsIndex("indexdir")
"""
if not index.exists():
    index.create()
"""
indexView = index.open()
n,dest = create_path()
docsDatabase = DocsDatabase(dest)
searcher: ProductSearcher = ProductSearcher(docsDatabase=docsDatabase, indexView=indexView)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == "Search":
        query = values[1]
        sentiment = values[2]
        and_type = 0
        query_type = query.split()
        for term in query_type:
            if term == "&":
                and_type = 1
        print("cerco")
        results = searcher.retrieve(query=query, sentiment=switcher(sentiment))
        print("finito di cercare")
        i = 1
        for i in range(0, 10):
            if i < len(results):
                aggiorna_campo(i, results[i])
                print(results[i])
            else:
                hideField(i)
            window.refresh()  # refresh required here
            window['-COLUMN-'].contents_changed()
