from gui_tools import *

# Default dimensions of touchscreen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

if __name__ == "__main__":
    # Creates a fullscreen window named "iffy radio"
    pygame.init()
    pygame.display.set_caption('iffy radio')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Hides cursor on start up
    # pygame.mouse.set_visible(False)

    mid_x, mid_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    test_button_1 = Button(screen, 'assets/sprites/test_button.png', (mid_x - 75, mid_y))
    test_button_2 = Button(screen, 'assets/sprites/test_button.png', (mid_x + 75, mid_y))

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

        test_button_1.draw()
        test_button_2.draw()

        pygame.display.update()
    
    pygame.quit()