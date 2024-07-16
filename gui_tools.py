import pygame

class Button:
    def __init__(self, screen, function, image_path, position):
        # Stores screen for reference in draw()
        self.screen = screen
        
        # Loads image to serve as button's texture
        self.image = pygame.image.load(image_path).convert_alpha()

        # Creates a rect from the loaded image
        self.rect = self.image.get_rect()

        # Ensures the button's image's center is placed at paramterized position
        x = position[0] - (self.rect.size[0] / 2)
        y = position[1] - (self.rect.size[1] / 2)
        self.position = (x, y) 

        # Positions button's rect's center at calculated position
        self.rect.center =  position

        # Assigns the function that is called when button is pressed
        self.function = function

        self.clicked = True
        
    # Draws button onto the screen and handles function calling on button press
    def draw(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        # Calls stored function when button is pressed
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.function()
        
        # Resets unpressed boolean when mouse is no longer being pressed down
        if self.clicked == True:
            if not pygame.mouse.get_pressed()[0] == 1:
                self.clicked = False
        
        self.screen.blit(self.image, self.position)