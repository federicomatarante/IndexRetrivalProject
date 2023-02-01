from src.apii import Review
from src.sentimentanalysis import SentimentAnalyzer


class ReviewsAnalyzer:

    _sentimentAnalyzer = SentimentAnalyzer()

    def getSentiment(self, review: Review) -> float:
        """
        :param review: The review to be analyzed.
        :rtype: float. It's a value between -1 and 1.
        """
        return self._sentimentAnalyzer.getScore(review.text)
