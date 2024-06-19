import requests
from bs4 import BeautifulSoup as BS

class AlbumGrabber:
    def __init__(self, output_path) -> None:
        self.output_path = output_path
        
    # Returns the source url for the song's album from the HTML data of the YouTube video.
    def get(self, html):
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

    # 
    def download(self, html, name):
        source = self.get(html)
        print(f"Album : {name}\nSource: {source}")

# Allows the Album Grabber to be used as an independent tool.
if __name__ == "__main__":
    url = input("\nWhat is the youtube url? ")
    name = input("What is the name of the album? ")

    AG = AlbumGrabber("output/")
    AG.download(url, name)