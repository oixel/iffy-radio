import data_handler as DH
from downloader import *
from renamer import *
from pytube import Playlist
#from rfid_readerwriter import read_rfid
import pygame
import requests
import io

def main() -> None:
    # print("Please tap music card!")
    # data = read_rfid()
    # print(data)

    pygame.init()
    pygame.display.set_caption('iffy Radio')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    background = pygame.Surface((800, 480))
    background.fill(pygame.Color('#FFC0CB'))

    is_running = True

    req = requests.get("https://i.ibb.co/DDKn0JH/starcat.jpg")
    image = io.BytesIO(req.content)
    img = pygame.image.load(image).convert()
    screen.blit(background, (0, 0))
    screen.blit(img, (0, 0))

    pygame.display.flip()
    
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        

    pygame.quit()
    

if __name__ == "__main__":
    main()