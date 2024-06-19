import requests
from bs4 import BeautifulSoup as BS
import album_grabber as AG

class DataGrabber:
    COVER_MARKER = 'https://lh3'
    SONG_MARKER = '"imageStyle":"VIDEO_ATTRIBUTE_IMAGE_STYLE_SQUARE","title":"'
    ARTIST_MARKER = '","subtitle":"'
    ALBUM_MARKER = '"secondarySubtitle":{"content":"'

    def __init__(self, url) -> None:
        # Creates a giant string of the entire HTML for the YouTube video's page.
        html = requests.get(url).content

        # Uses BeautifulSoup to parse through the HTML data and convert it to a "legible" string
        bs = BS(html, "html.parser")
        self.html = bs.prettify()

        # Creates an empty dictionary to fill with metadata
        self.metadata = {}

        self.start = 0
    
    # 
    def find_data(self, marker, old_start, offset):
        start = self.html.find(marker, old_start) + offset
        end = self.html.find('"', start)
        data = self.html[start:end]
        
        new_start = end if start != -1 else old_start
        
        if not data:
            data = None

        return new_start, data

    #
    def get_data(self):
        # Gets album cover's source
        self.search_start, self.metadata["cover_src"] = self.find_data(self.COVER_MARKER, self.start, 0)

        # Gets song's name
        offset = len(self.SONG_MARKER)
        self.search_start, self.metadata["song"] = self.find_data(self.SONG_MARKER, self.start, offset)

        # Gets artist's name
        offset = len(self.ARTIST_MARKER)
        self.search_start, self.metadata["artist"] = self.find_data(self.ARTIST_MARKER, self.start, offset)

        # Gets album's name
        offset = len(self.ALBUM_MARKER)
        self.search_start, self.metadata["album"] = self.find_data(self.ALBUM_MARKER, self.start, offset)

        return self.metadata