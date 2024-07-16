import pygame

class Button:
    def __init__(self, position, regular_sprite, pressed_sprite):
        self.position = position
        self.regular_sprite = regular_sprite
        self.pressed_sprite = pressed_sprite
    
    def clicked(mouse_pos) -> bool:
        return 