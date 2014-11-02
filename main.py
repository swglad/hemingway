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

import wordnet as wn         
from nltk.tokenize import RegexpTokenizer    
import operator
import random
import string
import argparse


class WriteLike:
    def __init__(self, author, debug):
        self.author = author
        self.debug = debug
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

    def style_convert(self, infile, outfile):
        ''' For each word in input text, look up synonyms in the 
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. ''' 

        source = open("input/" + infile + ".txt", 'r')
        dest = open("output/" + outfile + ".out", 'w')
        firstWrite = True
        
        # Tokenize full input file by spaces + punctuation
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
        text = tokenizer.tokenize(source.read())
        
        if self.debug:
            print "text: ", text

        for word in text:
            origWord = word     # preserve capitalization
            word = word.strip().lower()
            # Reject non-ASCII characters
            try:
                word = word.decode('ascii')
            except UnicodeDecodeError, e:
                continue

            if self.debug:
                print 
                print word, "\t-->\t", self.thesaurus[word]
            
            # Check if word is in thesaurus: copy word exactly if not, replace if yes
            if len(self.thesaurus[word]) == 0:
                # Word not in thesaurus, so copy original word
                if firstWrite:
                    dest.write(origWord)
                    firstWrite = False
                else:
                    dest.write(" " + origWord)
            
            else: 
                # Probalistically choose a synonym in thesaurus[word]
                weightedKey = self._weighted_choice(word)
                # Make replaced word uppercase if original word was uppercase
                if origWord[0].isupper():
                    weightedKey = weightedKey.title()

                # Write to output file
                if firstWrite:
                    dest.write(weightedKey)
                    firstWrite = False
                else:
                    # Don't add a space when printing punctuation
                    if word in string.punctuation:
                        dest.write(origWord)
                    else:
                        dest.write(" " + weightedKey)

        source.close()
        dest.close()

        return outfile

    def _weighted_choice(self, word):
        ''' Returns a probalistically-selected synonym for a word. '''
        ''' Works by randomly choosing a number 'n', iterating through
            synonyms in thesaurus[word] in random order, & decreasing 
            'n' by the 'weight' (frequency) of each synonym. '''
        # Obtain random normal_pdf weight value from [0, total_weight]
        word_dict = self.thesaurus[word]
        total_weight = sum(word_dict[item] for item in word_dict)
        n = random.uniform(0, total_weight)

        # Randomize word order and select word with weight capturing 'n'
        mixKeys = word_dict.keys()
        random.shuffle(mixKeys)
        for choice in mixKeys:
            weight = word_dict[choice]
            if n < weight:
                return choice
            n = n - weight

        # Return final word as best choice (e.g. tail 'n' value)
        return choice

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-author', type=str, help='name of author', required=True)
    parser.add_argument('-input', type=str, help='user input file', required=True)
    parser.add_argument('-out', type=str, help='filename of output', required=True)
    parser.add_argument('-DEBUG', help=argparse.SUPPRESS, action='store_true', required=False)
    args = parser.parse_args()

    wl = WriteLike(args.author, args.DEBUG)
    wl.style_convert("sample", "a")
