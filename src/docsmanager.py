import os
from typing import List, Union, Iterable, Optional

from src.apii import Review


class DocumentManager:
    @staticmethod
    def writeReview(file, review: Review):
        """
        Writes a review to a file.
        :param file: the file to write to.
        :param review: the review to write.
        """
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
        """
        :param lines: the lines of the file.
        :return: True if the file is valid, False otherwise.
        """
        if len(lines) < 5:
            return False
        if lines[0].rstrip() == "" or lines[2].rstrip() == "":
            return False
        if len([line for line in lines[4:] if line == "" or line == '\n']) == len(lines[3:]):
            return False
        if not lines[1].rstrip().isdigit() or not lines[3].rstrip().replace('.', "").replace("-", "").isnumeric():
            return False
        return True

    @staticmethod
    def getReview(file) -> Optional[Review]:
        """
        It reads a review from a file.
        :param file: the file to read from.
        :return: the review as a Review object.
        """
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


class DocsDatabase:
    _path: str
    _documentManager: DocumentManager

    def __init__(self, path: str):
        """
        :param path: the path to the database. It must be a directory.
        """
        self._path = path
        self._documentManager = DocumentManager()

    def getDocs(self, documents: Union[str, Iterable[str]] = None) -> List[Review]:
        """
        :param documents: the documents to get. If None, all documents will be returned.
        :return: the documents as a list of Review objects. The order of the documents is the same as the order
        of the names.
        """
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
        """
        Adds the documents to the database
        :param reviews: the documents to add.
        """
        if isinstance(reviews, Review):
            reviews = [reviews]
        for review in reviews:
            with open(self._path + os.sep + review.document, "w", encoding='utf-8') as file:
                self._documentManager.writeReview(file, review)

    def removeDocs(self, reviews: Union[Review, Iterable[Review]]):
        """
        Removes the documents from the database
        """
        if isinstance(reviews, Review):
            reviews = [reviews]
        for review in reviews:
            os.remove(self._path + os.sep + review.document)

    def exists(self) -> bool:
        """
        :return: True if the database exists, False otherwise
        """
        return os.path.exists(self._path)

    def create(self):
        """
        Creates the database
        """
        os.makedirs(self._path)

    def getAvailableName(self) -> str:
        """
        :return: the first available document name in the database
        """
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
        """
        :return: number of documents in the database
        """
        return len(os.listdir(self._path))
