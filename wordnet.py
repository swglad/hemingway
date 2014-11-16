"""
wordnet.py

API wrapper to lookup words on Princeton Wordnet.
"""

from nltk.corpus import wordnet
from nltk.wsd import lesk


def disambiguate(context, word, pos):
    """
    Word sense disambiguation using Lesk algorithm
    @context: a string containing the word whose meaning we want to disambiguate
    @word: the word we want to disambiguate
    @pos: the part of speech
    Returns: the Synset of the most likely meaning of the word
    """
    return lesk(context, word, pos)


def get_synonyms(word):
    return wordnet.synsets(word)
