import pygame
from pygame.locals import *

SIZE = 720, 640
screen = pygame.display.set_mode(SIZE)

class Beach():
    def __init__(self, screen):
        self.screen = screen

    # Create the beach background
    def create_beach_bg(self):
        # Create the sea
        sea = Rect(0, 0, 720, 280)
        pygame.draw.rect(screen, "#2700ff", sea)
        #
        sand = Rect(0, 280, 720, 360)
        pygame.draw.rect(screen, "#ffeb38", sand)
