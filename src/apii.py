from dataclasses import dataclass


# Classe che descrive una recensione
@dataclass
class Review:
    product: str  # prodotto della recensione
    text: str  # testo della recensione
    link: str  # link della recensione
    sentiment: float  # sentimento della recensione
    stars: int  # stelle della recensione
    document: str  # nome del documento dalla quale estraggo la recensione
