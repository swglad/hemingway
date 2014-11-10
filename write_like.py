import config
import random
import string
import re
from collections import defaultdict, Counter
from build_corpus import tokenize_string

class WriteLike:
    def __init__(self, author, debug=False):
        self.author = author
        self.debug = debug
        self.thesaurus = self._read_thesaurus()

    def style_convert(self, infile_name, outfile_name):
        """ For each word in input text, look up synonyms in the
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. """

        with open(infile_name, 'r') as infile, open(outfile_name, 'w') as outfile:

            for line in infile:

                # Tokenize full input file by spaces + punctuation (not apostrophe/hyphen)
                text = tokenize_string(line)

                if self.debug:
                    print "text: ", text

                for index, orig_word in enumerate(text):
                    was_title = orig_word.istitle()        # "Title"
                    was_capitalized = orig_word.isupper()  # "UPPER"
                    
                    word = orig_word.strip().lower()

                    # Reject non-ASCII characters
                    try:
                        word = word.decode('ascii')
                    except (UnicodeDecodeError, UnicodeEncodeError):
                        continue

                    if self.debug:
                        print
                        print word,
                        if word in self.thesaurus:
                            print "\t-->\t", self.thesaurus[word]
                        else:
                            print "\t-->\t Empty"

                    # Probabilistically choose a synonym in thesaurus[word]
                    weighted_key = self._weighted_choice(word)

                    # Match capitalization of original word
                    if was_title:
                        weighted_key = weighted_key.title()
                    elif was_capitalized:
                        weighted_key = weighted_key.upper()
                    elif not orig_word.islower(): 
                        weighted_key = orig_word

                    # Add a space between words, no space for punctuation
                    if word not in string.punctuation and index != 0:
                        outfile.write(" ")

                    outfile.write(weighted_key)
                outfile.write('\n')

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
        filename = config.THESAURI_FOLDER + "/" + self.author + config.THES_TAG

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