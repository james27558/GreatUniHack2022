import pygame
import sys
from pygame.locals import *
from main import Rubbish
from main import Bin
from main import Score
import random

class River():
    def __init__(self, screen):
        self.screen = screen
        self.rubbish_list = []
        self.bin_list = []
        self.score = Score(screen, 0, 0)

        self.background = pygame.image.load("river.png")
        self.background = pygame.transform.scale(self.background, (720, 640))

    # Draw river background
    def draw_background(self):
        self.screen.blit(self.background, (0, 0))


    # Create rubbish and append to list
    def create_rubbish(self):
        rubbish_type = random.randint(0, 3)

        if rubbish_type == 0:
            self.rubbish_list.append([Rubbish(self.screen, random.randint(100, 620), random.randint(1, 10), 0, 1, image_path="bottle.png"), random.uniform(1,2)])
        elif rubbish_type == 1:
            self.rubbish_list.append([Rubbish(self.screen, random.randint(100, 620), random.randint(1, 10), 0, 1, image_path="can.png"), random.uniform(1,2)])
        elif rubbish_type == 2:
            self.rubbish_list.append([Rubbish(self.screen, random.randint(100, 620), random.randint(1, 10), 1, 2, image_path="foodbox.png"), random.uniform(1,2)])
        elif rubbish_type == 3:
            self.rubbish_list.append([Rubbish(self.screen, random.randint(100, 620), random.randint(1, 10), 1, 1, image_path="leaves.png"), random.uniform(1,2)])

    def create_bin(self):
        self.bin_list.append((Bin(150, 550, self.screen, 0, "bin.png", scale=0.75)))
        self.bin_list.append((Bin(225, 550, self.screen, 1, "regbin.png", scale=0.75)))


    # Draw falling rubbish
    def falling_rubbish(self):
        index = 0

        for rubbish, speed in self.rubbish_list:
            rubbish.y_pos += speed

            # Delete if it is pass the screen
            if rubbish.y_pos > 530:
                del self.rubbish_list[index]
                index -= 1

            index += 1
            rubbish.draw()

            # if rubbish.y_pos >= self.bin.y_pos:
            #     if rubbish.x_pos <

    # Draw the bin
    def draw_bin(self):
        for bin in self.bin_list:
            bin.draw()

    def move(self, pos):
        for index, bin in enumerate(self.bin_list):
            bin.x_pos += pos
            if bin.x_pos < 0 + (index) * 75 or bin.x_pos > 720 - (2 - index) * 75:
                bin.x_pos -= pos
