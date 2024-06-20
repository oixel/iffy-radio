import data_grabber as DG
from downloader import *
from pytube import *
import taglib

TEST_PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa'

playlist = Playlist(TEST_PLAYLIST_URL)

for song_url in playlist.video_urls:
    dg = DG.DataGrabber(song_url)
    data = dg.get_data()

    print(data, "\n")
    if data["cover_src"] != None:
        spaceless_album = data["album"].replace(' ', '').replace('/', '-')
        spaceless_name = data["title"].replace(' ', '').replace('(', '').replace(')', '').replace('/', '-')

        download_cover(data["cover_src"], spaceless_album)
        download_song(song_url, spaceless_name)

        with taglib.File(f"content/songs/{spaceless_name}.mp3", save_on_exit=True) as mp3:
            mp3.tags["TITLE"] = [data["title"]]
            mp3.tags["ALBUM"] = [data["album"]]
            mp3.tags["ARTIST"] = [data["artist"]]
        
        print(data["title"], "downloaded and written!")
