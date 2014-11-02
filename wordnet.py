"""
wordnet.py

Author: Alex Gerstein

API wrapper to lookup words on
Princeton Wordnet.
"""

from nltk.corpus import wordnet

def get_synonyms(word):
        return wordnet.synsets(word)