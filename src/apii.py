from dataclasses import dataclass

@dataclass
class Review:
    stars: int
    text: str


@dataclass
class Product:
    title: str
    link: str
    reviews: list[Review]

    def __post_init__(self):
        self.reviews = [] if self.reviews is None else self.reviews
