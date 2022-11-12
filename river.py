import pygame
import sys
from pygame.locals import *
from main import Rubbish
import random


class River():
    def __init__(self, screen):
        self.screen = screen
        self.rubbish_list = []
        self.bin = RiverBin(screen, 320, 550, "bin.png")

        self.background = pygame.image.load("river.png")
        self.background = pygame.transform.scale(self.background, (720, 640))

    # Draw river background
    def draw_background(self):
        self.screen.blit(self.background, (0, 0))


    # Create rubbish and append to list
    def create_rubbish(self):
        self.rubbish_list.append([Rubbish(self.screen, random.randint(100, 620), random.randint(1, 10), 0, 1, image_path="bottle.png"), random.randint(1, 3)])

    # Draw falling rubbish
    def falling_rubbish(self):
        index = 0

        for rubbish, speed in self.rubbish_list:
            rubbish.y_pos += speed

            # Delete if it is pass the screen
            if rubbish.y_pos > 600:
                del self.rubbish_list[index]
                index -= 1

            index += 1
            rubbish.draw()

            # if rubbish.y_pos >= self.bin.y_pos:
            #     if rubbish.x_pos < self.bin.y_pos:

    # Draw the bin
    def draw_bin(self):
        self.bin.draw()



class RiverBin():
    def __init__(self, screen, x_pos, y_pos, image_path=""):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.image_path = image_path
        self.image = None

        # Load the image and store it into self.image if an image was given
        if image_path != "":
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (50, 50))

    def draw(self):
        if self.image is not None:
            self.screen.blit(self.image, (self.x_pos, self.y_pos))
        else:
            pygame.draw.circle(self.screen, (0, 0, 255), (self.x_pos, self.y_pos), 10)

    # Move the bin left or right
    def move(self, pos):
        self.x_pos += pos
        if self.x_pos < 100 or self.x_pos > 520:
            self.x_pos -= pos





def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 640))
    clock = pygame.time.Clock()

    river = River(screen)

    while True:
        river.draw_background()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        # Move bin if arrow keys are pressed
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            river.bin.move(-4)
        if keys_pressed[pygame.K_RIGHT]:
            river.bin.move(4)

        # Create rubbish randomly
        if random.randint(0, 50) == 0:
            river.create_rubbish()

        river.falling_rubbish()
        river.draw_bin()

        pygame.display.flip()
        clock.tick(60)

main()