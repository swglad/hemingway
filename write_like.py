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

    def style_convert(self, infile, outfile):
        """ For each word in input text, look up synonyms in the
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. """

        input_file = INPUT_FOLDER + "/" + infile + IN_TAG
        output_file = OUTPUT_FOLDER + "/" + outfile + OUT_TAG

        with open(input_file, 'r') as source, open(output_file, 'w') as dest:

            first_write = True

            # Tokenize full input file by spaces + punctuation
            tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
            text = tokenizer.tokenize(source.read())

            if self.debug:
                print "text: ", text

            for word in text:
                orig_word = word  # preserve capitalization
                word = word.strip().lower()
                # Reject non-ASCII characters
                try:
                    word = word.decode('ascii')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    continue

                if self.debug:
                    print
                    print word, "\t-->\t", self.thesaurus[word]

                # Check if word is in thesaurus: copy word exactly if not, replace if yes
                if len(self.thesaurus[word]) == 0:
                    # Word not in thesaurus, so copy original word
                    if first_write:
                        dest.write(orig_word)
                        first_write = False
                    else:
                        dest.write(" " + orig_word)

                else:
                    # Probabilistically choose a synonym in thesaurus[word]
                    weighted_key = self._weighted_choice(word)
                    # Make replaced word uppercase if original word was uppercase
                    if orig_word[0].isupper():
                        weighted_key = weighted_key.title()

                    # Write to output file
                    if first_write:
                        dest.write(weighted_key)
                        first_write = False
                    else:
                        # Don't add a space when printing punctuation
                        if word in string.punctuation:
                            dest.write(orig_word)
                        else:
                            dest.write(" " + weighted_key)

        return outfile

    def _weighted_choice(self, word):
        """
        Returns a probabilistically-selected synonym for a word.

        Works by randomly choosing a number 'n', iterating through
        synonyms in thesaurus[word] in random order, & decreasing
        'n' by the 'weight' (frequency) of each synonym.
        """
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