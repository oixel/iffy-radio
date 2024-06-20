import data_grabber as DG
from downloader import *
from pytube import *
import taglib
import eyed3
from io import BytesIO
from eyed3.id3.frames import ImageFrame

TEST_PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa'

playlist = Playlist(TEST_PLAYLIST_URL)

# Shows that MP3 properly stores cover source!
# mp3 = taglib.File(f"content/songs/Slug.mp3", save_on_exit=True)
# print(mp3.tags["COVER"])

for song_url in playlist.video_urls:
    dg = DG.DataGrabber(song_url)
    data = dg.get_data()

    # print(data, "\n")
    if data["cover_src"] != None:
        spaceless_album = data["album"].replace(' ', '').replace('/', '-')
        spaceless_name = data["title"].replace(' ', '').replace('(', '').replace(')', '').replace('/', '-')

        # Download cover becomes obsolete if I just render the album cover directly from the internet
        #download_cover(data["cover_src"], spaceless_album)
        download_song(song_url, spaceless_name)

        with taglib.File(f"content/songs/{spaceless_name}.mp3", save_on_exit=True) as mp3:
            mp3.tags["TITLE"] = [data["title"]]
            mp3.tags["ALBUM"] = [data["album"]]
            mp3.tags["ARTIST"] = [data["artist"]]
            mp3.tags["COVER_SOURCE"] = [data["cover_src"]]
        

        # Reads and store byte data for album cover image
        cont = requests.get(data["cover_src"]).content
        image_bytes = BytesIO(cont).read()

        # Writes image data to mp3 file and saves it
        eyed3_mp3 = eyed3.load(f"content/songs/{spaceless_name}.mp3")
        eyed3_mp3.tag.images.set(ImageFrame.FRONT_COVER, image_bytes, 'image/jpeg')
        eyed3_mp3.tag.save(version=eyed3.id3.ID3_V2_4)

        print(data["title"], "downloaded and written!")

# Possible Reference for embedding album art:
# https://stackoverflow.com/questions/50437358/c-sharp-taglib-set-album-cover-for-mp3

#
#
# Potential alternative:
#
# Save url to image in ID3 data,
# then follow this to convert url to surface on pygame player
# https://stackoverflow.com/questions/57023015/convert-image-from-request-to-pygame-surface
#
# Yeah, just do that. Instead of downloading each album cover, just store the source of the cover onto it