import requests
from bs4 import BeautifulSoup as BS

def get_album_cover(url):
    html = requests.get(url).content

    bs = BS(html, "html.parser")

    html = bs.prettify()

    MARKER = 'https://lh3'

    if MARKER in html:
        start = html.find(MARKER)
        end = html.find('"', start)
        source = html[start:end]
        return source
    else:
        return 'No album art available, grabbing thumbnail instead.'

if __name__ == "__main__":
    url = input("\nWhat is the youtube url? ")

    get_album_cover(url)