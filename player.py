import vlc
import pytube
from time import sleep

# Downloads song at given url
def download_song(url, num):
    # Downloads audio from url to queue folder
    youtube = pytube.YouTube(url)
    audio = youtube.streams.filter(only_audio=True).first()

    # Stores song in format of song_# where # is its place in queue
    audio.download("queue", "song_" + str(num) + ".mp3")

# Takes plays song in queue depending which number is given
def play_song(song_num):
    # Plays song at given number in queue
    player = vlc.MediaPlayer(f'queue/song_{song_num}.mp3')
    player.play()

    # Gives vlc player time to open
    sleep(5)

    # Prevents closing as long as vlc player is running and quit button is not pressed
    while player.is_playing():
        continue

# Takes data stored in QR Code from main and runs the command stored on it
def play(command):
    # Returns error if no QR Code was ever provided but loop closes
    if command == None:
        print("No QR Code Provided")
        return

    properties = command.split(" :: ")
    
    # If only a single song is in QR Code, only play that one song
    if properties[0] == "song":
        download_song(properties[1], 1)
        play_song(1)
    # Otherwise download and play every song
    elif properties[0] == "playlist":
        playlist = pytube.Playlist(properties[1])
        num = 1
        for song_url in playlist.video_urls:
            download_song(song_url, num)
            num += 1
        
        for i in range(1, 4):
            play_song(i)