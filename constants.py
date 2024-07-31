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

# URL that is inputted when start button is pressed on Windows OS
DEFAULT_TEST_URL = "https://www.youtube.com/playlist?list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa"

# Any elapsed time greater than this variable resets the current song rather than playing the previous song
RESET_TIME = 4

# Constants relating to colored background
START_BG_COLOR = (0, 0, 0)
PLAYER_BG_COLOR = '#d184a1'

# Paths for test button UI
REG_IMG_PATH = 'assets/textures/test_button.png'
PRESSED_IMG_PATH = 'assets/textures/test_button_pressed.png'

# Paths to different fonts in assets
BASIC_FONT_PATH = "assets/fonts/NotoSansRegular.ttf"
SONG_INFO_FONT_PATH = "assets/fonts/NotoSansRegular.ttf"
TIMER_FONT_PATH = "assets/fonts/ChivoMono.ttf"

# Variables relating to font attributes
ARTIST_FONT_SIZE = 16
ARTIST_FONT_COLOR = (255, 255, 255)
SONG_FONT_SIZE = 24
SONG_FONT_COLOR = (255, 255, 255)
TIME_FONT_SIZE = 16
TIME_FONT_COLOR = (0, 0, 0)

# Variables relating to the progress bar
BAR_SIZE = (200, 10)
CLICK_SAFETY = 20
BAR_BG_COLOR = (0, 0, 0)
BAR_PLAYING_COLOR = (255, 0, 0, 0)
BAR_PAUSED_COLOR = (90, 90, 90)

# Variables relating to the positioning of time stamps around the progress bar
GAP = 25
TIME_Y_OFFSET = 1