import pygame.freetype
import os
from pytubefix import Playlist
from gui_tools import *
from data_handler import *
from downloader import *

# Default dimensions of touchscreen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

#
def start() -> None:
    playlist_url = "https://www.youtube.com/playlist?list=PL2fTbjKYTzKfQPvxeElX4HktVjDFLIgXs"
    # playlist_url = "https://www.youtube.com/playlist?list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa"
    playlist = Playlist(playlist_url)

    not_downloaded = []

    for url in playlist.video_urls:
        file_name = url[32:]

        queue.append(f"songs/{file_name}.mp3")

        if not os.path.isfile(f"songs/{file_name}.mp3"):
            not_downloaded.append(url)
    
    download_count = 0
    start_text.change_text(f"{len(not_downloaded)} out of {len(playlist.video_urls)} songs not downloaded...")
    status_text.change_text(f"{download_count}/{len(not_downloaded)} downloaded!")

    background = pygame.Surface(SCREEN_SIZE)
    background.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    start_text.draw()
    status_text.draw()
    pygame.display.update()

    for song_url in not_downloaded:
        file_name = song_url[32:]

        if download_song(song_url, "", "songs/", file_name) == False:
            status_text.change_text(f"ERROR SONG COULDN'T DOWNLOAD")
            continue
        
        dh = DataHandler(song_url)
        dh.write_data("", "songs/", file_name)

        download_count += 1
        status_text.change_text(f"{download_count}/{len(not_downloaded)} downloaded!")

        screen.blit(background, (0, 0))
        start_text.draw()
        status_text.draw()
        pygame.display.update()

    global state
    state = 1

    pygame.mixer.init()
    pygame.mixer.music.load(queue[track_num])
    pygame.mixer.music.play()

# Temporary function to be called when 1st test button is pressed
def test1() -> None:
    background = pygame.Surface(SCREEN_SIZE)
    background.fill(pygame.Color('#d184a1'))
    screen.blit(background, (0, 0))

    global track_num
    track_num = len(queue) - 1 if track_num == 0 else track_num - 1

    song_info.update_data(queue[track_num])

    pygame.mixer.music.pause()
    pygame.mixer.music.load(queue[track_num])
    pygame.mixer.music.play()
    

# Temporary function to be called when 2nd test button is pressed
def test2() -> None:
    background = pygame.Surface(SCREEN_SIZE)
    background.fill(pygame.Color('#d184a1'))
    screen.blit(background, (0, 0))

    global track_num
    track_num = 0 if track_num == len(queue) - 1 else track_num + 1

    song_info.update_data(queue[track_num])
    
    pygame.mixer.music.pause()
    pygame.mixer.music.load(queue[track_num])
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

    # Tracks state to render proper UI elements
    state = 0

    #
    queue = []
    track_num = 0

    # Hides cursor on start up
    # pygame.mouse.set_visible(False)

    # Basic variables for test UI
    mid_x, mid_y = screen.get_rect().center
    reg_img_path = 'assets/textures/test_button.png'
    pressed_img_path = 'assets/textures/test_button_pressed.png'

    # UI Elements in start state
    start_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 24, "Press Button to Start", (255, 255, 255), (mid_x, mid_y - 35))
    start_button = Button(screen, start, (mid_x, mid_y + 35), reg_img_path, pressed_img_path)

    # UI Elements in status state
    status_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 24, "", (255, 255, 255), (mid_x, mid_y + 35))
    
    # UI Elements in main state
    test_button_1 = Button(screen, test1, (mid_x - 75, mid_y + 70), reg_img_path, pressed_img_path)
    test_button_2 = Button(screen, test2, (mid_x + 75, mid_y + 70), reg_img_path, pressed_img_path)
    pause_button = Button(screen, toggle_pause, (mid_x, mid_y + 130), reg_img_path, pressed_img_path)
    
    initial_state = True

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

        if state == 1 and initial_state:
            background = pygame.Surface(SCREEN_SIZE)
            background.fill(pygame.Color('#d184a1'))
            screen.blit(background, (0, 0))
            song_info = SongInfo(screen, queue[0], (mid_x, mid_y - 40))
            initial_state = False

        if state == 0:
            start_text.draw()
            start_button.draw()
        elif state == 1:
            test_button_1.draw()
            test_button_2.draw()
            pause_button.draw()
            song_info.draw()

        pygame.display.update()
    
    pygame.quit()