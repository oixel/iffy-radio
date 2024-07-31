from ui_tools import *

# Handles loading playlist and downloading non-downloaded songs
def start() -> None:
    # Only utilizes RFID reading on Raspberry Pi
    if is_windows:
        playlist_url = DEFAULT_TEST_URL
    else:
        # Resets text back to requesting RFID card
        start_text.change_text(TAP_REQUEST_TEXT)
        render([background, start_text])

        # Loads data in RFID into playlist URL when card is tapped
        playlist_url = f"https://www.youtube.com/playlist?list={read_rfid()}"

    # Updates text to reflect current activity
    start_text.change_text(VERIFYING_TEXT)
    render([background, start_text])

    # Checks if playlist actually exists, if not, calls function again to request another card
    try:
        playlist = Playlist(playlist_url)
        _ = playlist.video_urls[0]  # Tests if playlist actually exists by checking it has at least one song
    except:
        start()

    # Updates text to reflect current activity
    start_text.change_text(CHECKING_TEXT)
    render([background, start_text])
    
    # Creates list to track the URLs that need to be downloaded from
    not_downloaded = []

    # Loops through all downloaded songs and appends the URLs of non-downloaded songs to list
    for url in playlist.video_urls:
        file_name = url[32:]

        # Adds paths of all songs to unalterable queue
        start_queue.append(f"songs/{file_name}.mp3")

        # If song is not found in downloaded songs, append its URL to the list
        if not os.path.isfile(f"songs/{file_name}.mp3"):
            not_downloaded.append(url)
    
    # Creates a non-linked copy of the unalterable queue to be able to be altered with shuffle
    global queue
    queue = start_queue.copy()

    # Only runs this functionality if there are undownloaded songs
    if len(not_downloaded) != 0:
        # Keeps track of how many songs have been downloaded out of the missing songs  
        download_count = 0

        # Updates text to display status of downloads
        start_text.change_text(f"{len(not_downloaded)} out of {len(playlist.video_urls)} songs not downloaded...")
        status_text.change_text(f"{download_count}/{len(not_downloaded)} downloaded!")
        render([background, start_text, status_text])

        # Loops through all the missing songs
        for song_url in not_downloaded:
            # Grabs the song's unique URL ID to set it as the song's filename
            file_name = song_url[32:]

            # Renders error message if song failed to download
            if download_song(song_url, "", "songs/", file_name) == False:
                status_text.change_text(ERROR_TEXT)
                continue
            
            # Writes any found song metadata to the downloaded MP3 
            dh = DataHandler(song_url)
            dh.write_data("", "songs/", file_name)

            # Updates download status to reflect success
            download_count += 1
            status_text.change_text(f"{download_count}/{len(not_downloaded)} downloaded!")
            render([background, start_text, status_text])

    # Updates state from start menu to player
    global state
    state = 1

    # Changes rendered background color and updates the displayed metadata to be the first song in queue
    background.change_color(PLAYER_BG_COLOR)
    song_info.change_song(queue[track_num])

    # Starts first song in queue!
    pygame.mixer.init()
    pygame.mixer.music.load(queue[track_num])
    pygame.mixer.music.play()

# Loops through all ui elements in passed-in list and renders them to screen
def render(to_render) -> None:
    for ui_item in to_render:
        ui_item.draw()
    
    pygame.display.update()

# Goes back to start menu from player menu
def back() -> None:
    global state, start_queue, queue, track_num

    # Resets all values of queue
    state = 0
    start_queue = [] 
    queue = []
    track_num = 0

    # Stops the music and closes the player
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Resets background and text on screen to their initial states
    background.change_color(START_BG_COLOR)
    start_text.change_text(START_TEXT)
    render(start_ui)

# Toggles the shuffle of the rest of the queue and ensures current song is left unaltered
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

        # Resets queue to its initial state when it was first loaded
        queue = start_queue.copy()

# Updates song info and loads new song into music player
def load_song() -> None:
    song_info.change_song(queue[track_num])

    pygame.mixer.music.load(queue[track_num])
    pygame.mixer.music.play()

    if paused:
        pygame.mixer.music.pause()

# Resets song or plays previous song (or last song in queue if the queue's beginning has been reached)
def previous() -> None:
    global track_num

    # Resets song to start unless button had been pressed in the last few seconds
    if song_info.get_time() < RESET_TIME:
        track_num = len(queue) - 1 if track_num == 0 else track_num - 1
    
    load_song()
    
# Skips to next song in queue (or first song if the queue's end has been reached)
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

    # Updates paused state of progress bar
    song_info.change_pause(paused)

if __name__ == "__main__":
    # Creates a fullscreen window named "iffy radio"
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)
    
    # Uses full screen and enables RFID checker when not using Windows
    is_windows = system() == "Windows"
    if is_windows:
        screen = pygame.display.set_mode(SCREEN_SIZE)
    else:
        from rfid_rw import read_rfid

        # Sets display to full screen
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Hides cursor on start up
        pygame.mouse.set_visible(False)

    # Tracks state to render proper UI elements
    state = 0

    # Variables that are altered in functions
    start_queue = []  # Stores unshuffled queue
    queue = []  # Stores current queue (shuffled or not)
    track_num = 0
    paused = False

    # Basic variables for test UI
    mid_x, mid_y = screen.get_rect().center
    
    # Creates a colored background that fills the entire screen
    background = Background(screen, START_BG_COLOR)

    # UI Elements in start state
    start_text = Text(screen, BASIC_FONT_PATH, 24, START_TEXT, (255, 255, 255), (mid_x, mid_y - 35))
    start_button = Button(screen, start, (mid_x, mid_y + 35), REG_IMG_PATH, PRESSED_IMG_PATH)
    exit_button = Button(screen, exit, (0, 0), REG_IMG_PATH, PRESSED_IMG_PATH)
    start_ui = [background, start_text, start_button, exit_button]

    # UI Elements in status state
    status_text = Text(screen, BASIC_FONT_PATH, 24, "", (255, 255, 255), (mid_x, mid_y + 35))
    
    # UI Elements in main state
    song_info = SongInfo(screen, (mid_x, mid_y - 60))
    previous_button = Button(screen, previous, (mid_x - 75, mid_y + 70), REG_IMG_PATH, PRESSED_IMG_PATH)
    skip_button = Button(screen, skip, (mid_x + 75, mid_y + 70), REG_IMG_PATH, PRESSED_IMG_PATH)
    pause_button = Button(screen, toggle_pause, (mid_x, mid_y + 130), REG_IMG_PATH, PRESSED_IMG_PATH)
    shuffle_button = Button(screen, shuffle, (mid_x, mid_y + 200), REG_IMG_PATH, PRESSED_IMG_PATH)
    back_button = Button(screen, back, (0, 0), REG_IMG_PATH, PRESSED_IMG_PATH)
    player_ui = [background, song_info, previous_button, skip_button, pause_button, shuffle_button, back_button]

    # Ensures loop runs from start
    is_running = True
    while is_running:
        # Allows for quitting the radio by pressing the 'X' icon or tapping the 'ESC' key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

        # Renders different UI elements depending on if in start menu (0) or player menu (1)
        if state == 0:
            # Renders start menu UI
            render(start_ui)
        elif state == 1:
            # If the song is not paused and not playing anymore, then the song is over
            if not paused and not pygame.mixer.music.get_busy():
                skip()

            # Renders player UI
            render(player_ui)
    
    # Closes down pygame when loop is quit
    pygame.quit()