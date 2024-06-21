import data_grabber as DG
from downloader import *
from pytube import *
import taglib
import eyed3
from io import BytesIO
from eyed3.id3.frames import ImageFrame
from renamer import *

TEST_PLAYLIST_URL = "https://www.youtube.com/watch?v=xVsa7whnDfU&list=PLpqORVIE0FYRZ8aPel-yVdZ6zAMI6ePTL"

playlist = Playlist(TEST_PLAYLIST_URL)

for song_url in playlist.video_urls:
    dg = DG.DataGrabber(song_url)
    data = dg.get_data()
    file_name = rename(data["title"])

    # print(data, "\n")
    if data["cover_src"] != None:
        print(f"Downloading...{file_name}")

        # Download cover becomes obsolete if I just render the album cover directly from the internet
        # download_cover(data["cover_src"], data["album"])
        download_song(song_url, file_name)

        # Writes basic info into MP3's ID3 metadata
        with taglib.File(f"content/songs/{file_name}.mp3", save_on_exit=True) as mp3:
            mp3.tags["TITLE"] = [data["title"]]
            mp3.tags["ALBUM"] = [data["album"]]
            mp3.tags["ARTIST"] = [data["artist"]]
            mp3.tags["COVER_SOURCE"] = [data["cover_src"]]

        # Reads and store byte data for album cover image
        cont = requests.get(data["cover_src"]).content
        image_bytes = BytesIO(cont).read()

        # Writes image data to mp3 file and saves it if file can be read by eyed3
        eyed3_mp3 = eyed3.load(f"content/songs/{file_name}.mp3")
        if eyed3_mp3 != None:
            eyed3_mp3.tag.images.set(ImageFrame.FRONT_COVER, image_bytes, "image/jpeg")
            eyed3_mp3.tag.save(version=eyed3.id3.ID3_V2_4)
        
        # Write byte data that was embeded into another ID3 tag to read in GUI more easily
        #mp3.tags["COVER_DATA"] = image_bytes
        #print(mp3.tags)

        print(file_name, "downloaded and written!\n")

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
#
#
#
# Here is how to read image data from song:
# from PIL import Image
# stream = BytesIO(mp3.tags["COVER_DATA"])
#
# image = Image.open(stream).convert("RGBA")
# stream.close()
# image.show()
#
#
# Alternative to this is just using requests again and using mp3.tags["COVER_SOURCE"] to pull image data like i did in embedding
# Honestly I think just reading that link and using requests would be so much cleaner than storing a giant block of bytes in text