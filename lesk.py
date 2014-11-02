""" 
lesk.py
Word sense disambiguation using Lesk algorithm and part of speech tagging. 
"""

from nltk.wsd import lesk 
from nltk.tag import pos_tag 
from nltk import word_tokenize
import pdb

def ptb_to_wn_pos(ptb_tag):
	"""
	Converts Penn Tree bank pos tags to wordet part of speech tags.
	"""
	ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
	wn_pos=''

	if ptb_tag[0]=='V':
		wn_pos = VERB
	elif ptb_tag[0]=='N':
		wn_pos = NOUN
	elif ptb_tag[0]=='J':
		wn_pos = ADJ
	elif ptb_tag[0]=='R':
		wn_pos = ADV
	else:
		wn_pos = None


def pos_tagger(string):
	"""
	Returns:
	"""
	tagged = pos_tag(word_tokenize(string))
	disambiguated = []
	for word, tag in tagged:
		temp = [word, tag, lesk(string, word, ptb_to_wn_pos(tag) )]
		disambiguated.append(temp)

	pdb.set_trace()
	return disambiguated

pos_tagger("John's big idea isn't all that bad.")