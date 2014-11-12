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


def my_lesk(tagged_string, desired_word):
    """
    @tagged_string: the string of words in the format 'word1_pos1 word2_pos2...'
    @desired_word: the word we want disambiguated
    Returns: - synset returned by lesk with part of speech (more accurate)
             - synset returned by lesk without pos specified if no pos (less accurate)
             - None if lesk returns nothing
    """
    normal_string=''
    desired_tag=''
    for word_and_tag in tagged_string:
        word = word_and_tag.split('_')[0]
        tag = word_and_tag.split('_')[1]
        if word==desired_word:
            desired_tag = tag

        normal_string+=word+' '

    # ignore proper nouns and punctuation
    if desired_tag=='NNP' or desired_tag=='NNPS' or desired_tag in string.punctuation:
        return None

    # if the POS can be resolved to a wordnet POS, call lesk with POS
    # else call lesk without POS
    wn_pos = ptb_to_wn_pos(desired_tag)
    if wn_pos==None:
        return lesk(normal_string,desired_word)
    else:
        return lesk(normal_string, desired_word, wn_pos)

    # # tagged = pos_tag(word_tokenize(string.decode('ascii','ignore')))
    # disambiguated = []
    # for word_and_tag in string:
    #     word, tag = word_and_tag.split('_')
    #     print "word =",word
    #     print "tag =",tag
    #     # ignore proper nouns
    #     if tag=='NNP' or tag=='NNPS':
    #         temp=[word,tag,None]
    #     else:
    #         temp = [word, tag, lesk(string, word, ptb_to_wn_pos(tag))]
    #         # temp = [word, tag, lesk(string, word)] # doesn't do POS tagging
    #     disambiguated.append(temp)
    # return disambiguated

if __name__=='__main__':
    a= my_lesk("It_PRP was_VBD not_RB fear_NN or_CC dread_NN ._.".split(), 'fear')
    b= my_lesk(["He_PRP" ,"should_MD","have_VB" ,"killed_VBN"], 'killed')
    print a, a.definition()
    print b, b.definition()
    # print my_lesk("Ronald loves jelly beans more than Nancy.")