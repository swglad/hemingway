""" 
Word sense disambiguation using the Lesk algorithm. 
"""

from nltk.wsd import lesk 
from nltk import word_tokenize

def disambiguate(context, word, pos):
	"""
	@context: a string containing the word whose meaning we want to disambiguate
	@word: the word we want to disambiguate
	@pos: the part of speech 
	Returns: the Synset of the most likely meaning of the word 
	"""

	return lesk(context,word,pos)