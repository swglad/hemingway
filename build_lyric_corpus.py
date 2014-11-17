"""
build_lyric_corpus.py

Web scraper to obtain corpus of lyrics given list of artists from genius.com.
Command line interface, only.
"""

from config import *
from urlparse import urljoin
from bs4 import BeautifulSoup
import requests
import argparse
from build_corpus import tokenize_string

BASE_URL = "http://genius.com"
artist_url = BASE_URL + "/artists/"

ASIDE_REGEX = "\[.*\]$"


def compile_lyrics(artist_name, output_filename):
    response = requests.get(artist_url + artist_name, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})

    soup = BeautifulSoup(response.text, "lxml")

    with open(output_filename, 'a') as f:
        for song_link in soup.select('ul.song_list > li > a'):
            link = urljoin(BASE_URL, song_link['href'])
            response = requests.get(link)
            soup = BeautifulSoup(response.text)
            lyrics = soup.find('div', class_='lyrics').text.strip().split('\n')

            for line in lyrics:

                # Reject non-ASCII lines
                try:
                    line = line.decode('ascii')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    continue

                if not re.match(ASIDE_REGEX, line):
                    f.write(" ".join(tokenize_string(line)) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-artist', '--artist', '-a', '--a', type=str, nargs='+', help='names of musical artists. use - for spaces.', required=True)
    parser.add_argument('-output', '--output', '-o', '--o', type=str, help='name of output corpus.', required=True)

    args = parser.parse_args()

    outfile = CORPUS_FOLDER + "/" + args.output

    # Clear file contents
    open(outfile, 'w').close()

    for artist in args.artist:
        compile_lyrics(artist, outfile)