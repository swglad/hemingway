""" 
lesk.py
Word sense disambiguation using Lesk algorithm and part of speech tagging. 
"""

from nltk.wsd import lesk
from nltk.tag import pos_tag
from nltk import word_tokenize

ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'


def ptb_to_wn_pos(ptb_tag):
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


def pos_tagger(string):
    """
    Returns:
    """
    tagged = pos_tag(word_tokenize(string.decode('ascii','ignore')))
    disambiguated = []
    for word, tag in tagged:
        # ignore proper nouns
        if tag=='NNP' or tag=='NNPS':
            temp=[word,tag,None]
        else:
            temp = [word, tag, lesk(string, word, ptb_to_wn_pos(tag))]
            # temp = [word, tag, lesk(string, word)] # doesn't do POS tagging

        disambiguated.append(temp)

    return disambiguated

if __name__=='__main__':
    print pos_tagger("John's big idea isn't all that bad.")
    print pos_tagger("Ronald loves jelly beans more than Nancy.")