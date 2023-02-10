import PySimpleGUI as sg
import Test_search


def res_col(i):
    return [sg.Column(layout=fieldSingle(i), key='-COLUMN'+str(i)+'-', visible=False)]

# resCol = [  fieldCol(i) for i in range(0,10)]
class gui:
    def __init__(self, tipo, risutlati=None):
        """
        Metodo per creare una finestra con la libreria pysimplegui
        :param tipo: tipo di finestra da creare
        :param risutlati: risultati della ricerca
        """
        self.tipo = tipo
        self.risultati = risutlati
        self.headings = ["Document", "Product", "text", "Link", "Stars", "Sentiment"]

        # crea la finestra
        self.window = self.make_window()



    def make_window(self):
        """
        Metodo che utilizzo per risolvere il problema di pysimplegui che non permette
        di riutilizzare lo stesso layout più volte, la finestra la creo con un layout definito
        come variabile locale di questa funzione, così posso riusalra varie volte
        """
        if self.tipo == "Ricerca":
            layoutRicerca = [[sg.Image(filename=("sm4.png"))],
                            [sg.Text("                  Search smartphone reviews",font=(2,25))],
                            [sg.InputText(size=(65,2),font=16)],
                            [sg.Text("                   Review opinion", font=22), sg.OptionMenu(("all","very bad", " negative"," neuter"," positive"," very positive"),size=(12,3))],
                            [sg.Text("                                                     "),sg.Button("Search", font=16),sg.Button("Cancel", font=16)],
                            [sg.Text("", key='-OutputStart-', size=(100, 1))],
                            [sg.Column(resCol, size=(690, 330), scrollable=True, key='-COLUMN-',vertical_scroll_only=True)]]
            return sg.Window("Search window", layoutRicerca, element_justification='l', size=(840, 580))


def app():
    window = gui("Ricerca")
    while True:
        event, values = window.window.read()

        if event == sg.WIN_CLOSED:
            break


        if event == "Search":

            # acquisico i valori dalla gui
            query_text = values[1]
            query_sentiment = values[2]

            if query_text == "":
                sg.popup_error("Enter something to search for")

            # elimino i risultati della precedente ricerca
            # nel caso ce ne fossero
            risultati = []
            Test_search.MySearch(query_text,query_sentiment, risultati)

            window2 = gui("Risultati",risultati)
            window,window2 = window2,window
            window2.window.close()