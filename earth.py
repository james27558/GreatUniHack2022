import pygame
from pygame.locals import *

pygame.init()

SIZE = 720, 640
screen = pygame.display.set_mode(SIZE)

# Beach functions
def create_beach_bg():
    # Create the sea
    sea = Rect(0, 0, 720, 280)
    pygame.draw.rect(screen, "#2700ff", sea)
    #
    sand = Rect(0, 280, 720, 360)
    pygame.draw.rect(screen, "#ffeb38", sand)

# River functions

# Functions to run the different locations
def runBeach():
    beach = True
    while beach:
        for event in pygame.event.get():
            if event.type == QUIT:
                beach = False

        create_beach_bg()
        pygame.display.flip()

# def runRiver()
def create_earth():
    img = pygame.image.load("earth.png")
    # Scale the image to fit the screen
    img = pygame.transform.scale(img, (720, 640))
    # Add the image to the screen
    screen.blit(img, (0, 0))

def locations():
    red = (255, 0, 0)
    darkRed = (200, 0, 0)

    # Location coordinates
    coord = [[360, 320], [160, 260], [240, 360]]

    # Drawing the circle for the locations
    for i in range(0, 3):
        pygame.draw.circle(screen, red, (coord[i][0], coord[i][1]), 15)

    # Making the circle interactive when hovering
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Create the text for each location
    oceanText = pygame.image.load("ocean-text.png")
    beachText = pygame.image.load("beach.text.png")
    riverText = pygame.image.load("river-text.png")

    # Checking if the mouse if hovering over the circle

    # ocean location
    if (mouse[0] >= coord[0][0]-15 and mouse[0] <= coord[0][0]+15)\
            and (mouse[1] >= coord[0][1]-15 and mouse[1] <= coord[0][1]+15):
        pygame.draw.circle(screen, darkRed, (coord[0][0], coord[0][1]), 15)
        screen.blit(oceanText, (360, 320))

    # beach location
    if (mouse[0] >= coord[1][0]-15 and mouse[0] <= coord[1][0]+15)\
            and (mouse[1] >= coord[1][1]-15 and mouse[1] <= coord[1][1]+15):
        pygame.draw.circle(screen, darkRed, (coord[1][0], coord[1][1]), 15)
        screen.blit(beachText, (160, 260))
        if click[0] == 1:
            runBeach()

    if (mouse[0] >= coord[2][0]-15 and mouse[0] <= coord[2][0]+15)\
            and (mouse[1] >= coord[2][1]-15 and mouse[1] <= coord[2][1]+15):
        pygame.draw.circle(screen, darkRed, (coord[2][0], coord[2][1]), 15)
        screen.blit(riverText, (240, 360))
        if click[0] == 1:
            runRiver()

# Main
game = True
while game:
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

    screen.fill((0, 0, 0))
    create_earth()
    locations()
    pygame.display.flip()


pygame.quit()
