import uuid
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Review:
    stars: int      # stelle della recensione
    text: str       # testo della recensione
    sentiment = None    #sentimento della recensione
    id: str = None      # nome del documento dalla quale estraggo la recensione

    def __post_init__(self):
        self.id = str(uuid.uuid4()) if self.id is None else self.id


@dataclass
class Product:
    title: str  # nome del prodotto
    link: str   # link amazon al prodotto
    reviews: list[Review] = None # lista di recensioni
    id: UUID = None  # id del prodotto, per cercarlo nel DB

    def __post_init__(self):
        self.reviews = [] if self.reviews is None else self.reviews
        self.id = uuid.uuid4() if self.id is None else self.id
