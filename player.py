import vlc
from pytube import YouTube
from time import sleep

# Test link
url = "https://www.youtube.com/watch?v=1RKqOmSkGgM"

# Downloads audio from url to queue
youtube = YouTube(url)
audio = youtube.streams.filter(only_audio=True).first()

song_count = 1
audio.download("queue", "song_" + str(song_count) + ".mp3")

# Plays first song in queue
p = vlc.MediaPlayer(f'queue/song_1.mp3')
p.play()

# Gives vlc player time to open
sleep(5)

# Prevents closing as long as vlc player is running
while p.is_playing():
    sleep(1)
