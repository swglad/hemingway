""" 
lesk.py
Word sense disambiguation using Lesk algorithm and part of speech tagging. 
"""

from nltk.wsd import lesk
from nltk.tag import pos_tag
from nltk import word_tokenize
import config
import string

ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'

def reduce_pos_tagset(ptb_tag):
    """
    Converts Penn Tree bank pos tags to wordnet pos tags.
    """

    if ptb_tag[0] == 'V':
        wn_pos = VERB
    elif ptb_tag[0] == 'N':
        wn_pos = NOUN
    elif ptb_tag[0] == 'J':
        wn_pos = ADJ
    elif ptb_tag[0] == 'R':
        wn_pos = ADV
    else:
        wn_pos = None

    return wn_pos

def my_lesk(tagged_strings, desired_word):
    """
    @tagged_string: the string of words in the format 'word1_pos1 word2_pos2...'
    @desired_word: the word we want disambiguated
    Returns: - synset returned by lesk with part of speech (more accurate)
             - synset returned by lesk without pos specified if no pos (less accurate)
             - None if lesk returns nothing
    """
    normal_string = ''
    desired_tag = ''
    for tagged_string in tagged_strings:
        word, tag = tagged_string.rsplit("_", 1)

        # Reject non-ASCII characters
        try:
            word = word.decode('ascii')
        except (UnicodeDecodeError, UnicodeEncodeError):
            continue

        if word == desired_word:
            desired_tag = tag

        normal_string += word + ' '

    # ignore proper nouns and punctuation
    if desired_tag == 'NNP' or desired_tag == 'NNPS' or desired_tag in string.punctuation:
        return None

    # if the POS can be resolved to a wordnet POS, call lesk with POS
    # else call lesk without POS
    wn_pos = reduce_pos_tagset(desired_tag)
    if not wn_pos:
        return lesk(normal_string,desired_word)
    else:
        return lesk(normal_string, desired_word, wn_pos)