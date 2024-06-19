import album_grabber as AG
from pytube import *

TEST_PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa'

playlist = Playlist(TEST_PLAYLIST_URL)
num = 1
for song_url in playlist.video_urls:
    print(AG.get_album_cover(song_url), '\n')