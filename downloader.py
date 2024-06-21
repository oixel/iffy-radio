import requests
from pytube import *
from pytube.innertube import _default_clients

# Takes in image source URL and downloads it at parameterized path
def download_cover(url, song_name) -> None:
    image_data = requests.get(url).content

    # Downloads album cover art in format of SongName.jpg in album_covers folder
    path =  f'content/album_covers/{song_name}.jpg'
    open(path, "wb").write(image_data)

# Downloads song at given url
def download_song(url, song_name) -> None:
    # Used to bypass age restricted authorization
    _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

    # Downloads audio from url to queue folder
    youtube = YouTube(url)
    audio = youtube.streams.filter(only_audio=True).first()

    # Stores song in format of SongName.mp3 in songs folder
    audio.download('content/songs/', f'{song_name}.mp3')