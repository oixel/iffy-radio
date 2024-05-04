import vlc

url = "https://www.youtube.com/watch?v=AE005nZeF-A"
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(url)
media.get_mrl()
player.set_media(media)
player.play()