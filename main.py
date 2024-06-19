import data_grabber as DG
from pytube import *
import webbrowser

TEST_PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa'

playlist = Playlist(TEST_PLAYLIST_URL)

for song_url in playlist.video_urls:
    dg = DG.DataGrabber(song_url)
    print(dg.get_data())

#TEST_SONG = YouTube()