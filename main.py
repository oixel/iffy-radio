from ui_tools import *

# Handles loading playlist and downloading non-downloaded songs
def start() -> None:
    # Only utilizes RFID reading on Raspberry Pi
    if is_windows:
        data = WINDOWS_PLAYLIST
    else:
        # Resets text back to requesting RFID card
        start_text.change_text(TAP_REQUEST_TEXT)
        render([background, start_text])
        
        # Loads data in RFID into playlist URL when card is tapped
        data = read_rfid()

    # Grabs custom background image name if one is written in data
    if DATA_SEPERATOR in data:
        split = data.split(DATA_SEPERATOR)
        url = split[0]
        bg_path = f"assets/backgrounds/{split[1]}.png"

        # Prevents non-existent backgrounds from being used
        if not os.path.isfile(bg_path) or DATA_SEPERATOR not in data:
            bg_path = DEFAULT_BG_PATH
    else:
        url = data
        bg_path = DEFAULT_BG_PATH

    # Fills out the rest of the playlist's URL
    playlist_url = f"https://www.youtube.com/playlist?list={url}"
        
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
    background.change_image(bg_path)
    song_info.change_song(queue[track_num])

    # Updates the displayed position in queue
    queue_pos_text.change_text(f"{track_num + 1} / {len(queue)}")

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
    global state, start_queue, queue, track_num, paused, looping

    # Resets all values of queue
    state = 0
    start_queue = [] 
    queue = []
    track_num = 0
    paused = False
    looping = False

    # Stops the music and closes the player
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Resets states of buttons with different variations
    pause_button.change_sprites("pause", "pause_pressed")
    shuffle_button.change_sprites("shuffle_off", "shuffle_off_pressed")
    loop_button.change_sprites("loop_off", "loop_off_pressed")
    
    # Resets background and text on screen to their initial states
    background.change_image(START_BG_PATH)
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

        shuffle_button.change_sprites("shuffle_on", "shuffle_on_pressed")
    else:  # Otherwise, unshuffle
        # Places position in queue back to currently playing song's regular position in playlist
        track_num = start_queue.index(queue[track_num])

        # Resets queue to its initial state when it was first loaded
        queue = start_queue.copy()

        shuffle_button.change_sprites("shuffle_off", "shuffle_off_pressed")
    
    # Updates displayed position to reflect the current track's new position in altered queue
    queue_pos_text.change_text(f"{track_num + 1} / {len(queue)}")

# Updates song info and loads new song into music player
def load_song() -> None:
    song_info.change_song(queue[track_num])

    # Updates position displayed in text to reflect change
    queue_pos_text.change_text(f"{track_num + 1} / {len(queue)}")

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
def skip(skip_pressed = True) -> None:
    global track_num

    # If looping is toggled on for current song, replay it if the song ended naturally (skip button wasn't pressed)
    if (not looping and not skip_pressed) or skip_pressed:
        track_num = 0 if track_num == len(queue) - 1 else track_num + 1

    load_song()

# Toggles pause on music depending on its current state
def toggle_pause() -> None:
    global paused

    if paused:
        pygame.mixer.music.unpause()
        pause_button.change_sprites("pause", "pause_pressed")
    else:
        pygame.mixer.music.pause()
        pause_button.change_sprites("play", "play_pressed")

    paused = not paused

    # Updates paused state of progress bar
    song_info.change_pause(paused)

# Toggles looping of current track depending on its current state
def toggle_looping():
    global looping

    # Stops looping current song
    if looping:
        loop_button.change_sprites("loop_off", "loop_off_pressed")
    else:
        loop_button.change_sprites("loop_on", "loop_on_pressed")

    looping = not looping

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
    looping = False

    # Basic variables for test UI
    mid_x, mid_y = screen.get_rect().center
    
    # Creates a colored background that fills the entire screen
    background = Background(screen, START_BG_PATH)

    # UI Elements in start state
    start_text = Text(screen, BASIC_FONT_PATH, 24, START_TEXT, BASIC_FONT_COLOR, (mid_x, mid_y - 15))
    start_button = Button(screen, start, (mid_x, mid_y + 35), "start", "start_pressed")
    exit_button = Button(screen, exit, (32, 32), "exit", "exit_pressed")
    start_ui = [background, start_text, start_button, exit_button]

    # UI Elements in status state
    status_text = Text(screen, BASIC_FONT_PATH, 24, "", BASIC_FONT_COLOR, (mid_x, mid_y + 35))
    
    # UI Elements in main state
    song_info = SongInfo(screen, (mid_x, mid_y - 60))
    previous_button = Button(screen, previous, (mid_x - 75, mid_y + 70), "previous", "previous_pressed")
    skip_button = Button(screen, skip, (mid_x + 75, mid_y + 70), "skip", "skip_pressed")
    pause_button = Button(screen, toggle_pause, (mid_x, mid_y + 70), "pause", "pause_pressed")
    loop_button = Button(screen, toggle_looping, (mid_x - 36, mid_y + 140), "loop_off", "loop_off_pressed")
    shuffle_button = Button(screen, shuffle, (mid_x + 36, mid_y + 140), "shuffle_off", "shuffle_off_pressed")
    back_button = Button(screen, back, (32, 32), "back", "back_pressed")
    queue_pos_text = Text(screen, BASIC_FONT_PATH, 24, "0 / 0", BASIC_FONT_COLOR, (SCREEN_WIDTH - 48, SCREEN_HEIGHT - 32))
    player_ui = [background, song_info, queue_pos_text, previous_button, skip_button, pause_button, loop_button, shuffle_button, back_button]
    
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
                skip(False)  # Passes in false since the skip button wasn't pressed

            # Renders player UI
            render(player_ui)
    
    # Closes down pygame when loop is quit
    pygame.quit()