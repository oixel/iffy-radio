import requests
from bs4 import BeautifulSoup as BS

class DataGrabber:
    # Each marker represents the HTML that comes right before each specific piece of metadata
    COVER_MARKER = 'https://lh3.googleusercontent.com/'
    SONG_MARKER = '"imageStyle":"VIDEO_ATTRIBUTE_IMAGE_STYLE_SQUARE","title":"'
    ARTIST_MARKER = '","subtitle":"'
    ALBUM_MARKER = '"secondarySubtitle":{"content":"'

    def __init__(self, url) -> None:
        # Creates a giant string of the entire HTML for the YouTube video's page.
        html = requests.get(url).content

        # Uses BeautifulSoup to parse through the HTML data and convert it to a "legible" string
        bs = BS(html, "html.parser")
        self.html = bs.prettify()[800000:]  # Everything before ~800000 does not include metadata info

        # Creates an empty dictionary to fill with metadata
        self.metadata = {}

        # Makes sure that first search for album cover starts at the beginning of HTML
        self.prev_end = 0
    
    # Takes marker and searches for it from the previous data's end character index to the end of the HTML
    # Returns: new point to search for next marker from and found data
    def find_data(self, marker, use_offset=True) -> tuple[int, str]:
        # Only turn off offset of marker's character count if specifically stated in function call
        offset = 0 if use_offset == False else len(marker)

        # Start search at last data's end and add offset of character count of marker to make sure it searches past marker
        start = self.html.find(marker, self.prev_end) + offset
        end = self.html.find('"', start)  # " indicates the end of metadata value
        data = self.html[start:end]
        
        # When there is a bug or metadata does not exist, ensure that new_start does not change and data is type None
        if self.prev_end > start or not data:
            new_start = self.prev_end
            data = None
        else:
            # Otherwise, leave data as what it is found to be and updata the new_start to be at the end of current data
            new_start = end
    
        # Returns the value of the new start and the metadata that was found (or not found)
        return new_start, data

    # Gets all desired metadata from self's HTML
    def get_data(self) -> dict:
        # Gets album cover's source
        self.prev_end, self.metadata["cover_src"] = self.find_data(self.COVER_MARKER, False)

        # Gets song's name
        self.prev_end, self.metadata["song"] = self.find_data(self.SONG_MARKER)

        # Gets artist's name
        self.prev_end, self.metadata["artist"] = self.find_data(self.ARTIST_MARKER)

        # Gets album's name
        self.prev_end, self.metadata["album"] = self.find_data(self.ALBUM_MARKER)

        return self.metadata