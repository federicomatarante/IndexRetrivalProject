import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class TextPreprocessor:

    @staticmethod
    def process(text: str, language: str = 'english') -> set[str]:
        """
        :param text: str. The text to be preprocessed.
        :param language: str. The language of the text. The default is 'english'.
        :return: a list of processed tokens.
        """
        processing = TextProcessing(text,language=language)
        processing.tokenize()
        processing.removeStopwords()
        processing.filter(keepNouns=True, keepVerbs=True)
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
        self._tokens = set()
        self._language = language

    def tokenize(self):
        """Tokenizes the text generating the tokens"""
        self._tokens = set(nltk.word_tokenize(text=self._text, language=self._language))

    def removeStopwords(self):
        """Removes the stopwords from the generated tokens"""
        self._tokens -= set(stopwords.words(self._language))

    def stem(self):
        """Stems every generated token"""
        stemmer = PorterStemmer()
        self._tokens = set(stemmer.stem(token) for token in self._tokens)

    def lemmatize(self):
        """Lemmatizes every generated token"""
        lemmatizer = nltk.WordNetLemmatizer()
        self._tokens = set(lemmatizer.lemmatize(token) for token in self._tokens)

    def filter(self, keepNouns=True, keepVerbs=False, keepAdverbs=False, keepAdjectives=False):
        """Filters the token by syntactic category
        :param keepAdjectives bool. If it must keep the adjectives. By default, it's False.
        :param keepAdverbs bool. If it must keep the adverbs. By default, it's False.
        :param keepVerbs bool. If it must keep the verbs. By default, it's False.
        :param keepNouns boo.If it must keep the nouns. By default, it's True.
        """
        tags = nltk.pos_tag(self._tokens)
        self.clear()
        if keepNouns:
            self._tokens |= self._getTags(tags, 'NN', 'NNP', 'NNPS', 'NNS')
        if not keepVerbs:
            self._tokens |= self._getTags(tags, 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')
        if not keepAdverbs:
            self._tokens |= self._getTags(tags, 'RB', 'RBR', 'RBS', 'RP')
        if not keepAdjectives:
            self._tokens |= self._getTags(tags, 'JJ', 'JJR', 'JJS')

    @staticmethod
    def _getTags(tags: list[set[2]], *categories) -> set[str]:
        tokens: set[str] = set()
        for tag, category in tags:
            if category in categories:
                tokens.add(tag)

        return tokens

    def wordSenseDisambiguate(self):
        raise NotImplementedError()

    def clear(self):
        """Clears the generated tokens, creating a new empty set."""
        self._tokens = set()

    @property
    def tokens(self) -> set[str]:
        """The generated and processed tokens."""
        return self._tokens
