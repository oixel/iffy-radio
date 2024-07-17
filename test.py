# https://www.youtube.com/playlist?list=PL2fTbjKYTzKfQPvxeElX4HktVjDFLIgXs
from data_handler import DataHandler
from pytubefix import Playlist
from downloader import download_song
import taglib
import os

playlist_url = "https://www.youtube.com/playlist?list=PL2fTbjKYTzKfQPvxeElX4HktVjDFLIgXs"
playlist = Playlist(playlist_url)

for song_url in playlist.video_urls:
    path = "content/songs/TEST/"
    file_name = song_url[32:]
    dh = DataHandler(song_url)
    
    if download_song(song_url, "", path, file_name) == False:
        continue

    dh.write_data("", path, file_name)

#song1 = taglib.File("content/songs/TEST/1RKqOmSkGgM.mp3")
#print(song1.tags["IMAGE_DATA"])