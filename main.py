#!/usr/bin/env python
''' 
Authors: Alex Gerstein, Scott Gladstone, Vikram Narayan
CS 73 Final Project: Write Like Hemingway

Pseudocode:
1. Read in a corpus X from author (e.g. Hemingway)
2. For each word w in corpus X:
3.    Increment count of w in dict thesaurus
4.    Look up all synonyms of w in WordNet
5.    Map all synonyms of w to thesaurus[w]
6. Read in a user input Y
7. For each word y in input Y:
8.    If y is in thesarus:
9.        Use pdf to map y --> synonym(y) 

Input:
    (1) Tokenized corpus file at 'corpus/author.txt'

Output:

Description:

Parameters:

Enhancements:

'''

import re
from collections import defaultdict, Counter    

THESAURI_FOLDER = "thesauri"                     

class WriteLike:
    def __init__(self, author):
        self.author = author
        self.thesaurus = self._read_thesaurus()

    def _read_thesaurus(self):
        filename = THESAURI_FOLDER + "/" + self.author + ".txt"

        thesaurus = defaultdict(lambda: Counter())

        with open(filename, 'r') as f:  
            for line in f:
                if re.match("^[\s]", line):
                    syn, count = line.strip().split()
                    current_word.update({syn: int(count)})
                else:
                    dict_key = line.strip()
                    current_word = thesaurus[dict_key]

        return thesaurus

if __name__=='__main__':
    wl = WriteLike("hemingway_short")
    print wl.thesaurus
