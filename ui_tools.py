from constants import *

# Handles the custom image backgrounds
class Background:
    # Creates an image as a surface and stores it for blitting in draw function
    def __init__(self, screen, path, position = (0, 0)) -> None:
        self.screen = screen
        self.position = position

        self.surface = pygame.image.load(path).convert()

    # Changes the image that is used as surface to the new image at path
    def change_image(self, path) -> None:
        self.surface = pygame.image.load(path).convert()

    # Renders image background onto screen
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
    def __init__(self, screen, function, position, sprite_name, pressed_sprite_name):
        # Stores screen for reference in draw()
        self.screen = screen
        
        # Sets button's sprites
        self.change_sprites(sprite_name, pressed_sprite_name)

        # Creates a rect from the loaded image
        self.rect = self.image.get_rect()

        # Positions button's rect's center at calculated position
        self.rect.center =  position

        # Assigns the function that is called when button is pressed
        self.function = function

        # Clicked is only set true if the button is clicked on the first frame of the mouse button being pressed
        self.clicked = False
        self.first_click_occurred = False      

    # Changes regular and pressed sprites to what is passed in parameters
    def change_sprites(self, sprite_name, pressed_sprite_name=None):
        # Loads unpressed variant of button's image
        self.regular_image = pygame.image.load(f"assets/textures/{sprite_name}.png").convert_alpha()
        
        # Loads pressed variant of button's image
        self.pressed_image = pygame.image.load(f"assets/textures/{pressed_sprite_name}.png").convert_alpha()

        # Sets button's current image to its unpressed variant
        self.image = self.regular_image

    # Draws button onto the screen and handles function calling on button press
    def draw(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        # Ensures that button only gets clicked when it was clicked directly
        if pygame.mouse.get_pressed()[0] == 1 and not self.first_click_occurred:
            # Makes it so this check is only called on the first frame mouse being pressed down
            self.first_click_occurred = True

            # If button was clicked on the first frame of mouse button being pressed, then it was actually clicked
            if self.rect.collidepoint(mouse_pos):
                self.clicked = True
                
        # Calls function and resets unpressed boolean when mouse is no longer being pressed down and 
        if self.clicked == True:
            # Sets button's image to its pressed variant (if it exists)
            if self.pressed_image != None and self.image != self.pressed_image:
                self.image = self.pressed_image
        
            if not pygame.mouse.get_pressed()[0] == 1:
                # Calls this button's stored function if mouse is still over the button on release
                if self.rect.collidepoint(mouse_pos):
                    self.function()

                # Resets button's click state to allow it to be clicked again
                self.clicked = False

                # Resets button's image to its unpressed variant
                self.image = self.regular_image
        
        # Called when mouse was released: resets state of first click occurring
        if not pygame.mouse.get_pressed()[0] == 1 and self.first_click_occurred:
            self.first_click_occurred = False

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
        self.artist_text = Text(screen, SONG_INFO_FONT_PATH, ARTIST_FONT_SIZE, self.artist, ARTIST_FONT_COLOR, artist_text_pos)

        # Intiailizes text stating song's name
        song_text_pos = (position[0], position[1] - 100)
        self.song_text = Text(screen, SONG_INFO_FONT_PATH, SONG_FONT_SIZE, self.song, SONG_FONT_COLOR, song_text_pos)

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

    # Returns the elapsed time stored in the progress bar
    def get_time(self) -> float:
        return self.progress_bar.elapsed_time

    # Renders song information onto screen
    def draw(self) -> None:
        self.screen.blit(self.cover_image, self.rect)
        self.artist_text.draw()
        self.song_text.draw()
        self.progress_bar.draw()

# Handles progress bar rendering, scrubbing functionality, and tracking elapsed time
class ProgressBar:
    def __init__(self, screen, position) -> None:
        # Stores basic variables depending on parameters
        self.screen = screen
        self.position = position

        # Sets initial values for variables used in incrementation and scrubbing
        self.increment = 0
        self.paused = False
        self.first_click_occurred = False
        self.scrubbing = False  # Only gets set to true if it is clicked on first frame of mouse being pressed down

        # Stores the width that occurs from any alterations of the progress (pause or scrubbing)
        # In order to increment from it rather than the progress bar's start width of 0
        self.stored_width = 0  

        # Variables that keep track of the time passed
        self.stored_time = 0  # Stores the time of last alteration (pause or scrub)
        self.progressed_time = 0  # Stores the time that has passed since last alteration
        self.elapsed_time = 0  # Stores sum of both

        # Creates background rectangle at center of screen, under cover art
        self.back_rect = pygame.Rect((0, 0), BAR_SIZE)
        self.back_rect.center = position

        # Creates invisible rectangle that makes clicking progress bar more comfortable on the small touch screen
        safety_size = (BAR_SIZE[0] + CLICK_SAFETY, BAR_SIZE[1] + CLICK_SAFETY)
        self.click_rect = pygame.Rect((0, 0), safety_size)
        self.click_rect.center = position

        # Initializes progress rectangle with the same height as the background rectangle
        self.progress_rect = pygame.Rect((0, 0), (0, BAR_SIZE[1]))
        self.progress_color = BAR_PLAYING_COLOR
        self.progress_rect.left = self.back_rect.left
        self.progress_rect.centery = self.back_rect.centery

        # Elapsed time text is the text on the left of the bar that shows how much time has passed since the start
        et_pos = (position[0] - (BAR_SIZE[0] / 2) - GAP, position[1] - TIME_Y_OFFSET)
        self.elapsed_time_text = Text(screen, TIMER_FONT_PATH, TIME_FONT_SIZE, "0:00", TIME_FONT_COLOR, et_pos)

        # Song length text is the text on the right of the bar that shows the max length of the song
        sl_pos = (position[0] + (BAR_SIZE[0] / 2) + GAP, position[1] - TIME_Y_OFFSET)
        self.song_length_text = Text(screen, TIMER_FONT_PATH, TIME_FONT_SIZE, "0:00", TIME_FONT_COLOR, sl_pos)

    # Resetting the epoch ensures all incrementations occur on top of any alterations (pausing or scrubbing)
    # Basically, ensures time is synced from the point after a pause or after scrubbing through the song
    def reset_epoch(self) -> None:
        self.epoch = time()
        self.stored_width = self.progress_rect.width

    # Since increment is calculated by diving the max width by the length of the song,
    # Dividing the current width essentially returns the current elapsed time.
    def calculate_time(self) -> float:
        return self.progress_rect.width / self.increment

    # Toggles paused state of progress bar and ensures time spent paused does not get added to total time
    def change_pause(self, paused) -> None:
        # Stores new paused state
        self.paused = paused
        
        # If now paused, change progress bar's color to reflect it
        if paused:
            self.stored_time += self.progressed_time
            self.progressed_time = 0
            self.progress_color = BAR_PAUSED_COLOR
        else:  # Otherwise, if just unpaused
            # Reset epoch and update stored width
            self.reset_epoch()

            # Change progress bar's color to reflect playing
            self.progress_color = BAR_PLAYING_COLOR

    # Resets start time to current time and calculates the new increment for each second
    def reset(self, song_length) -> None:
        # Calculate increment by dividing background rect's width / seconds of song
        self.epoch = time()
        self.increment = self.back_rect.width / song_length
        
        # Reset progress rect's width since a new song is playing from 0
        self.progress_rect.width = 0

        # Reset stored width, since new song has not been altered in any way
        self.stored_width = 0

        # Resets the variables storing time since a new song starts at 0
        self.stored_time = 0
        self.progressed_time = 0

        # Changes song length text to display the length of new song
        song_length_str = self.get_time_string(song_length)
        self.song_length_text.change_text(song_length_str)

    # Makes the bar's right side move to the right as the song goes on
    def increment_bar(self) -> None:
        # Updates progressed time to reflect how much time has passed since last stored time position
        self.progressed_time = time() - self.epoch

        # Increments the progress bar based on how much time has passed in the song
        self.progress_rect.width = self.elapsed_time * self.increment

        # Resets progress bar's left side to left of background bar so only the right side moves
        self.progress_rect.left = self.back_rect.left
        self.progress_rect.centery = self.back_rect.centery

    # Handles all functionality related to clicking / dragging through song
    def handle_scrubbing(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        # Ensures that progress bar only gets altered when it was clicked directly
        if pygame.mouse.get_pressed()[0] == 1 and not self.first_click_occurred:
            # Makes it so this check is only called on the first frame of mouse being pressed down
            self.first_click_occurred = True

            # If progress bar was clicked on the first frame that mouse was pressed down, then it is clicked
            if self.click_rect.collidepoint(mouse_pos):
                self.scrubbing = True
                self.progressed_time = 0
        
        # Only called if progress bar is clicked initially
        if self.scrubbing:
            # Updates progress bar's width to match mouse's position
            width = mouse_pos[0] - self.back_rect.bottomleft[0]

            # Stores maximum possible width as that of the background rectangle
            MAX_WIDTH = self.back_rect.width
            
            # Clamps width between 0 and the dimensions of the background rectangles
            if width < 0:
                width = 0
            elif width > MAX_WIDTH:
                width = MAX_WIDTH
            
            # Updates progress rectangles width to match mouse position (in range of clamp)
            self.progress_rect.width = width

            # Ensures that left side of progress bar lines up to that of the background
            self.progress_rect.left = self.back_rect.left
            self.progress_rect.centery = self.back_rect.centery

            # Updates the elapsed time text as the progress bar is scrubbed
            self.stored_time = self.calculate_time()

            # Updates song position only when mouse is released
            if not pygame.mouse.get_pressed()[0] == 1:
                # Reset epoch and update stored width
                self.reset_epoch()

                # Sets position in the song to the last scrubbed position
                pygame.mixer.music.set_pos(self.stored_time)

                # Resets states back to normal
                self.scrubbing = False
        
        # Called when mouse was released: Resets state of first click occurring
        if not pygame.mouse.get_pressed()[0] == 1 and self.first_click_occurred:
            self.first_click_occurred = False

    # Converts passed in time (representing seconds) into a string properly formatted to 0:00
    def get_time_string(self, time) -> None:
        # Calculates minutes and seconds of time passed
        minutes = str(floor(time // 60))
        seconds = floor(time % 60)

        # Adds a zero to front of seconds if it is not double digits
        seconds = f"0{seconds}" if seconds < 10 else str(seconds)

        # Returns properly formatted string
        return f"{minutes}:{seconds}"
    
    # Updates total elapsed time and only changes text when progress has been made in the song
    def update_elapsed_time(self) -> None:
        # Creates time text from current position in the song
        self.elapsed_time = self.stored_time + self.progressed_time
        time_text = self.get_time_string(self.elapsed_time)

        # Only changes time text if it has made progress since last frame
        if time_text != self.elapsed_time_text.text:
            self.elapsed_time_text.change_text(time_text)
        
    # Applies alpha values to hidden click box that provides extra space to click the progress bar
    def draw_click_box(self, alpha = 0):
        click_surface = pygame.Surface(pygame.Rect(self.click_rect).size, pygame.SRCALPHA)
        click_surface.set_alpha(alpha)
        pygame.draw.rect(click_surface, (0, 255, 0), click_surface.get_rect())
        self.screen.blit(click_surface, self.click_rect)

    # Renders background bar and progress bar to the screen
    def draw(self) -> None:
        # Updates the elapsed_time_text to reflect the position of time in the song
        self.update_elapsed_time()

        # Only increases bar if song is actively playing
        if self.increment != 0 and not self.paused and not self.scrubbing:
            self.increment_bar()
            
        # Renders background rectangle behind progress rectangle
        pygame.draw.rect(self.screen, BAR_BG_COLOR, self.back_rect)
        
        # Renders invisible rectangle around rectangle around progress bar to make collision space more comfortable for touchscreen
        self.draw_click_box()  # Pass 255 as parameter to see invisible box

        # Renders progress rectangle to screen
        pygame.draw.rect(self.screen, self.progress_color, self.progress_rect)

        # Renders the text displaying current time and song length next to progress bar
        self.elapsed_time_text.draw()
        self.song_length_text.draw()

        # Handles functionality for scrubbing through song by clicking progress bar
        self.handle_scrubbing()