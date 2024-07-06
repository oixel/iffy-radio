import data_handler as DH
from downloader import *
from renamer import *
from pytube import Playlist
#from rfid_readerwriter import read_rfid
import pygame
import requests
import io

def main() -> None:
    SCREEN_SIZE = WIDTH, HEIGHT = 800, 480
    # print("Please tap music card!")
    # data = read_rfid()
    # print(data)

    # Creates a fullscreen window named "iffy radio"
    pygame.init()
    pygame.display.set_caption('iffy radio')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Creates a background and fills it with pink
    background = pygame.Surface(SCREEN_SIZE)
    background.fill(pygame.Color('#FFC0CB'))
    screen.blit(background, (0, 0))

    # Creates image surface from URL
    req = requests.get("https://i.ibb.co/DDKn0JH/starcat.jpg")
    image = io.BytesIO(req.content)
    image = pygame.image.load(image).convert()
    image = pygame.transform.scale(image, (200, 200))

    # Renders newly loaded image at center of screen
    center_pos = (WIDTH / 2 - image.get_width() / 2, HEIGHT / 2 - image.get_height() / 2)
    screen.blit(image, center_pos)

    # Updates screen once
    pygame.display.flip()
    
    is_running = True
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