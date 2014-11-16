import config
import glob
import wordnet as wn
from collections import defaultdict, Counter
import re
import lesk

BOOK_TITLE_REGEX = '^[0-9]*\s?[A-Za-z\s]+[0-9]*$'

MAP_WEIGHT = 1.65   # overweight directly-mapped word counts
WINDOW = 4

def _is_title(line):
    """
    Ignore book title if repeated in corpus
    """
    return re.match(BOOK_TITLE_REGEX, line) is not None

def make_thesaurus(file_path):
    """
    Returns dict of counters 'thesaurus', where
    thesaurus[word] = { synonym1: 4, syn2: 8, syn3: 1, ... }
    """
    thesaurus = defaultdict(lambda: Counter())

    with open(file_path, 'r') as f:
        for line in f:

            # Ignore repeated book title headers
            if _is_title(line):
                continue

            for word in line.split():
                word = word.strip().lower()

                # Reject non-ASCII characters
                try:
                    word = word.decode('ascii')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    continue

                # Reject whitespace character
                if re.match("^[\s]*$", word):
                    continue

                # Increment word count of word w
                thesaurus[word].update([word])

                # Retrieve syn = synonym[w], add to thesaurus[syn]
                for syn in wn.get_synonyms(word):
                    syn = syn.name().split(".")[0]
                    thesaurus[syn].update([word])

    # Update thesaurus with mappings, if map_file exists
    file_path = file_path.replace(config.CORPUS_FOLDER, config.MAPPING_FOLDER)
    map_file = file_path.replace(config.CORP_TAG, config.MAP_TAG)
    thesaurus = _add_mappings(map_file, thesaurus)

    return thesaurus

def make_thesaurus_lesk(file_path):
    """
    Returns dict of counters 'thesaurus', where
    thesaurus[synset] = { word1: 4, word2: 8, word3: 1, ... }
    """
    thesaurus = defaultdict(lambda: Counter())

    with open(file_path, 'r') as f:

        f = f.read().split()
        for i, word_and_tag in enumerate(f):

            word = word_and_tag.split('_')[0]
            tag = word_and_tag.split('_')[1]

            # Reject non-ASCII characters
            try:
                word = word.decode('ascii')
            except (UnicodeDecodeError, UnicodeEncodeError):
                continue

            # look at a window of 9 words each time lesk is called
            window = [i - WINDOW, i + WINDOW]
            if i < WINDOW:
                window = [i, i + 2 * WINDOW]
            elif i >= len(f) - WINDOW:
                window = [i - 2 * WINDOW, i]

            synset = lesk.my_lesk(f[window[0]:window[1]], word)

            # if lesk can decide on a meaning for that word, add
            # that meaning, i.e., that synset, to thesaurus
            if synset is None:
                continue

            thesaurus[synset].update([word.lower()])

    # Update thesaurus with mappings, if map_file exists
    file_path = file_path.replace(config.CORPUS_FOLDER_LESK, config.MAPPING_FOLDER)
    map_file = file_path.replace(config.CORP_TAG, config.MAP_TAG)
    thesaurus = _add_mappings(map_file, thesaurus)
    return thesaurus

def write_thesaurus(file_path, thesaurus):
    """
    Writes thesaurus to output file as: word\n \tsyn1 38\n \tsyn2 12 ...
    """
    file_path = file_path.replace(config.CORPUS_FOLDER, config.THESAURI_FOLDER)
    file_path = file_path.replace(config.CORP_TAG, config.THES_TAG)

    with open(file_path, 'w') as f:
        for word in thesaurus:
            f.write(word + "\n")

            for syn in thesaurus[word]:
                f.write("\t" + syn + " " + str(thesaurus[word][syn]) + "\n")


def write_thesaurus_lesk(file_path, thesaurus):
    """
    Writes thesaurus to output file as: Synset\n \tsyn1 38\n \tsyn2 12 ...
    """
    file_path = file_path.replace(config.CORPUS_FOLDER_LESK, config.THESAURI_FOLDER)
    file_path = file_path.replace(config.CORP_TAG, config.THES_TAG)

    with open(file_path, 'w') as f:
        for synset in thesaurus:
            f.write(str(synset) + "\n")

            for syn in thesaurus[synset]:
                f.write("\t" + syn + " " + str(thesaurus[synset][syn]) + "\n")

def _add_mappings(mapping_file, thesaurus):
    """
    Uses map_file to add word-to-word mappings to thesaurus
    (e.g. Shakespeare: "you" --> {"you", "thy", "thou", ...})
    """
    # Update thesaurus with mappings, if map_file exists
    try:
        with open(mapping_file) as map_file:
            print "Mapping to Thesaurus:", mapping_file
            for line in map_file:

                if line is None: #added to
                    continue     #prevent none

                author_word, user_word = map(str.lower, line.strip().split())

                # Reject non-ASCII characters
                try:
                    author_word = author_word.decode('ascii')
                    user_word = user_word.decode('ascii')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    continue

                # e.g. thesaurus["you"]["thy"] = thesaurus["thy"]["thy"]
                thesaurus[user_word][author_word] = \
                        int(MAP_WEIGHT * thesaurus[author_word][author_word])
    except IOError:
        pass

    return thesaurus


import pdb
if __name__ == "__main__":
    print "Starting to make thesauri..."
    for file_name in glob.glob(config.CORPUS_FOLDER_LESK + "/*_tagged" + config.CORP_TAG):
        print "Making Thesaurus:", file_name
        author_thesaurus = make_thesaurus_lesk(file_name)
        file_name = file_name.replace(config.CORPUS_FOLDER, config.THESAURI_FOLDER)

        print "Writing To File:", file_name.replace(config.CORP_TAG, config.THES_TAG)
        write_thesaurus_lesk(file_name, author_thesaurus)
    print "Done!"
