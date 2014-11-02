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

from collections import defaultdict, Counter 	
import string, re 								
import wordnet as wn 							

class WriteLike:
    def __init__(self, author):
        self.author = author
        self.thesaurus = self._make_thesaurus()
    
    def _make_thesaurus(self):
    	''' Returns dict of counters 'thesaurus', where
    		thesaurus[word] = { synonym1: 4, syn2: 8, syn3: 1, ... } '''
    	thesaurus = defaultdict(lambda: Counter())
    	
    	# Build thesaurus from author's corpus
    	source = open("corpus/" + self.author + ".txt")
    	for line in source:
    		if self._is_title(line): # ignore repeated book title
    			continue

    		for word in line.split():
    			word = word.strip()		\
    						.lower()	\
    						.translate(string.maketrans("",""), 
												string.punctuation)
    			# Reject non-ASCII characters
    			try:
    				word = word.decode('ascii')
    			except UnicodeDecodeError, e:
    				continue

    			thesaurus[word].update([word]) # Increment word count

    			# Retrieve syn = synonym[w], add to thesaurus[syn]
    			for syn in wn.get_synonyms(word):
    				syn = syn.name().split(".")[0]
    				thesaurus[syn].update([word])

    	return thesaurus

    def _is_title(self, line):
    	''' Ignore book title if repeated in corpus '''
    	return re.match("^[0-9]*\s?[A-Z\s]+[0-9]*$", line) is not None


if __name__=='__main__':
    wl = WriteLike("hemingway_short")
    print wl.thesaurus
