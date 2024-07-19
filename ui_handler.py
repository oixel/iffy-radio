import pygame.freetype
import os
from pytubefix import Playlist
import random
from rfid_readerwriter import read_rfid
from gui_tools import *
from data_handler import *
from downloader import *

# Default dimensions of touchscreen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

#
def start() -> None:
    background = pygame.Surface(SCREEN_SIZE)
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    start_text.change_text("Tap playlist card!")
    start_text.draw()
    pygame.display.update()

    playlist_url = f"https://www.youtube.com/playlist?list={read_rfid()}"

    playlist = Playlist(playlist_url)

    # 
    screen.blit(background, (0, 0))
    start_text.change_text("Now checking for new songs..")
    start_text.draw()
    pygame.display.update()
    
    # 
    not_downloaded = []

    # 
    for url in playlist.video_urls:
        file_name = url[32:]

        start_queue.append(f"songs/{file_name}.mp3")

        if not os.path.isfile(f"songs/{file_name}.mp3"):
            not_downloaded.append(url)
    
    #
    global queue
    queue = start_queue

    # 
    if len(not_downloaded) != 0:
        download_count = 0
        start_text.change_text(f"{len(not_downloaded)} out of {len(playlist.video_urls)} songs not downloaded...")
        status_text.change_text(f"{download_count}/{len(not_downloaded)} downloaded!")

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

# 
def shuffle() -> None:
    global queue
    global start_queue

    # If queue has not been shuffled, shuffle
    if queue == start_queue:
        random.shuffle(queue)
    else:  # Otherwise, unshuffle
        queue = start_queue

# 
def back() -> None:
    background = pygame.Surface(SCREEN_SIZE)
    background.fill(pygame.Color('#d184a1'))
    screen.blit(background, (0, 0))

    global track_num
    track_num = len(queue) - 1 if track_num == 0 else track_num - 1

    song_info.update_data(queue[track_num])

    pygame.mixer.music.pause()
    pygame.mixer.music.load(queue[track_num])
    pygame.mixer.music.play()
    
# 
def skip() -> None:
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
    
    # Sets display to full screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Hides cursor on start up
    pygame.mouse.set_visible(False)

    # Tracks state to render proper UI elements
    state = 0

    #
    start_queue = []  # Stores unshuffled queue
    queue = []  # Stores current queue (shuffled or not)
    track_num = 0

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
    back_button = Button(screen, back, (mid_x - 75, mid_y + 70), reg_img_path, pressed_img_path)
    skip_button = Button(screen, skip, (mid_x + 75, mid_y + 70), reg_img_path, pressed_img_path)
    pause_button = Button(screen, toggle_pause, (mid_x, mid_y + 130), reg_img_path, pressed_img_path)
    shuffle_button = Button(screen, shuffle, (mid_x, mid_y + 200), reg_img_path, pressed_img_path)
    
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
            back_button.draw()
            skip_button.draw()
            pause_button.draw()
            shuffle_button.draw()
            song_info.draw()

        pygame.display.update()
    
    pygame.quit()