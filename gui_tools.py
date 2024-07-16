import pygame

class Button:
    def __init__(self, screen, image_path, position):
        # Stores screen for reference in draw()
        self.screen = screen

        # Loads image to serve as button's texture
        self.image = pygame.image.load(image_path).convert_alpha()

        # Creates a rect from the loaded image
        self.rect = self.image.get_rect()

        # Ensures the center of button is placed at paramterized position
        x = position[0] - (self.rect.size[0] / 2)
        y = position[1] - (self.rect.size[1] / 2)
        self.position = (x, y) 

        # Positions button's rect's center at calculated position
        self.rect.center =  self.position
        
    # Draws button onto the screen
    def draw(self) -> None:
        self.screen.blit(self.image, self.position)

    # 
    def clicked(mouse_pos) -> bool:
        return 