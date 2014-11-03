import re
from collections import defaultdict, Counter    
from nltk.tokenize import RegexpTokenizer
import random
import string

THESAURI_FOLDER = "thesauri"
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
THES_TAG = ".thes"
IN_TAG = ".txt"
OUT_TAG = ".out"

class WriteLike:
    def __init__(self, author, debug = False):
        self.author = author
        self.debug = debug
        self.thesaurus = self._read_thesaurus()

    def style_convert(self, infile, outfile):
        ''' For each word in input text, look up synonyms in the 
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. '''

        input_file = INPUT_FOLDER + "/" + infile + IN_TAG
        output_file = OUTPUT_FOLDER + "/" + outfile + OUT_TAG

        with open(input_file, 'r') as source, open(output_file, 'w') as dest:

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
                except (UnicodeDecodeError, UnicodeEncodeError) as e:
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

        return outfile

    def _weighted_choice(self, word):
        ''' 
        Returns a probalistically-selected synonym for a word.

        Works by randomly choosing a number 'n', iterating through
        synonyms in thesaurus[word] in random order, & decreasing 
        'n' by the 'weight' (frequency) of each synonym.
        '''
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

    def _read_thesaurus(self):
        """
        Store pre-processed thesaurus in dict object.
        """
        filename = THESAURI_FOLDER + "/" + self.author + THES_TAG

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