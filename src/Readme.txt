# ---------------------------------------------------------------------#
# Progetto per il corso di gestione dell'informazione
# 229288@studenti.unimore.it   Bonfatti Andrea
# 85008@studenti.unimore.it    Matarante Federico
# 228001@studenti.unimore.it   Cocchi Giovanni
# ---------------------------------------------------------------------#

# ---------------------------------------------------------------------#
# Il progetto consiste in un IR che consente di effettuare ricerca basate
# sul contenuto di tecensioni
# ---------------------------------------------------------------------#

# ---------------------------------------------------------------------#
# Al primo avvio del programma non dovrebbe esistere la text repository
# e l'indice per crearli
# Però, dato che il seguente comando è molto lento, questi file sono stati
# già inseriti del file .rar. Se si vuole comunque creare la text repository,
# l'indice e il file di configurazione, lanciare il file setup.py dopo aver eliminato
# i file nella directory Doc e nella directory indexdir.
# Eseguire il file setup.py per creare la text repository e l'indice.
#       python3 setup.py
# I tempi di creazione della Text repository e dell'indice sono
# molto alti, convinene lancarli molto prima del test del programma vero
# e proprio.
# ---------------------------------------------------------------------#

# ---------------------------------------------------------------------#
# Agli avvi successivi, è possibile lanciare l'interfaccia grafica dal file main.py:
#       python3 main.py
# ---------------------------------------------------------------------#

# ---------------------------------------------------------------------#
# Per lanciare il benchmark, lanciare il file benchmark.py:
#     python3 benchmark.py
# ---------------------------------------------------------------------#

# ---------------------------------------------------------------------#
# ------------------------ Requisiti ----------------------------------#
# ---------------------------------------------------------------------#
Whoosh==2.7.4
transformers==4.3.3
tork==1.13.1
PySimpleGUI==4.34.0
nltk==3.5
# ---------------------------------------------------------------------#