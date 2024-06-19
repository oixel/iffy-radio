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
        path = f'album_art/{data["song"]}.jpg'
        download_image(data["cover_src"], path)