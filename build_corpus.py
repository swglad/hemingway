import argparse
from nltk.tokenize import RegexpTokenizer
from string import punctuation

CORPUS_FOLDER = "corpus"
CORP_TAG = ".txt"


def build_corpus(input_filename, output_filename):
    word = '[\w-]+'
    price = '\$[\d\.]+'
    punctuation_except_hyphen = '[' + punctuation.replace('-', '') + ']'

    possible_regexes = [word, price, punctuation_except_hyphen]

    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            line = line.replace("'", '')

            tokenizer = RegexpTokenizer('|'.join(possible_regexes))
            text = tokenizer.tokenize(line)
            outfile.write(" ".join(text) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', '--input', '-in', '--in', '-i', '--i', type=str, help='Filename of original text',
                        required=True)
    parser.add_argument('-output', '--output', '-out', '--out', '-o', '--o', type=str,
                        help='Filename of tokenized output. Do not include folder name.',
                        required=True)
    args = parser.parse_args()

    build_corpus(args.input, CORPUS_FOLDER + "/" + args.output)
