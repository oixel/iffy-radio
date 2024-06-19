import data_grabber as DG
from downloader import *
from pytube import *
import webbrowser

TEST_PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa'

playlist = Playlist(TEST_PLAYLIST_URL)

for song_url in playlist.video_urls:
    dg = DG.DataGrabber(song_url)
    data = dg.get_data()
    print(data, "\n")
    if data["cover_src"] != None:
        spaceless_album = data["album"].replace(' ', '')
        spaceless_name = data["song"].replace(' ', '')
        path = f'album_art/{spaceless_name}.jpg'
        download_cover(data["cover_src"], spaceless_album)
        download_song(song_url, spaceless_name)
