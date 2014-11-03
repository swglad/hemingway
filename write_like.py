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
    def __init__(self, author, debug=False):
        self.author = author
        self.debug = debug
        self.thesaurus = self._read_thesaurus()

    def style_convert(self, infile_name, outfile_name):
        """ For each word in input text, look up synonyms in the
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. """

        input_file = INPUT_FOLDER + "/" + infile_name + IN_TAG
        output_file = OUTPUT_FOLDER + "/" + outfile_name + OUT_TAG

        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:

            first_write = True

            # Tokenize full input file by spaces + punctuation
            tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
            text = tokenizer.tokenize(infile.read())

            if self.debug:
                print "text: ", text

            for word in text:
                was_capitalized = word.istitle()
                word = word.strip().lower()

                # Reject non-ASCII characters
                try:
                    word = word.decode('ascii')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    continue

                if self.debug:
                    print
                    print word, "\t-->\t", self.thesaurus[word]

                # Probabilistically choose a synonym in thesaurus[word]
                weighted_key = self._weighted_choice(word)

                # Mirror capitalization of original word
                if was_capitalized:
                    weighted_key = weighted_key.title()

                # Add a space when word is not punctuation
                # and word is not first word in line
                if word not in string.punctuation and not first_write:
                    outfile.write(" ")

                outfile.write(weighted_key)
                first_write = False

        return outfile_name

    def _weighted_choice(self, word):
        """
        Returns a probabilistically-selected synonym for a word.

        Works by randomly choosing a number 'n', iterating through
        synonyms in thesaurus[word] in random order, & decreasing
        'n' by the 'weight' (frequency) of each synonym.
        """
        if word not in self.thesaurus:
            return word

        # Obtain random normal_pdf weight value from [0, total_weight]
        word_dict = self.thesaurus[word]
        total_weight = sum(word_dict[item] for item in word_dict)
        n = random.uniform(0, total_weight)

        # Randomize word order and select word with weight capturing 'n'
        mix_keys = word_dict.keys()
        random.shuffle(mix_keys)
        for choice in mix_keys:
            weight = word_dict[choice]
            if n < weight:
                return choice
            n = n - weight

        # Return final word as best choice (e.g. tail 'n' value)
        return mix_keys[-1]

    def _read_thesaurus(self):
        """
        Store pre-processed thesaurus in dict object.
        """
        filename = THESAURI_FOLDER + "/" + self.author + THES_TAG

        thesaurus = defaultdict(lambda: Counter())

        with open(filename, 'r') as f:
            for line in f:
                if not re.match('^[\s]', line):
                    dict_key = line.strip()
                    current_word = thesaurus[dict_key]
                else:
                    syn, count = line.strip().split()
                    current_word.update({syn: int(count)})
        return thesaurus