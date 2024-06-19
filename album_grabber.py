import requests
from bs4 import BeautifulSoup as BS

# Returns the source url for the song's album from the HTML data of the YouTube video.
def get_album_cover(url):
    # Creates a giant string of the entire HTML for the YouTube video's page.
    html = requests.get(url).content

    # Uses BeautifulSoup to parse through the HTML data and convert it to a "legible" string
    bs = BS(html, "html.parser")
    html = bs.prettify()

    # Indicates the start of the desired image's source (the album cover hidden under description).
    MARKER = 'https://lh3'

    # If the video contains an album image, find and return the entire URL link to the image.
    if MARKER in html:
        start = html.find(MARKER)
        end = html.find('"', start)
        source = html[start:end]
        return source
    # Otherwise, the video does not have a proper album cover attached to it :(
    else:
        print('No album art available, grabbing thumbnail instead.')
        print("NEED TO IMPLEMENT THIS STILL ~ ♥")
        return 'https://www.gstatic.com/youtube/img/watch/yt_music_channel.jpeg'

# Allows the Album Grabber to be used as an independent tool.
if __name__ == "__main__":
    url = input("\nWhat is the youtube url? ")

    get_album_cover(url)