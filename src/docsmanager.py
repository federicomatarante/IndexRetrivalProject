import os
import re
from typing import List, Union, Iterable, Optional

from src.apii import Review
from src.sentimentanalysis import SentimentAnalyzer, ReviewsHuggingFaceAnalyzer


class DocumentManager:
    _sentimentAnalyzer: SentimentAnalyzer

    def __init__(self, sentimentAnalyzer: SentimentAnalyzer):
        self._sentimentAnalyzer = sentimentAnalyzer

    def getReview(self, file) -> Optional[Review]:
        lines: list[str] = file.readlines()
        if not DocumentManager._isFileValid(lines):
            return None
        product = lines[0].rstrip()
        stars = int(lines[1].rstrip())
        link = lines[2].rstrip()
        sentiment = float(lines[3].rstrip())
        text = ''.join(lines[4:]).replace('\n', '')
        document = file.name[file.name.rindex(os.sep) + 1:]
        return Review(product=product, stars=stars, link=link, text=text, document=document, sentiment=sentiment)

    @staticmethod
    def writeReview(file, review: Review):
        lines: list[str] = [
            review.product + "\n",
            str(review.stars) + "\n",
            str(review.link) + "\n",
            str(review.sentiment) + "\n",
            review.text
        ]
        file.writelines(lines)

    @staticmethod
    def _isFileValid(lines: list[str]) -> bool:
        if len(lines) < 5:
            return False
        if lines[0].rstrip() == "" or lines[2].rstrip() == "":
            return False
        if len([line for line in lines[4:] if line == "" or line == '\n']) == len(lines[3:]):
            return False
        if not lines[1].rstrip().isdigit() or not lines[3].rstrip().isdigit():
            return False
        return True


class DocsDatabase:
    _path: str
    _documentManager: DocumentManager

    def __init__(self, path: str, sentimentAnalyzer: SentimentAnalyzer):
        self._path = path
        self._documentManager = DocumentManager(sentimentAnalyzer)

    def getDocs(self, documents: Union[str, Iterable[str]] = None) -> List[Review]:
        reviews: List[Review] = []
        if isinstance(documents, str):
            documents = [documents]

        if documents is not None:
            filenames = documents
        else:
            filenames = os.listdir(self._path)

        i = 0
        for filename in filenames:
            with open(self._path + os.sep + filename, 'r', encoding='utf-8') as file:
                review: Optional[Review] = self._documentManager.getReview(file)
                i = i + 1
                if review is not None:
                    reviews.append(review)

        if documents is not None:
            reviews = sorted(reviews, key=lambda r: documents.index(r.document))
        return reviews

    def addDocs(self, reviews: Union[Review, Iterable[Review]]):
        if isinstance(reviews, Review):
            reviews = [reviews]
        for review in reviews:
            with open(self._path + os.sep + review.document, "w", encoding='utf-8') as file:
                self._documentManager.writeReview(file, review)

    def removeDocs(self, reviews: Union[Review, Iterable[Review]]):
        if isinstance(reviews, Review):
            reviews = [reviews]
        for review in reviews:
            os.remove(self._path + os.sep + review.document)

    def exists(self) -> bool:
        return os.path.exists(self._path)

    def create(self):
        os.makedirs(self._path)

    def getAvailableName(self) -> str:
        file_names = os.listdir(self._path)
        numbers = [int(name.rstrip("Rev")) for name in file_names]
        last_number = numbers[len(numbers) - 1]
        for i in range(last_number):
            if i not in numbers:
                file_number = i
                break
        else:
            file_number = last_number
        return "Rev" + str(file_number)

    @property
    def count(self):
        return len(os.listdir(self._path))
