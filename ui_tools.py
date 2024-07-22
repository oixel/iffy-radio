import pygame
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from io import BytesIO
from time import time

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

        # Stores position of cover art's center which is used in referenced by the positions of everything else
        self.position = position

        # Creates empty song info to change when a new song is played
        self.artist = ""
        self.song = ""
        self.album = ""
        self.length = 0
        
        # Initializes text stating artist's name
        artist_text_pos = (position[0], position[1] - 125)
        self.artist_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 16, self.artist, (255, 255, 255), artist_text_pos)

        # Intiailizes text stating song's name
        song_text_pos = (position[0], position[1] - 100)
        self.song_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 24, self.song, (255, 255, 255), song_text_pos)

        # Initializes progress bar
        self.progress_bar = ProgressBar(screen, (position[0], position[1] + 85))
    
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
        
        # Stores songs length in seconds and updates how much the progress bar should increment every second
        self.length = MP3(mp3_path).info.length
        self.progress_bar.reset(self.length)

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

    # Changes paused state of progress bar when pause button is pressed
    def change_pause(self, paused) -> None:
        self.progress_bar.change_pause(paused)

    # Renders song information onto screen
    def draw(self) -> None:
        self.screen.blit(self.cover_image, self.rect)
        self.artist_text.draw()
        self.song_text.draw()
        self.progress_bar.draw()

class ProgressBar:
    def __init__(self, screen, position) -> None:
        # Initializes default attributes of progress bar
        BAR_SIZE = (200, 10)
        back_color = (0, 0, 0)
        self.playing_color = (255, 0, 0)
        self.paused_color = (90, 90, 90)
        progress_color = self.playing_color

        # Stores basic variables depending on parameters
        self.screen = screen
        self.position = position

        # Set values for variables used in incrementation
        self.increment = 0
        self.paused = False
        self.time_spent_paused = 0

        # Creates background rectangle at center of screen, under cover art
        self.back_rect = pygame.Rect((0, 0), BAR_SIZE)
        self.back_color = back_color
        self.back_rect.center = position

        # Initializes progress rectangle with the same height as the background rectangle
        self.progress_rect = pygame.Rect((0, 0), (0, BAR_SIZE[1]))
        self.progress_color = progress_color
        self.progress_rect.left = self.back_rect.left
        self.progress_rect.centery = self.back_rect.centery
    
    # Toggles paused state of progress bar and ensures time spent paused does not get added to total time
    def change_pause(self, paused) -> None:
        # Stores new paused state
        self.paused = paused
        
        # If now paused, store the time when the paused start
        if paused:
            self.pause_start_epoch = time()
            
            # Change progress bar's color to reflect being paused
            self.progress_color = self.paused_color
        else:  # Otherwise, if now unpaused, add time spent paused to stored variable
            self.time_spent_paused += time() - self.pause_start_epoch

            # Change progress bar's color to reflect playing
            self.progress_color = self.playing_color

    # Resets start time to current time and calculates the new increment for each second
    def reset(self, song_length) -> None:
        # Calculate increment by dividing background rect's width / seconds of song
        self.start_epoch = time()
        self.time_spent_paused = 0
        self.increment = self.back_rect.width / song_length

    # Makes the bar's right side move to the right as the song goes on
    def increment_bar(self) -> None:
        # Increments the progress bar every second not spent paused
        seconds = time() - self.start_epoch - self.time_spent_paused
        self.progress_rect.width = self.increment * seconds

        # Resets progress bar's left side to left of background bar so only the right side moves
        self.progress_rect.left = self.back_rect.left
        self.progress_rect.centery = self.back_rect.centery

    # Renders background bar and progress bar to the screen
    def draw(self) -> None:
        # Renders background rectangle behind progress rectangle
        pygame.draw.rect(self.screen, self.back_color, self.back_rect)

        # Only increases bar if song is actively playing
        if self.increment != 0 and self.paused == False:
            self.increment_bar()
        
        # Renders progress rectangle to screen
        pygame.draw.rect(self.screen, self.progress_color, self.progress_rect)