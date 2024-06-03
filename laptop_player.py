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
from time import sleep

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
def download_song(url, num):
    # Downloads audio from url to queue folder
    youtube = YouTube(url)
    audio = youtube.streams.filter(only_audio=True).first()

    # Stores song in format of song_# where # is its place in queue
    audio.download("queue", "song_" + str(num) + ".mp3")


# Takes plays song in queue depending which number is given
def play_song(song_num):
    # Plays song at given number in queue
    player = vlc.MediaPlayer(f'queue/song_{song_num}.mp3')
    player.play()

    # Prevents closing as long as media being played has not reached the end
    while player.get_state() != vlc.State.Ended and player.get_state() != vlc.State.Stopped:
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
            return song_num + 1
        
        # Resets skip button when it is let go
        if not skip_button.is_active() and skip_button.is_pressed():
            skip_button.set_pressed(False)
        
        # Handles going back functionality
        if back_button.is_active() and not back_button.is_pressed():
            back_button.set_pressed(True)
            player.stop()
            return song_num - 1
        
        # Resets back button when it is let go
        if not back_button.is_active() and back_button.is_pressed():
            back_button.set_pressed(False)
    
    # Automatically moves onto next song once the current song has ended
    return song_num + 1

# Takes data stored in QR Code from main and runs the command stored on it
def play(command):
    song_num = 1

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

        # Downloads all songs in imported playlist
        num = 1
        for song_url in playlist.video_urls:
            download_song(song_url, num)
            num += 1
        
        # Runs as long as the song being played is in range of queue
        while song_num >= 1 and song_num < len(playlist.video_urls) + 1:
            # the integer returned is an altered version o
            song_num = play_song(song_num)
        
        # Debug message to show when playlist has finished playing
        print("PLAYLIST DONE!")