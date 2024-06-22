import urllib
import urllib.request
from bs4 import BeautifulSoup as BS

print("\n\n\n")

# Test input Westcoast Collective: https://www.youtube.com/watch?v=vcZAjGbXEiE&list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa&index=6
html_input = input("What YouTube Link? ")

html = urllib.request.urlopen(html_input).read()

soup = BS(html, "html.parser")

html = soup.prettify()  #bs is your BeautifulSoup object

with open("out.txt","w") as out:
    for i in range(0, len(html)):
        try:
            out.write(html[i])
        except Exception:
            1+1