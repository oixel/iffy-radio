#
# This is for testing the player on my laptop compared to the actual Raspberry Pi
#

# Prevents error with importing vlc
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import vlc
from pytube import YouTube, Playlist
from pytube.innertube import _default_clients
import keyboard

class Queue:
    def __init__(self, side_length, song_urls) -> None:
        self.SIDE_LENGTH = side_length  # Refers to how many songs are on each side of current song
        self.MAX_SIZE = (side_length * 2) + 1
        self.song_index = 0
        self.song_urls = song_urls
        self.current_queue = []
        self.left = 0
        self.right = self.SIDE_LENGTH

        self.current_queue.append(download_song(self.song_urls[0], self.song_index))
    
    def get_current_song(self) -> str:
        print("Current index:", str(self.song_index))
        return self.current_queue[self.song_index]
    
    def at_start(self) -> bool:
        return self.song_index == 0
    
    def is_full(self) -> bool:
        return len(self.current_queue) == self.MAX_SIZE
    
    def is_complete(self) -> bool:
        return self.song_index == len(self.song_urls)

    def back(self) -> None:
        self.left += 1
        os.remove(f"queue/song_{self.song_index + self.SIDE_LENGTH}.mp3")
        self.current_queue.pop(0)
        self.song_index -= 1
    
    def skip(self) -> None:
        self.right += 1
        if (not self.at_start()) and self.is_full():
            os.remove(f"queue/song_{self.song_index - self.SIDE_LENGTH}.mp3")
            self.current_queue.pop()
        self.song_index += 1
        #
        # NOT WORKING PROPERLY BECAUSE SONG INDEX IS DOUBLING AS NUMBER IN SONG NAME
        #
    
    def fill_queue(self) -> None:
        for i in range(1, self.right + 1):
            self.download(self.song_index + i)
            self.right -= 1
        
        for i in range(1, self.left + 1):
            self.download(self.song_index - i)
            self.left -= 1
        
    def download(self, index) -> None:
        song = download_song(self.song_urls[index], index)
        self.current_queue.insert(index, song)
    

    
    

# Basic template for different control buttons
class ControlButton:
    # Uses gipiozero button class for basic functionality
    def __init__(self, key):
        self.key = key
        self.pressed = False
    
    # Returns whether key is currently being pressed down
    def is_active(self):
        return keyboard.is_pressed(self.key)

    # Pressed boolean prevents spam-toggling while holding down button
    def is_pressed(self):
        return self.pressed
    
    # Returns true when the key is not being pressed down
    def is_released(self):
        return not keyboard.is_pressed(self.key)

    # Sets state of pressed button's pressed boolean
    def set_pressed(self, state):
        self.pressed = state
        
# Creates buttons to handle different playback functionalities
pause_button = ControlButton('p')
skip_button = ControlButton('s')
back_button = ControlButton('b')

# Downloads song at given url
def download_song(url, num) -> str:
    # Downloads audio from url to queue folder
    youtube = YouTube(url)
    audio = youtube.streams.filter(only_audio=True).first()

    # Stores song in format of song_# where # is its place in queue
    name = "song_" + str(num) + ".mp3"

    audio.download("queue", name)

    return name


# Takes plays song in queue depending which number is given
def play_song(queue):
    # Plays song at given number in queue
    player = vlc.MediaPlayer(f'queue/{queue.get_current_song()}')
    player.play()

    # Prevents closing as long as media being played has not reached the end
    while player.get_state() != vlc.State.Ended and player.get_state() != vlc.State.Stopped:
        if not queue.is_full():
            queue.fill_queue()

        # Handles pausing functionality
        if pause_button.is_active() and not pause_button.is_pressed():
            pause_button.set_pressed(True)
            player.pause()
        
        # Resets pause button when it is let go
        if not pause_button.is_active() and pause_button.is_pressed():
            pause_button.set_pressed(False)

        # Handles skipping functionality
        if skip_button.is_active() and not skip_button.is_pressed():
            skip_button.set_pressed(True)
            player.stop()
            queue.skip()
            return
        
        # Resets skip button when it is let go
        if not skip_button.is_active() and skip_button.is_pressed():
            skip_button.set_pressed(False)
        
        # Handles going back functionality
        if back_button.is_active() and not back_button.is_pressed():
            if not queue.at_start():
                back_button.set_pressed(True)
                player.stop()
                queue.back()
                return
        
        # Resets back button when it is let go
        if not back_button.is_active() and back_button.is_pressed():
            back_button.set_pressed(False)

# Takes data stored in QR Code from main and runs the command stored on it
def play(command):
    # Used to bypass age restricted authorization
    _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

    # Returns error if no QR Code was ever provided but loop closes
    if command == None:
        print("No QR Code Provided")
        return

    properties = command.split(" :: ")
    
    # If only a single song is in QR Code, only play that one song
    if properties[0] == "song":
        download_song(properties[1], 1)
        play_song(1)

        # Debug message to show when song has finished playing
        print("SONG DONE!")
    # Otherwise download and play every song
    elif properties[0] == "playlist":
        # Creates list of songs from playlist object
        playlist = Playlist(properties[1])

        queue = Queue(1, playlist)
        print("Setting up your music... 🐈‍⬛")
        queue.fill_queue()
        print("Your music is now ready!")
        
        # Runs as long as the song being played is in range of queue
        while not queue.is_complete():
            play_song(queue)
        
        # Debug message to show when playlist has finished playing
        print("PLAYLIST DONE!")