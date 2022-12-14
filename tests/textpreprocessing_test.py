from unittest import TestCase

from src.textpreprocessing import TextProcessing


class Test(TestCase):
    text = "Text processing is, unlike an algorithm, a manually administered sequence of simpler macros that are the " \
           "pattern-action expressions and filtering mechanisms. In either case the programmer's intention is " \
           "impressed indirectly upon a given set of textual characters in the act of text processing. The results of " \
           "a text processing step are sometimes only hopeful, and the attempted mechanism is often subject to " \
           "multiple drafts through visual feedback, until the regular expression or markup language details, " \
           "or until the utility options, are fully mastered. "

    def test_preprocessing(self):
        processing = TextProcessing(self.text)
        print("Tokenizing...")
        processing.tokenize()
        print(f"The tokens are {processing.tokens}")
        print("Removing stopwords...")
        processing.removeStopwords()
        print("Keeping only nouns and verbs...")
        processing.filter(keepNouns=True,keepVerbs=True)
        print(f"The tokens are {processing.tokens}")
        print("Lemming...")
        processing.lemmatize()
        print(f"The tokens are {processing.tokens}")
        print("Stemming...")
        processing.stem()
        print(f"The tokens are {processing.tokens}")

