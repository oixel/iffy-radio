import urllib
import urllib.request
from bs4 import BeautifulSoup as BS

html = urllib.request.urlopen("https://www.youtube.com/watch?v=ws5K_5G_xvI").read()

bs = BS(html, "html.parser")

html = bs.prettify()

MARKER = '{"image":{"sources":[{"url":"'

if MARKER in html:
    start = html.find(MARKER) + len(MARKER)
    end = start
    for i in range(start, len(html)):
        if html[i] == '"':
            end = i
            break
    src = html[start:end]
    print(src)
else:
    print("No album art available, grabbing thumbnail instead")