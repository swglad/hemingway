from collections import defaultdict, Counter
import re
from string import punctuation

CORPUS_FOLDER = "corpus"
THESAURI_FOLDER = "thesauri"
MAPPING_FOLDER = "mappings"
CORP_TAG = ".txt"
THES_TAG = ".thes"
MAP_TAG = ".map"

WORD = "\w+[\'-]?\w*"
PRICE = "\$[\d.]+"
PUNCTUATION_EXCEPT_HYPHEN = '[' + punctuation.replace('-', '') + ']'