# from feel_it import EmotionClassifier, SentimentClassifier
from abc import ABC

from transformers import pipeline, Pipeline


class SentimentAnalyzer(ABC):

    def getScore(self, phrase: str) -> float:
        """
        :param phrase: The text to be analyzed.
        :rtype: float. It's a value between -1 and 1.
        """
        pass


class ReviewsHuggingFaceAnalyzer(SentimentAnalyzer):
    """
    This uses the HuggingFace pipeline to analyze the sentiment of a phrase.
    The model used is: juliensimon/reviews-sentiment-analysis.
    """
    _sentiment_model: Pipeline

    def __init__(self):
        self._sentiment_model = pipeline(task='sentiment-analysis', model="juliensimon/reviews-sentiment-analysis")

    def getScore(self, phrase: str) -> float:
        """
        :param phrase: The text to be analyzed.
        :rtype: float. It's a value between -1 and 1.
        """
        # se il documento contiene più di 512 termini tronco il documento
        # la funzione di sentiment non riesce a calcolare senza errori per più
        # di 512 termini
        phrase = phrase[0:510]

        sentiment = self._sentiment_model(phrase)[0]
        if sentiment['label'] == 'LABEL_1':
            return sentiment["score"]
        elif sentiment["label"] == 'LABEL_0':
            return -sentiment["score"]
        else:
            raise TypeError(sentiment)


class AmazonHuggingFaceAnalyzer(SentimentAnalyzer):
    """
    This uses the HuggingFace pipeline to analyze the sentiment of a phrase.
    The model used is: LiYuan/amazon-review-sentiment-analysis.
    """
    _sentiment_model: Pipeline

    def __init__(self):
        self._sentiment_model = pipeline(task='sentiment-analysis', model="LiYuan/amazon-review-sentiment-analysis")

    def getScore(self, phrase: str) -> float:
        """
        :param phrase: The text to be analyzed.
        :rtype: float. It's a value between -1 and 1.
        """

        # se il documento contiene più di 512 termini tronco il documento
        # la funzione di sentiment non riesce a calcolare senza errori per più
        # di 512 termini
        phrase = phrase[0:510]

        sentiment = self._sentiment_model(phrase)[0]
        if sentiment['label'] == '1 star':  # Between -1 and -0.6
            return -1 + sentiment["score"] * 0.4
        elif sentiment["label"] == '2 stars':  # Between -0.6 and -0.2
            return -0.6 + sentiment["score"] * 0.4
        elif sentiment["label"] == '3 stars':  # between -0.2 and 0.2
            return -0.2 + sentiment["score"] * 0.4
        elif sentiment["label"] == '4 stars':  # between 0.2 and 0.6
            return 0.2 + sentiment["score"] * 0.4
        elif sentiment["label"] == '5 stars':  # between 0.6 and 1
            return 0.6 + sentiment["score"] * 0.4
        else:
            raise TypeError(sentiment)
