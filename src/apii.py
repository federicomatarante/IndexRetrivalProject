import uuid
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Review:
    stars: int
    text: str
    id: str = None

    def __post_init__(self):
        self.id = str(uuid.uuid4()) if self.id is None else self.id


@dataclass
class Product:
    title: str
    link: str
    reviews: list[Review] = None
    id: UUID = None

    def __post_init__(self):
        self.reviews = [] if self.reviews is None else self.reviews
        self.id = uuid.uuid4() if self.id is None else self.id
