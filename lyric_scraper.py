from urlparse import urljoin
from bs4 import BeautifulSoup
import requests
import argparse
import re


BASE_URL = "http://genius.com"
artist_url = BASE_URL + "/artists/"

ASIDE_REGEX = "\[.*\]$"


def compile_lyrics(artist_name):
    response = requests.get(artist_url + artist_name, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})

    soup = BeautifulSoup(response.text, "lxml")

    with open(artist_name + ".txt", 'w') as f:
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
                    f.write(line + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-artist', '--artist', '-a', '--a', type=str, help='name of musical artist. use - for spaces.', required=True)
    args = parser.parse_args()

    compile_lyrics(args.artist)