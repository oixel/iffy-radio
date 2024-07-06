import data_handler as DH
from downloader import *
from renamer import *
from pytube import Playlist
import pygame
import requests
import io
from rfid_readerwriter import read_rfid

# Draws button with given text label at set offset and with set colors
def draw_button(view, font, text='', x_offset=0, y_offset=0, button_width=80, button_height=35, label_color=(255, 255, 255), button_color = (0, 0, 0)):
    HEIGHT, WIDTH = 800, 480

    # Draw rectangle around button label
    button = pygame.Rect(WIDTH / 2 - (button_width / 2) + x_offset, HEIGHT / 2 - (button_height / 2) + y_offset,
                         button_width, button_height)
    pygame.draw.rect(view, button_color, button)

    # Draw label on top of rectangle
    label = font.render(text, True, label_color)
    label_rect = label.get_rect(center=(WIDTH / 2 + x_offset, HEIGHT / 2 + y_offset))
    view.blit(label, label_rect)

    # Return rectangle to check position
    return button

def core(screen, SCREEN_SIZE, WIDTH, HEIGHT) -> None:
    # Creates a background and fills it with pink
    background = pygame.Surface(SCREEN_SIZE)
    background.fill(pygame.Color('#FFC0CB'))
    screen.blit(background, (0, 0))
    is_pink = True
    
    text_surface = pygame.font.Font(None, 24).render("Please Tap a Music Card!", False, (0, 0, 0))
    screen.blit(text_surface, (WIDTH / 2, HEIGHT / 2))

    # Updates screen once
    pygame.display.flip()
    data = read_rfid()

    screen.blit(background, (0, 0))
    text_surface = pygame.font.Font(None, 24).render(data, False, (0, 0, 0))
    screen.blit(text_surface, (10, 10))
    button = draw_button(screen, pygame.font.Font(None, 24), 'TEST', x_offset = 160)
    back_button = draw_button(screen, pygame.font.Font(None, 24), 'BACK')
    
    # Creates image surface from URL
    req = requests.get("https://lh3.googleusercontent.com/_c4JMCiDeaC2RRfShXddOuIV_A7oCL4m1R6-YK-3TDlsYgNQTXwxV0f-TTJrsO1StMt07qW3O6XNPSNt")
    image = io.BytesIO(req.content)
    image = pygame.image.load(image).convert()
    image = pygame.transform.scale(image, (200, 200))

    # Renders newly loaded image at center of screen
    center_pos = (WIDTH / 2 - image.get_width() / 2, HEIGHT / 2 - image.get_height() / 2)

    screen.blit(image, center_pos)
    
    pygame.display.flip()

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(pygame.mouse.get_pos()):
                    if is_pink:
                        background.fill(pygame.Color('#008000'))
                    else:
                        background.fill(pygame.Color('#FFC0CB'))
                    
                    screen.blit(background, (0, 0))
                    screen.blit(image, center_pos)
                    screen.blit(text_surface, (10, 10))
                    button = draw_button(screen, pygame.font.Font(None, 24), 'TEST', x_offset = 160)
                    back_button = draw_button(screen, pygame.font.Font(None, 24), 'BACK')
                    pygame.display.flip()

                    is_pink = not is_pink
                elif back_button.collidepoint(pygame.mouse.get_pos()):
                    background = pygame.Surface(SCREEN_SIZE)
                    background.fill(pygame.Color('#FFC0CB'))
                    return True

def main() -> None:
    # print("Please tap music card!")
    # data = read_rfid()
    # print(data)

    SCREEN_SIZE = WIDTH, HEIGHT = 800, 480

    # Creates a fullscreen window named "iffy radio"
    pygame.init()
    pygame.display.set_caption('iffy radio')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Hides cursor on start up
    pygame.mouse.set_visible(False)

    while True:
        desire = core(screen, SCREEN_SIZE, WIDTH, HEIGHT)
        if desire == False:
            break

    pygame.quit()
    

if __name__ == "__main__":
    main()