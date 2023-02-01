# from feel_it import EmotionClassifier, SentimentClassifier
from transformers import pipeline, Pipeline


class SentimentAnalyzer:
    _sentiment_pipeline: Pipeline

    def __init__(self):
        self._sentiment_pipeline = pipeline("sentiment-analysis")

    def getScore(self, phrase: str) -> float:
        """
        :param phrase: The text to be analyzed.
        :rtype: float. It's a value between -1 and 1.
        """
        sentiment = self._sentiment_pipeline(phrase)[0]
        print(sentiment)
        if sentiment['label'] == 'POSITIVE':
            return sentiment["score"]
        elif sentiment["label"] == 'NEGATIVE':
            return -sentiment["score"]
        else:
            raise TypeError(sentiment)