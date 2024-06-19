import urllib
import urllib.request
from bs4 import BeautifulSoup as BS

print("START\n\n\n")
html = urllib.request.urlopen("https://www.youtube.com/watch?v=ws5K_5G_xvI").read()

soup = BS(html)

html = soup.prettify()  #bs is your BeautifulSoup object

with open("out.txt","w") as out:
    for i in range(0, len(html)):
        try:
            out.write(html[i])
        except Exception:
            1+1