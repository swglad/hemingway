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
from collections import defaultdict
from random import shuffle

class WriteLike:
    def __init__(self):
        self.author = "Hemingway"

if __name__=='__main__':
    Hemingway = WriteLike()
