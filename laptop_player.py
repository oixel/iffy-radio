#
# This is for testing the player on my laptop compared to the actual Raspberry Pi
#

import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import vlc
import keyboard
from pytube import YouTube, Playlist
from pytube.innertube import _default_clients
from time import sleep
        

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
        pause_pressed = keyboard.is_pressed("p")
        skip_pressed = keyboard.is_pressed("s")
        
        # Handles pausing functionality
        if pause_pressed:
            player.pause()

        # Handles skipping functionality
        if skip_pressed:
            player.stop()

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
        playlist = Playlist(properties[1])
        num = 1
        for song_url in playlist.video_urls:
            download_song(song_url, num)
            num += 1
        
        for i in range(1, len(playlist.video_urls) + 1):
            play_song(i)
        
        # Debug message to show when playlist has finished playing
        print("PLAYLIST DONE!")