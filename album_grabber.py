import requests
from bs4 import BeautifulSoup as BS

url = input("What is the youtube url? ")

html = requests.get(url).content

bs = BS(html, "html.parser")

html = bs.prettify()

MARKER = 'https://lh3'

if MARKER in html:
    start = html.find(MARKER)
    end = html.find('"', start)
    src = html[start:end]
    print(src)
else:
    print('No album art available, grabbing thumbnail instead.')