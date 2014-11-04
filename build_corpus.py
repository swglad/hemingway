import argparse
from nltk.tokenize import RegexpTokenizer
from config import *

REGEX = "|".join([WORD, PRICE, PUNCTUATION_EXCEPT_HYPHEN])


def tokenize_string(line):
    tokenizer = RegexpTokenizer(REGEX)
    return tokenizer.tokenize(line)

def build_corpus(input_filename, output_filename):
    """
    Tokenize an input file to use for a corpus, which we
    can later use to build out a thesaurus.

    Saves the output file to the corpus folder.
    """

    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            line = line.replace("'", '')
            outfile.write(" ".join(tokenize_string(line)) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', '--input', '-in', '--in', '-i', '--i', type=str, help='Filename of original text',
                        required=True)
    parser.add_argument('-output', '--output', '-out', '--out', '-o', '--o', type=str,
                        help='Filename of tokenized output. Do not include folder name.',
                        required=True)
    args = parser.parse_args()

    build_corpus(args.input, CORPUS_FOLDER + "/" + args.output)
