from src.api import Review
from src.sentimentanalysis import SentimentAnalyzer


class ReviewsAnalyzer:

    @staticmethod
    def getSentiment(review: Review) -> float:
        """
        :param review: The review to be analyzed.
        :rtype: float. It's a value between -1 and 1.
        """
        return SentimentAnalyzer.getScore(review.text)
