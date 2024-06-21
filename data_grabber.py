import requests
from bs4 import BeautifulSoup as BS

class DataGrabber:
    # Each marker represents the HTML that comes right before each specific piece of metadata
    COVER_MARKER = 'https://lh3.googleusercontent.com/'
    SONG_MARKER = '"}]},"imageStyle":"VIDEO_ATTRIBUTE_IMAGE_STYLE_SQUARE","title":"'
    ARTIST_MARKER = '","subtitle":"'  # MAKE ARTIST MARKER INCLUDE TITLE
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

        try:
            # Start search at last data's end and add offset of character count of marker to make sure it searches past marker
            start = self.html.index(marker, self.prev_end) + offset
            end = self.html.index('"', start)  # " indicates the end of metadata value
            data = self.html[start:end]
            
            # Ensures that there is no indexing bug for a cover source that does not actually exists
            if data != None:
                if not use_offset and self.COVER_MARKER not in data:
                    raise
            
            # Only gets called if no error was raised
            new_start = end
        except:
            new_start = self.prev_end
            data = None
        
        
    
        # Returns the value of the new start and the metadata that was found (or not found)
        return new_start, data

    # Alters the empty values in metadata to mirror YouTube video's information
    def set_filler(self) -> None:
        # If no album cover art is available, set cover to cropped YouTube thumbnail
        if self.metadata["cover_src"] == None:
            self.metadata["cover_src"] = "https://i.ibb.co/DDKn0JH/starcat.jpg"
        
        # If no song title is available, set title to YouTube video's title
        if self.metadata["title"] == None:
            self.metadata["title"] = "YouTube Title"

        # If not artist name is available, set artist name to YouTube video's creator
        if self.metadata["artist"] == None:
            self.metadata["artist"] = "YouTube Creator"
        
        # Just set album to an empty string instead of None since there is no relevant info
        if self.metadata["album"] == None:
            self.metadata["album"] = ""

    # Gets all desired metadata from self's HTML
    def get_data(self) -> dict:
        # Gets album cover's source
        self.prev_end, self.metadata["cover_src"] = self.find_data(self.COVER_MARKER, False)
        
        # Gets song's title
        self.prev_end, self.metadata["title"] = self.find_data(self.SONG_MARKER)
        #
        # CHANGE THIS WHEN I MAKE PROPER NAME CLEANER
        #
        if self.metadata["title"] != None:
            if "u0026" in self.metadata["title"]:
                self.metadata["title"] = self.metadata["title"].replace("\\", "").replace("u0026", "&")
        #   
        #
        #

        # Gets artist's name
        artist_marker = f'"{self.metadata}{self.ARTIST_MARKER}'
        self.prev_end, self.metadata["artist"] = self.find_data(artist_marker)

        # Gets album's name
        self.prev_end, self.metadata["album"] = self.find_data(self.ALBUM_MARKER)

        # Ensures that song does not leave with no information
        if None in self.metadata.values():
            self.set_filler()

        return self.metadata