#!/usr/bin/env python
# Authors: Alex Gerstein, Scott Gladstone, Vikram Narayan
# CS 73 Final Project: Write Like Hemingway
# 
# Pseudocode:
# 1. Read in a corpus X from author (e.g. Hemingway)
# 2. For each word w in corpus X:
# 3.    Increment count of w in dict thesaurus
# 4.    Look up all synonyms of w in WordNet
# 5.    Map all synonyms of w to thesaurus[w]
# 6. Read in a user input Y
# 7. For each word y in input Y:
# 8.    If y is in thesarus:
# 9.        Use pdf to map y --> synonym(y) 
#
# Description: 
# Parameters:
# Enhancements:
#

import numpy
import numpy.linalg
from collections import defaultdict, Counter
from random import shuffle

import string, re

import wordnet as wn

class WriteLike:
    def __init__(self, author):
        self.author = author
        self.thesaurus = self._make_thesaurus()

    def _make_thesaurus(self):
    	thesaurus = defaultdict(lambda: Counter())

    	source = open("corpus/" + self.author + ".txt")

    	for line in source:
    		if self._is_title(line):
    			continue

    		for word in line.split():
    			word = word.strip()		\
    						.lower()	\
    						.translate(string.maketrans("",""), 
												string.punctuation)

    			try:
    				word = word.decode('ascii')
    			except UnicodeDecodeError, e:
    				continue
				
    			thesaurus[word].update([word])

    			for syn in wn.get_synonyms(word):
    				syn = syn.name().split(".")[0]
    				thesaurus[syn].update([word])

    	return thesaurus

    def _is_title(self, line):
    	return re.match("^[0-9]*\s?[A-Z\s]+[0-9]*$", line) is not None


if __name__=='__main__':
    wl = WriteLike("hemingway_short")
    print wl.thesaurus
