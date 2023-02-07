import uuid
from dataclasses import dataclass
from uuid import UUID

# Classe che descrive una recensione
@dataclass
class Review:
    product: str     # prodotto della recensione
    text: str        # testo della recensione
    link: str        # link della recensione
    sentiment: float # sentimento della recensione
    star: int        # stelle della recensione
    document: str    # nome del documento dalla quale estraggo la recensione


@dataclass
class Product:
    title: str  # nome del prodotto
    link: str   # link amazon al prodotto
    reviews: list[Review] = None # lista di recensioni
    id: UUID = None  # id del prodotto, per cercarlo nel DB

    def __post_init__(self):
        self.reviews = [] if self.reviews is None else self.reviews
        self.id = uuid.uuid4() if self.id is None else self.id
