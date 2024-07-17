from gui_tools import *

# Default dimensions of touchscreen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

# Temporary function to be called when 1st test button is pressed
def test1() -> None:
    background = pygame.Surface(SCREEN_SIZE)
    background.fill(pygame.Color('#d184a1'))
    screen.blit(background, (0, 0))

    song_info.update_data("content/songs/TEST/1RKqOmSkGgM.mp3")

    pygame.mixer.music.pause()
    pygame.mixer.music.load("content/songs/TEST/1RKqOmSkGgM.mp3")
    pygame.mixer.music.play()
    

# Temporary function to be called when 2nd test button is pressed
def test2() -> None:
    background = pygame.Surface(SCREEN_SIZE)
    background.fill(pygame.Color('#44752e'))
    screen.blit(background, (0, 0))

    song_info.update_data("content/songs/TEST/BBsV0Q7kGGY.mp3")
    
    pygame.mixer.music.pause()
    pygame.mixer.music.load("content/songs/TEST/BBsV0Q7kGGY.mp3")
    pygame.mixer.music.play()

# Toggles pause on music depending on its current state
def toggle_pause() -> None:
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

if __name__ == "__main__":
    # Creates a fullscreen window named "iffy radio"
    pygame.init()
    pygame.display.set_caption('iffy radio')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Hides cursor on start up
    # pygame.mouse.set_visible(False)

    # Debugging for button class functionality
    mid_x, mid_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    reg_img_path = 'assets/sprites/test_button.png'
    pressed_img_path = 'assets/sprites/test_button_pressed.png'
    test_button_1 = Button(screen, test1, (mid_x - 75, mid_y + 70), reg_img_path, pressed_img_path)
    test_button_2 = Button(screen, test2, (mid_x + 75, mid_y + 70), reg_img_path, pressed_img_path)
    pause_button = Button(screen, toggle_pause, (mid_x, mid_y + 140), reg_img_path, pressed_img_path)

    song_info = SongInfo(screen, "content/songs/TEST/v1eypolupH0.mp3", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    
    pygame.mixer.init()
    pygame.mixer.music.load("content/songs/TEST/v1eypolupH0.mp3")
    pygame.mixer.music.play()
    
    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

        test_button_1.draw()
        test_button_2.draw()
        pause_button.draw()
        song_info.draw()

        pygame.display.update()
    
    pygame.quit()