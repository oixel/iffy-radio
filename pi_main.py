import pygame.freetype
import os
from pytubefix import Playlist
import random
from rfid_rw import read_rfid
from ui_tools import *
from data_handler import *
from downloader import *

# Default dimensions of touchscreen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

#
def start() -> None:
    start_text.change_text("Tap playlist card!")
    render([background, start_text])

    # 
    playlist_url = f"https://www.youtube.com/playlist?list={read_rfid()}"

    #
    start_text.change_text("Verifying playlist...")
    render([background, start_text])

    #
    try:
        playlist = Playlist(playlist_url)
        _ = playlist.video_urls[0]
    except:
        start()

    # 
    start_text.change_text("Now checking for new songs..")
    render([background, start_text])
    
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
    queue = start_queue.copy()

    # 
    if len(not_downloaded) != 0:
        download_count = 0
        start_text.change_text(f"{len(not_downloaded)} out of {len(playlist.video_urls)} songs not downloaded...")
        status_text.change_text(f"{download_count}/{len(not_downloaded)} downloaded!")
        render([background, start_text, status_text])

        for song_url in not_downloaded:
            file_name = song_url[32:]

            if download_song(song_url, "", "songs/", file_name) == False:
                status_text.change_text(f"ERROR SONG COULDN'T DOWNLOAD")
                continue
            
            dh = DataHandler(song_url)
            dh.write_data("", "songs/", file_name)

            download_count += 1
            status_text.change_text(f"{download_count}/{len(not_downloaded)} downloaded!")

            render([background, start_text, status_text])

    global state
    state = 1

    pygame.mixer.init()
    pygame.mixer.music.load(queue[track_num])
    pygame.mixer.music.play()

# Loops through all ui elements in passed-in list and renders them to screen
def render(to_render) -> None:
    for ui_item in to_render:
        ui_item.draw()
    
    pygame.display.update()

#
def back() -> None:
    global state, start_queue, queue, track_num, initial_state

    # Resets all values of queue
    state = 0
    start_queue = [] 
    queue = []
    track_num = 0

    #
    initial_state = True

    #
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    #
    background.change_color((0, 0, 0))
    start_text.change_text("Press Button to Start")
    render(start_ui)

#
def exit() -> None:
    global is_running
    is_running = False

# 
def shuffle() -> None:
    global start_queue, queue, track_num

    # If queue has not been shuffled, shuffle
    if queue == start_queue:
        random.shuffle(queue)

        # Places position in queue to wherever the currently playing song was just moved to
        track_num = queue.index(start_queue[track_num])
    else:  # Otherwise, unshuffle
        # Places position in queue back to currently playing song's regular position in playlist
        track_num = start_queue.index(queue[track_num])

        queue = start_queue.copy()

#
def load_song() -> None:
    song_info.change_song(queue[track_num])

    pygame.mixer.music.load(queue[track_num])
    pygame.mixer.music.play()

    if paused:
        pygame.mixer.music.pause()

# 
def previous() -> None:
    global track_num
    track_num = len(queue) - 1 if track_num == 0 else track_num - 1
    load_song()
    
# 
def skip() -> None:
    global track_num
    track_num = 0 if track_num == len(queue) - 1 else track_num + 1
    load_song()

# Toggles pause on music depending on its current state
def toggle_pause() -> None:
    global paused

    if paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

    paused = not paused

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
    paused = False

    # Basic variables for test UI
    mid_x, mid_y = screen.get_rect().center
    reg_img_path = 'assets/textures/test_button.png'
    pressed_img_path = 'assets/textures/test_button_pressed.png'

    #
    background = Background(screen, (0, 0, 0))

    # UI Elements in start state
    start_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 24, "Press Button to Start", (255, 255, 255), (mid_x, mid_y - 35))
    start_button = Button(screen, start, (mid_x, mid_y + 35), reg_img_path, pressed_img_path)
    exit_button = Button(screen, exit, (0, 0), reg_img_path, pressed_img_path)
    start_ui = [background, start_text, start_button, exit_button]

    # UI Elements in status state
    status_text = Text(screen, "assets/fonts/NotoSansRegular.ttf", 24, "", (255, 255, 255), (mid_x, mid_y + 35))
    
    # UI Elements in main state
    song_info = SongInfo(screen, (mid_x, mid_y - 40))
    previous_button = Button(screen, previous, (mid_x - 75, mid_y + 70), reg_img_path, pressed_img_path)
    skip_button = Button(screen, skip, (mid_x + 75, mid_y + 70), reg_img_path, pressed_img_path)
    pause_button = Button(screen, toggle_pause, (mid_x, mid_y + 130), reg_img_path, pressed_img_path)
    shuffle_button = Button(screen, shuffle, (mid_x, mid_y + 200), reg_img_path, pressed_img_path)
    back_button = Button(screen, back, (0, 0), reg_img_path, pressed_img_path)
    player_ui = [background, song_info, previous_button, skip_button, pause_button, shuffle_button, back_button]

    #
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
            # 
            background.change_color('#d184a1')

            # 
            song_info.change_song(queue[0])

            # 
            initial_state = False

        if state == 0:
            render(start_ui)
        elif state == 1:
            render(player_ui)

            # If the song is not paused and not playing anymore, then the song is over
            if not paused and not pygame.mixer.music.get_busy():
                skip()
    
    pygame.quit()