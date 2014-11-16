import config
import random
import string
import re
from collections import defaultdict, Counter
from build_corpus import tokenize_string

import nltk
from nltk.wsd import lesk as nltk_lesk
from lesk import reduce_pos_tagset

class WriteLike:
    def __init__(self, author, fast=True):
        self.author = author

        # added for Lesk
        if fast is False:
            self.thesaurus = self._read_thesaurus()
        else:
            self.thesaurus = self._read_thesaurus_lesk()

    def style_convert(self, infile_name, outfile_name):
        """ For each word in input text, look up synonyms in the
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. """

        with open(infile_name, 'r') as infile, open(outfile_name, 'w') as outfile:

            for line in infile:

                # Tokenize full input file by spaces + punctuation (not apostrophe/hyphen)
                text = tokenize_string(line)

                for index, orig_word in enumerate(text):
                    was_title = orig_word.istitle()        # "Title"
                    was_capitalized = orig_word.isupper()  # "UPPER"
                    was_lower = orig_word.islower()        # "lower"

                    word = orig_word.strip().lower()

                    # Reject non-ASCII characters
                    try:
                        word = word.decode('ascii')
                    except (UnicodeDecodeError, UnicodeEncodeError):
                        continue

                    # Probabilistically choose a synonym in thesaurus[word]
                    weighted_key = self._weighted_choice(word)

                    # Match capitalization of original word
                    if was_title:
                        weighted_key = weighted_key.title()
                    elif was_capitalized:
                        weighted_key = weighted_key.upper()
                    elif not was_lower: 
                        weighted_key = orig_word

                    # Add a space between words, no space for punctuation
                    if word not in string.punctuation and index != 0:
                        outfile.write(" ")

                    outfile.write(weighted_key)
                outfile.write('\n')

        return outfile_name


    def style_convert_lesk(self, infile_name, outfile_name):
        """ For each word in input text, look up synonyms in the
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. """

        with open(infile_name, 'r') as infile, open(outfile_name, 'w') as outfile:

            for line in infile:

                # POS tag, and then lesk-ify the input,
                # look it up in the thesauri
                try:
                    line = line.decode('ascii','ignore')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    continue
                line = tokenize_string(line)

                tagged_tuples = nltk.pos_tag(line)

                tagged_string = '' # tagged string
                untagged_string = '' # normal string
                for word, tag in tagged_tuples:
                    untagged_string += word + ' '
                    tagged_string += word + '_' + tag + ' '

                for index, original_word in enumerate(tagged_string.split()):

                    (orig_word, temp_pos) = tuple(original_word.split('_'))

                    word = orig_word.strip().lower()

                    was_title = orig_word.istitle()        # "Title"
                    was_capitalized = orig_word.isupper()  # "UPPER"
                    was_lower = orig_word.islower()        # "lower"

                    # converts penn tree bank parts of speech to wordnet parts of speech
                    wordnet_pos = reduce_pos_tagset(temp_pos)
                    if wordnet_pos is not None:
                        synset = nltk_lesk(untagged_string, orig_word.strip().lower(), wordnet_pos)
                    else:
                        synset = nltk_lesk(untagged_string, orig_word.strip().lower())

                    # Probabilistically choose a synonym in thesaurus[synset]
                    weighted_key = self._weighted_choice_lesk(str(synset), word)

                    # Match capitalization of original word
                    if was_title:
                        weighted_key = weighted_key.title()
                    elif was_capitalized:
                        weighted_key = weighted_key.upper()
                    elif not was_lower: 
                        weighted_key = orig_word

                    # Add a space between words, no space for punctuation
                    if word not in string.punctuation and index != 0: 
                        outfile.write(" ")

                    outfile.write(weighted_key)
                outfile.write('\n')

        return outfile_name


    def _weighted_choice_lesk(self, synset, orig_word):
        """
        Returns a probabilistically-selected synonym for a word.

        Works by randomly choosing a number 'n', iterating through
        synonyms in thesaurus[word] in random order, & decreasing
        'n' by the 'weight' (frequency) of each synonym.
        """
        if not synset or synset not in self.thesaurus:
            return self._weighted_choice(orig_word) 

        # Obtain random normal_pdf weight value from [0, total_weight]
        word_dict = self.thesaurus[synset]
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

    def _read_thesaurus_lesk(self):
        """
        Store pre-processed thesaurus in dict object.
        """
        filename = config.THESAURI_FOLDER + "/" + self.author +'_interpolate'+ config.THES_TAG
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