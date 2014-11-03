import glob

from collections import defaultdict, Counter    
import string, re                               
import wordnet as wn 

CORPUS_FOLDER = "corpus"
THESAURI_FOLDER = "thesauri"
MAP_FOLDER = "mappings"

def _is_title(line):
    '''
    Ignore book title if repeated in corpus
    '''
    return re.match("^[0-9]*\s?[A-Z\s]+[0-9]*$", line) is not None

def make_thesaurus(filepath):
    '''
    Returns dict of counters 'thesaurus', where
    thesaurus[word] = { synonym1: 4, syn2: 8, syn3: 1, ... }
    '''
    thesaurus = defaultdict(lambda: Counter())

    with open(filepath, 'r') as f:
        for line in f:

            # Ignore repeated book title headers
            if _is_title(line): 
                continue

            for word in line.split():
                word = word.strip().lower()

                # Reject non-ASCII characters
                try:
                    word = word.decode('ascii')
                except UnicodeDecodeError, e:
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

    ######## TODO #########
    # IF a map file exists for this author:
    #   author_mapfile = GET_THAT_FILE_NAME
    #   thesaurus = add_mappings(author_mapfile, thesaurus)

    return thesaurus

def write_thesaurus(filepath, thesaurus):
    filepath = filepath.replace(CORPUS_FOLDER, THESAURI_FOLDER)
    with open(filepath, 'w') as f:
        for word in thesaurus:
            f.write(word + "\n")

            for syn in thesaurus[word]:
                f.write("\t" + syn + " " + str(thesaurus[word][syn]) + "\n")

def add_mappings(mapping_file, thesaurus):
    '''
    Uses mapfile to add word-to-word mappings to thesaurus 
    (e.g. Shakespeare: "thy" -> "you")
    '''
    mapfile = open(MAP_FOLDER + mapping_file + ".map")

    for line in mapfile:
        line = line.strip().split()
        authorWord = line[0].lower()
        userWord = line[2].lower()
        # e.g. thesaurus["you"]["thy"] = thesaurus["you"]["you"]
        thesaurus[userWord][authorWord] = thesaurus[userWord][userWord]

    mapfile.close()

    return thesaurus 

if __name__ == "__main__":
    print "Starting to make thesauri..."
    for fname in glob.glob(CORPUS_FOLDER + "/*.txt"):
        print "Making Thesaurus:", fname
        thesaurus = make_thesaurus(fname)
        print "Writing To File:", fname
        write_thesaurus(fname, thesaurus)
    print "Done!"