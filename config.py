from string import punctuation

CORPUS_FOLDER = "data/corpus"
THESAURI_FOLDER = "data/thesaurus"
MAPPING_FOLDER = "data/mapping"
CORP_TAG = ".txt"
THES_TAG = ".thes"
MAP_TAG = ".map"

WORD = "\w+[\'-]?\w*"
PRICE = "\$[\d.]+"
PUNCTUATION_EXCEPT_HYPHEN = '[' + punctuation.replace('-', '') + ']'