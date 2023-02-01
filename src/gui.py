import PySimpleGUI as sg

class gui:
    def __init__(self, tipo):
        self.tipo = tipo
        self.window = self.make_window()

    def make_window(self):
        """
        Metodo che utilizzo per risolvere il problema di pysimplegui che non permette
        di riutilizzare lo stesso layout più volte, la finestra la creo con un layout definito
        come variabile locale di questa funzione, così posso riusalra varie volte
        """
        if self.tipo == "Ricerca":
            layoutRicerca = [[sg.Image(filename=("sm4.png"))],
                            [sg.Text("Ricerca tra le recensioni di smartphone",font=(1,30))],
                            [sg.Text("Contenuto da cercare", font=22), sg.InputText(size=(65,2),font=16)],
                            [sg.Text("Opinione della recensione", font=22), sg.OptionMenu(("Tutte","Positiva", "Negativa"),size=(12,3))],
                            [sg.Text("                                                                 "),sg.Button("Cerca", font=16)]]
            return sg.Window("Ricerca ", layoutRicerca, element_justification='l', size=(740, 480))


def app():
    window = gui("Ricerca")
    while True:
        event, values = window.window.read()
        if event == sg.WIN_CLOSED:
            break