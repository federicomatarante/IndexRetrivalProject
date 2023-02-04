import string
from abc import ABC

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class TextPreprocessor(ABC):
    @staticmethod
    def process(text: str, language: str = 'english') -> list[str]:
        """
        :param text: str. The nntext to be preprocessed.
        :param language: str. The language of the text. The default is 'english'.
        :return: a list of processed tokens.
        """
        pass


class FullPreprocessor(TextPreprocessor):

    @staticmethod
    def process(text: str, language: str = 'english') -> list[str]:
        processing = TextProcessing(text, language=language)
        processing.tokenize()
        processing.removeStopwords()
        processing.filter()
        processing.stem()
        processing.lemmatize()
        return processing.tokens


class TextProcessing:

    def __init__(self, text: str, language: str = 'english'):
        """
        :param text: str. The text to be processed.
        :param language: str. The language of the text. The default is 'english'.
        """
        self._text = text
        self._language = language
        self._tokens = list()

    def tokenize(self):
        """Tokenizes the text generating the tokens"""
        self._tokens = list(nltk.word_tokenize(text=self._text, language=self._language))
        self._tokens = [token.lower() for token in self._tokens
                        if not (not token.isalnum() or token in string.punctuation)]

    def removeStopwords(self):
        """Removes the stopwords from the generated tokens"""
        self._tokens = [token for token in self._tokens
                        if token not in stopwords.words(self._language)]

    def stem(self):
        """Stems every generated token"""
        stemmer = PorterStemmer()
        self._tokens = list(stemmer.stem(token) for token in self._tokens)

    def lemmatize(self):
        """Lemmatizes every generated token"""
        lemmatizer = nltk.WordNetLemmatizer()
        self._tokens = list(lemmatizer.lemmatize(token) for token in self._tokens)

    def filter(self, removeNouns=False, removeVerbs=True, removeAdverbs=True, removeAdjectives=True):
        """Filters the token by syntactic category
        :param removeAdjectives bool. If it must remove the adjectives. By default, it's True.
        :param removeAdverbs bool. If it must remove the adverbs. By default, it's True.
        :param removeVerbs bool. If it must remove the verbs. By default, it's True.
        :param removeNouns boo. If it must remove the nouns. By default, it's False.
        """
        tags = nltk.pos_tag(self._tokens)
        if removeNouns:
            self._tokens -= self._getTags(tags, 'NN', 'NNP', 'NNPS', 'NNS')
        if not removeVerbs:
            self._tokens -= self._getTags(tags, 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')
        if not removeAdverbs:
            self._tokens -= self._getTags(tags, 'RB', 'RBR', 'RBS', 'RP')
        if not removeAdjectives:
            self._tokens -= self._getTags(tags, 'JJ', 'JJR', 'JJS')

    @staticmethod
    def _getTags(tags: list[set[2]], *categories) -> list[str]:
        tokens: list[str] = list()
        for tag, category in tags:
            if category in categories:
                tokens.append(tag)

        return tokens

    def wordSenseDisambiguate(self):
        raise NotImplementedError()

    def clear(self):
        """Clears the generated tokens, creating a new empty set."""
        self._tokens = list()

    @property
    def tokens(self) -> list[str]:
        """The generated and processed tokens."""
        return self._tokens
