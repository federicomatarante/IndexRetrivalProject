import uuid
from typing import Iterable, Union, List
from uuid import UUID

from src.apii import Review, Product


class ProductQueryCreator:
    def __init__(self, productIds: Union[Union[str, UUID], List[Union[str, UUID]]] = None):
        self.productIds = productIds

    @property
    def where(self):
        where = None
        if isinstance(self.productIds, Iterable):
            products_id = [f"'{str(productId)}'" for productId in self.productIds]
            where = f"id IN ({', '.join(products_id)})"
        elif self.productIds is not None:
            where = f"id == '{str(self.productIds)}'"
        return where


class ProductCreator:
    def __init__(self, database_result):
        self.link = database_result["link"]
        self.title = database_result["title"]
        self.product_id = database_result['id']
        self.reviews = []

    def setReviews(self, review_results):
        self.reviews = [Review(text=review_result['text'], stars=review_result["stars"])
                        for review_result in review_results]

    @property
    def product(self):
        return Product(title=self.title, link=self.link, reviews=self.reviews, id=uuid.UUID(self.product_id))
