# Used by ui_tools.py
import pygame
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from io import BytesIO
from time import time
from math import floor

# Used by main.py
import os
from platform import system
from pytubefix import Playlist
import random
from ui_tools import *
from data_handler import *
from downloader import *

# Default dimensions of touchscreen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

#
DEFAULT_TEST_URL = "https://www.youtube.com/playlist?list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa"


# Any elapsed time greater than this variable resets the current song rather than playing the previous song
RESET_TIME = 4

# 
START_BG_COLOR = (0, 0, 0)
PLAYER_BG_COLOR = '#d184a1'

# 
REG_IMG_PATH = 'assets/textures/test_button.png'
PRESSED_IMG_PATH = 'assets/textures/test_button_pressed.png'

#
BASIC_FONT_PATH = "assets/fonts/NotoSansRegular.ttf"
SONG_INFO_FONT_PATH = "assets/fonts/NotoSansRegular.ttf"
TIMER_FONT_PATH = "assets/fonts/ChivoMono.ttf"

ARTIST_FONT_SIZE = 16
ARTIST_FONT_COLOR = (255, 255, 255)
SONG_FONT_SIZE = 24
SONG_FONT_COLOR = (255, 255, 255)

#
BAR_SIZE = (200, 10)
CLICK_SAFETY = 20
BAR_BG_COLOR = (0, 0, 0)
BAR_PLAYING_COLOR = (255, 0, 0, 0)
BAR_PAUSED_COLOR = (90, 90, 90)

# Creates text objects for displaying current time and song length next to progress bar
GAP = 25
TIME_FONT_SIZE = 16
TIMER_Y_OFFSET = 1