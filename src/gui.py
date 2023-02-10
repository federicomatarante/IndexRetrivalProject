import PySimpleGUI as sg
import Test_search

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
                            [sg.Text("                                                                 "),sg.Button("Search", font=16)]]
            return sg.Window("Search window", layoutRicerca, element_justification='l', size=(740, 480))


        if self.tipo == "Risultati":
            layout_mostra = [[sg.Image(filename=("sm4.png"))],
                             [sg.Table(values=self.risultati,
                                       headings=self.headings,
                                       max_col_width=35,
                                       auto_size_columns=True,
                                       alternating_row_color="DeepSkyBlue3",
                                       display_row_numbers=True,
                                       justification='right',
                                       num_rows=20,
                                       key='-TABLE-',
                                       vertical_scroll_only=False,
                                       row_height=45)],
                             [sg.Button("OK", font=16)]]
            return sg.Window("Risultati ricerca", layout_mostra, element_justification='l', size=(740, 480))

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
            window.risultati.clear()
            risultati = Test_search.MySearch(query_text,query_sentiment)




