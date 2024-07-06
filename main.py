import data_handler as DH
from downloader import *
from renamer import *
from pytube import Playlist
from rfid_readerwriter import read_rfid
import os

def main() -> None:
    data = read_rfid()
    print(data)

if __name__ == "__main__":
    main()