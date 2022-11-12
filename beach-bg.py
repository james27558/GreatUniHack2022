import pygame
from pygame.locals import *

pygame.init()

SIZE = 720, 640
screen = pygame.display.set_mode(SIZE)

def create_beach_bg():
    # Create the sea
    sea = Rect(0, 0, 720, 280)
    pygame.draw.rect(screen, "#2700ff", sea)
    #
    sand = Rect(0, 280, 720, 360)
    pygame.draw.rect(screen, "#ffeb38", sand)

game = True
while game:
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

    create_beach_bg()

    # Update the contents of the screen
    pygame.display.flip()

pygame.quit()
