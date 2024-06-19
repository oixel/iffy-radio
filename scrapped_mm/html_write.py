import urllib
import urllib.request
from bs4 import BeautifulSoup as BS

print("START\n\n\n")
html = urllib.request.urlopen("https://www.youtube.com/watch?v=bIX_ouNJsTs&list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa&index=9").read()

soup = BS(html, "html.parser")

html = soup.prettify()[850000:]  #bs is your BeautifulSoup object

with open("out.txt","w") as out:
    for i in range(0, len(html)):
        try:
            out.write(html[i])
        except Exception:
            1+1