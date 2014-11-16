#!/usr/bin/env python
"""
main.py

Authors: Alex Gerstein, Scott Gladstone, Vikram Narayan
CS 73 Final Project: Write Like Hemingway

See README.md at https://github.com/swglad/hemingway.git

Pseudocode:
1. Read in a corpus X from author (e.g. Hemingway)
2. For each word w in corpus X:
3.    Increment count of w in dict thesaurus
4.    Look up all synonyms of w in WordNet
5.    Map all synonyms of w to thesaurus[w]
6. Read in a user input Y
7. For each word y in input Y:
8.    If y is in thesaurus:
9.        Probabilistically map y --> synonym(y)

Requirements:
    Directories: 
        corpus
        thesaurus
        mapping
    Modules: 
        NLTK
        NLTK-Data - WordNet
        NLTK Punkt
        NLTK tagging/max_ent_pos_tagger/english.pickle

Input: 
    Text file of user input to convert

Output:
    Text file of replaced output using user text

Parameters:
    -author:    name of author to convert style to
    -input:     user input  
    -output:    output text
    -fast:      non-Lesk, non-POS tagging mode
"""

from write_like import WriteLike
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-author', '--author', '-a', '--a', type=str, help='name of author', required=True)
    parser.add_argument('-input', '--input', '-in', '--in', '-i', '--i', type=str, help='user input file',
                        required=True)
    parser.add_argument('-output', '--output', '-out', '--out', '-o', '--o', type=str, help='filename of output',
                        required=True)
    parser.add_argument('-fast', '--fast', '-nolesk', '--nolesk', '-f', '--f', action='store_true', required=False)
    args = parser.parse_args()

    wl = WriteLike(args.author)
    
    if args.fast:
        wl.style_convert(args.input, args.output)
    else:
        wl.style_convert_lesk(args.input, args.output)
