import pygame
from mutagen.id3 import ID3
from io import BytesIO

#
class Background:
    def __init__(self, screen, color, position = (0, 0)) -> None:
        self.screen = screen
        self.position = position

        self.surface = pygame.Surface(screen.get_size())
        self.surface.fill(pygame.Color(color))

    def change_color(self, color) -> None:
        self.surface.fill(pygame.Color(color))

    def draw(self) -> None:
        self.screen.blit(self.surface, self.position)


# Handles creation of text objects
class Text:
    def __init__(self, screen, font_path, size, text, color, position) -> None:
        # Stores text's attributes for future use
        self.size = size
        self.screen = screen
        self.text = text
        self.color = color
        self.position = position

        # Creates text object
        self.text_object = pygame.freetype.Font(font_path, self.size)

        self.update_position()

    # Creates rect from text and centers it
    def update_position(self) -> None:
        self.rect = self.text_object.get_rect(self.text)
        self.rect.center = self.position
    
    # Renders text onto screen
    def draw(self) -> None:
        self.text_object.render_to(self.screen, self.rect, self.text, self.color, size = self.size)
    
    # Takes in new string and changes text to display it instead ad then recenters it
    def change_text(self, text) -> None:
        self.text = text
        self.update_position()

# Handles buttons in menus with rendering their different images and pressing functionality
class Button:
    def __init__(self, screen, function, position, image_path, pressed_image_path=None):
        # Stores screen for reference in draw()
        self.screen = screen
        
        # Loads unpressed variant of button's image
        self.regular_image = pygame.image.load(image_path).convert_alpha()
        
        # Loads pressed variant of button's image (if one exists)
        if pressed_image_path != None:
            self.pressed_image = pygame.image.load(pressed_image_path).convert_alpha()

        # Sets button's current image to its unpressed variant
        self.image = self.regular_image

        # Creates a rect from the loaded image
        self.rect = self.image.get_rect()

        # Positions button's rect's center at calculated position
        self.rect.center =  position

        # Assigns the function that is called when button is pressed
        self.function = function

        # Ensures that button can be clicked from its initialization
        self.clicked = False
        
    # Draws button onto the screen and handles function calling on button press
    def draw(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        # Changes button's clicked state and updates image
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # Ensures that button's click functionality only runs once
                self.clicked = True

                # Sets button's image to its pressed variant (if it exists)
                if self.pressed_image != None:
                    self.image = self.pressed_image
        
        # Calls function and resets unpressed boolean when mouse is no longer being pressed down and 
        if self.clicked == True:
            if not pygame.mouse.get_pressed()[0] == 1:
                # Calls this button's stored function
                if self.rect.collidepoint(mouse_pos):
                    self.function()

                # Resets button's click state to allow it to be clicked again
                self.clicked = False

                # Resets button's image to its unpressed variant
                self.image = self.regular_image
        
        # Draws button's current image onto screen at its stored position
        self.screen.blit(self.image, self.rect)

# Handles the song information presented at the center of the screen
class SongInfo:
    # Constant storing the size of cover art image
    IMAGE_SIZE = (150, 150)

    def __init__(self, screen, position) -> None:
        # Stores parameterized screen as object's screen
        self.screen = screen

        # 
        self.position = position

        # Creates empty song info to change when a new song is played
        self.artist = ""
        self.song = ""
        self.album = ""

        artist_text_pos = (position[0], position[1] - 125)
        self.artist_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 16, self.artist, (255, 255, 255), artist_text_pos)

        song_text_pos = (position[0], position[1] - 100)
        self.song_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 24, self.song, (255, 255, 255), song_text_pos)
    
    # Takes in a new MP3 and updates stored song data
    def change_song(self, mp3_path) -> None:
        # Creates ID3 tags from new MP3
        id3 = ID3(mp3_path)

        # Updates stored song info
        self.artist = id3['TPE1'].text[0]
        self.song = id3['TIT2'].text[0]
        
        # Only stores an album name if one exists
        if 'TALB' in id3.keys():
            self.album = id3['TALB'].text[0]
        else:
            self.album = ""

        # Loads in new MP3's embedded cover image
        image_data = id3.getall('APIC')[0].data
        image = BytesIO(image_data)

        # Replaces currently rendered image with newly loaded image
        image = pygame.image.load(image).convert_alpha()
        self.cover_image = pygame.transform.scale(image, self.IMAGE_SIZE)
        self.rect = self.cover_image.get_rect()
        self.rect.center =  self.position

        # Updates song info to new song
        self.artist_text.change_text(self.artist)
        self.song_text.change_text(self.song)

    # Renders song information onto screen
    def draw(self) -> None:
        self.screen.blit(self.cover_image, self.rect)
        self.artist_text.draw()
        self.song_text.draw()
