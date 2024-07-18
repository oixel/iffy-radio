import pygame
from mutagen.id3 import ID3
from io import BytesIO

#
class Text:
    def __init__(self, screen, font_path, size, text, color, position) -> None:
        #
        self.screen = screen
        self.text = text
        self.color = color
        self.reg_pos = position

        self.text_object = pygame.freetype.Font(font_path, size)

        self.update_position()

    # 
    def update_position(self) -> None:
        text_rect = self.text_object.get_rect(self.text)
        width, height = text_rect.width, text_rect.height
        self.position = (self.reg_pos[0] - width / 2, self.reg_pos[1] - height / 2)
    
    # 
    def draw(self) -> None:
        self.text_object.render_to(self.screen, self.position, self.text, self.color)
    
    # 
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

        # Ensures the button's image's center is placed at paramterized position
        x = position[0] - (self.rect.size[0] / 2)
        y = position[1] - (self.rect.size[1] / 2)
        self.position = (x, y) 

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
                self.function()

                # Resets button's click state to allow it to be clicked again
                self.clicked = False

                # Resets button's image to its unpressed variant
                self.image = self.regular_image
        
        # Draws button's current image onto screen at its stored position
        self.screen.blit(self.image, self.position)

# Handles the song information presented at the center of the screen
class SongInfo:
    # Constant storing the size of cover art image
    IMAGE_SIZE = (150, 150)

    def __init__(self, screen, mp3_path, position) -> None:
        # Stores parameterized screen as object's screen
        self.screen = screen

        # Creates ID3 tags object from MP3 at given path
        id3 = ID3(mp3_path)

        # Stores MP3's ID3 tag info
        self.artist = id3['TPE1'].text[0]
        self.song = id3['TIT2'].text[0]
        self.album = id3['TALB'].text[0]
        
        # Loads in embedded cover art as byte data
        image_data = id3.getall('APIC')[0].data
        image = BytesIO(image_data)

        # Creates image square from embedded image data
        image = pygame.image.load(image).convert_alpha()
        self.cover_image = pygame.transform.scale(image, self.IMAGE_SIZE)

        # Creates a rect from the loaded image
        self.rect = self.cover_image.get_rect()

        # Ensures the button's image's center is placed at paramterized position
        x = position[0] - (self.rect.size[0] / 2)
        y = position[1] - (self.rect.size[1] / 2)
        self.cover_position = (x, y) 

        # Positions button's rect's center at calculated position
        self.rect.center =  position

        song_text_pos = (self.rect.center[0], self.rect.center[1] - 100)
        self.song_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 24, self.song, (255, 255, 255), song_text_pos)
    
    # Takes in a new MP3 and updates stored song data
    def update_data(self, mp3_path) -> None:
        # Creates ID3 tags from new MP3
        id3 = ID3(mp3_path)

        # Updates stored song info
        self.artist = id3['TPE1'].text[0]
        self.song = id3['TIT2'].text[0]
        self.album = id3['TALB'].text[0]

        # Loads in new MP3's embedded cover image
        image_data = id3.getall('APIC')[0].data
        image = BytesIO(image_data)

        # Replaces currently rendered image with newly loaded image
        image = pygame.image.load(image).convert_alpha()
        self.cover_image = pygame.transform.scale(image, self.IMAGE_SIZE)
        self.rect = self.cover_image.get_rect()
        self.rect.center =  self.cover_position

        # 
        self.song_text.change_text(self.song)

    # Draws song information onto screen
    def draw(self) -> None:
        self.screen.blit(self.cover_image, self.cover_position)
        self.song_text.draw()
