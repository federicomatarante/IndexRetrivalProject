from dataclasses import dataclass


@dataclass
class Review:
    text: str


@dataclass
class Product:
    title: str
    description: str
    reviews: list[Review]

    def __post_init__(self):
        self.reviews = [] if self.reviews is None else self.reviews
