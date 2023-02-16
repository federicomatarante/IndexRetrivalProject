from src.apii import Review
from src.sentimentanalysis import SentimentAnalyzer


class ReviewsAnalyzer:
    sentimentAnalyzer: SentimentAnalyzer

    def __init__(self, sentimentAnalyzer: SentimentAnalyzer):
        self.sentimentAnalyzer = sentimentAnalyzer

    def getSentiment(self, review: Review) -> float:
        """
        :param review: The review to be analyzed.
        :rtype: float. It's a value between -1 and 1.
        """
        return self.sentimentAnalyzer.getScore(review.text)
