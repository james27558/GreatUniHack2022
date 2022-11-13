import pygame
import sys
import math
import random as rand
from pygame.locals import *
from boat import Player
from main import Rubbish, Score, Bin
from river import River

class BackButton:
    def __init__(self, screen, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen
        self.image = pygame.image.load("back.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.clicked = False
        self.bounding_box = None

    def does_mouse_overlap_button(self, mouse_x, mouse_y):
        return self.bounding_box.collidepoint(mouse_x, mouse_y)

    def draw(self):
        self.bounding_box = self.screen.blit(self.image, (self.x_pos, self.y_pos))

# Functions to run the different locations
def run_ocean():
    clock = pygame.time.Clock()
    FPS = 60
    SCREEN_WIDTH = 720
    SCREEN_HEIGHT = 640
    # Creating the player (boat) object
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    # Defining the boat variables

    # Loading the boat background image
    bg = pygame.image.load("bg.png").convert_alpha()
    # Size of the background is set to the width and height of the screen
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_width = bg.get_width()
    scroll = 0
    tiles = math.ceil(720 / bg_width) + 1

    facingRight = pygame.image.load('ship_RIGHT.png')
    facingLeft = pygame.image.load('ship_LEFT.png')
    facingUp = pygame.image.load('ship_UP.png')
    facingDown = pygame.image.load('ship_DOWN.png')
    facingUR = pygame.image.load('ship_UR.png')  # Image is facing up right
    facingUL = pygame.image.load('ship_UL.png')  # Image is facing up left
    facingDR = pygame.image.load('ship_DR.png')  # Image is facing down right
    facingDL = pygame.image.load('ship_DL.png')  # Image is facing down left

    # Generate and keep track of Rubbish
    all_rubbish = []
    for x in range(rand.randint(15, 20)):
        random_type_number = rand.randint(0, 2)

        random_type_image_path = ""
        image_scale = 0.8
        if random_type_number == 0:
            random_type_image_path = "bottle.png"
        if random_type_number == 1:
            random_type_image_path = "glass bottle.png"
            # image_scale = 0.8
        if random_type_number == 2:
            random_type_image_path = "general waste face mask.png"
            image_scale = 1

        all_rubbish.append(Rubbish(screen, rand.randint(0, SCREEN_WIDTH - 50), rand.randint(0, SCREEN_HEIGHT - 50),
                                   random_type_number,
                                   image_scale,
                                   image_path=random_type_image_path))

    # Keep track of the score
    score = Score(screen, 0, 0)

    # Add the back button
    back = BackButton(screen, screen.get_width() - 50, screen.get_height() - 50)

    running = True
    while running:
        clock.tick(FPS)
        # Draws the scrolling background
        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))

        # Scrolls the background
        scroll -= 2

        # Resets scroll
        if abs(scroll) > bg_width:
            scroll = 0

        # If button is pressed then true
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left_pressed = True
                if event.key == pygame.K_RIGHT:
                    player.right_pressed = True
                if event.key == pygame.K_UP:
                    player.up_pressed = True
                if event.key == pygame.K_DOWN:
                    player.down_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    player.right_pressed = False
                if event.key == pygame.K_UP:
                    player.up_pressed = False
                if event.key == pygame.K_DOWN:
                    player.down_pressed = False

            # If one of the mouse buttons has been pressed down, check if the user clicked the back button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If it was the left mouse button
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    # Stop the function if the back button is clicked
                    if back.does_mouse_overlap_button(mouse_x, mouse_y):
                        return

        # Draws the player(boat)
        player.draw(screen)

        for rubbish in all_rubbish:
            rubbish.draw()

        # Iterate through the rubbish and check if any collide with the boat
        rubbish_index_to_delete = -1
        for rubbish_index, rubbish in enumerate(all_rubbish):
            # Check collision with the boat
            if player.bounding_box.colliderect(rubbish.bounding_box):
                rubbish_index_to_delete = rubbish_index

                score.incrementScore()

        # If a piece of rubbish does then destroy it
        if rubbish_index_to_delete != -1:
            del all_rubbish[rubbish_index_to_delete]

        # Draw the score to the screen
        score.draw()

        # Draw the back button
        back.draw()

        # Update the position of the boat
        player.update()
        pygame.display.flip()
        pygame.display.update()


# Creating the beach background
def create_beach_bg():
    # Create the beach
    img = pygame.image.load("beach.png")
    img = pygame.transform.scale(img, (720, 640))
    screen.blit(img, (0, 0))

def run_beach():
    create_beach_bg()
    # Run until the user asks to quit
    running = True
    currently_dragging = False
    obj_being_dragged = None

    # Rubbish(screen, 100, 100, 0, 1, image_path="bottle.png")
    all_rubbish = []
    for x in range(rand.randint(5, 10)):
        random_type_number = rand.randint(0, 2)

        random_type_image_path = ""
        image_scale = 1
        if random_type_number == 0:
            random_type_image_path = "bottle.png"
        if random_type_number == 1:
            random_type_image_path = "glass bottle.png"
            image_scale = 1.5
        if random_type_number == 2:
            random_type_image_path = "general waste face mask.png"
            image_scale = 1.5

        all_rubbish.append(
            Rubbish(screen, rand.randint(35, 600), rand.randint(280, 400), random_type_number, image_scale,
                    image_path=random_type_image_path))

    all_bins = [Bin(50, 520, screen, 0, "bin.png", bin_type_image_path="bottle.png"),
                Bin((screen.get_width() // 2) - 50, 520, screen, 1, "bin.png", scale=1.25, scale_both_images=False,
                    bin_type_image_path="glass bottle.png"),
                Bin(570, 520, screen, 2, "bin.png", scale=2, scale_both_images=False,
                    bin_type_image_path="general waste " \
                                        "face " \
                                        "mask.png")]

    # Variables used for dragging rubbish
    offset_x, offset_y = 0, 0

    score = Score(screen, 0, 0)

    # Add the back button
    back = BackButton(screen, screen.get_width() - 50, screen.get_height() - 50)

    while running:
        pygame.display.set_caption("Clean the beach")
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If one of the mouse buttons has been pressed down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If it was the left mouse button
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    # Stop the function if the back button is clicked
                    if back.does_mouse_overlap_button(mouse_x, mouse_y):
                        return

                    # Check to see if the cursor is over a draggable rubbish object
                    for rubbish in all_rubbish:
                        # Check if the current rubbish is draggable and if the mouse cursor is over the current rubbish's
                        # bounding box
                        if rubbish.draggable and rubbish.get_rect().collidepoint(event.pos):
                            currently_dragging = True
                            obj_being_dragged = rubbish

                            mouse_x, mouse_y = event.pos
                            # Record the offset between the rubbish's position and the mouse
                            offset_x = rubbish.x_pos - mouse_x
                            offset_y = rubbish.y_pos - mouse_y
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                # If the left mouse button has been released then drop the rubbish being currently dragged
                if event.button == 1:
                    currently_dragging = False
                    obj_being_dragged = None

            elif event.type == pygame.MOUSEMOTION:
                # While the mouse is moving and a rubbish object is being dragged, move the rubbish object with it
                if currently_dragging:
                    # Since offset_x and offset_y are fixed values (until we drop the piece of rubbish) we can just sum
                    # the current mouse position and the offset between the mouse and rubbish position
                    mouse_x, mouse_y = event.pos
                    obj_being_dragged.x_pos = mouse_x + offset_x
                    obj_being_dragged.y_pos = mouse_y + offset_y

        # Draw the beach background
        create_beach_bg()

        # Draw all rubbish
        for rubbish in all_rubbish:
            rubbish.draw()

        # Draw all bins
        for bin in all_bins:
            bin.draw()

        # Draw the score
        score.draw()

        # Check if any rubbish is colliding with any bin, if so, destroy it and change the score
        for bin in all_bins:
            rubbish_index_to_delete = -1

            # Iterate through the rubbish and check if any collide with this bin
            for rubbish_index, rubbish in enumerate(all_rubbish):
                if bin.check_collision(rubbish.bounding_box):
                    rubbish_index_to_delete = rubbish_index

                    # Change the score according depending on whether the rubbish is in the correct bin
                    if bin.type == rubbish.type:
                        score.incrementScore()
                    else:
                        score.decrementScore()

                    break

            # If a piece of rubbish does then destroy it
            if rubbish_index_to_delete != -1:
                del all_rubbish[rubbish_index_to_delete]

        back.draw()

        # Display it to the screen
        pygame.display.flip()

def run_river():
    clock = pygame.time.Clock()
    river = River(screen)
    pygame.display.set_caption("Clean the river")
    river.create_bin()

    # Add the back button
    back = BackButton(screen, screen.get_width() - 50, screen.get_height() - 50)

    running = True
    while running:
        river.draw_background()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            # If one of the mouse buttons has been pressed down, check if the user clicked the back button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If it was the left mouse button
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    # Stop the function if the back button is clicked
                    if back.does_mouse_overlap_button(mouse_x, mouse_y):
                        return


        # Move bin if arrow keys are pressed
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            river.move(-4)
        if keys_pressed[pygame.K_RIGHT]:
            river.move(4)

        if len(river.rubbish_list) < 10:
            if rand.randint(0, 20) == 0:
                river.create_rubbish()

        river.falling_rubbish()
        river.draw_bin()
        river.score.draw()

        for bin in river.bin_list:
            rubbish_index_to_delete = -1

            # Iterate through the rubbish and check if any collide with this bin
            for rubbish_index, rubbish in enumerate(river.rubbish_list):
                rubbish = rubbish[0]

                if bin.check_collision(rubbish.bounding_box):
                    rubbish_index_to_delete = rubbish_index

                    # Change the score according depending on whether the rubbish is in the correct bin
                    if bin.type == rubbish.type:
                        river.score.incrementScore()
                    else:
                        river.score.decrementScore()

                    break

            # If a piece of rubbish does then destroy it
            if rubbish_index_to_delete != -1:
                del river.rubbish_list[rubbish_index_to_delete]

        # Draw the back button
        back.draw()

        pygame.display.flip()
        clock.tick(60)

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
        if click[0] == 1:
            run_ocean()


    # beach location
    if (mouse[0] >= coord[1][0]-15 and mouse[0] <= coord[1][0]+15)\
            and (mouse[1] >= coord[1][1]-15 and mouse[1] <= coord[1][1]+15):
        pygame.draw.circle(screen, darkRed, (coord[1][0], coord[1][1]), 15)
        screen.blit(beachText, (160, 260))
        if click[0] == 1:
            run_beach()

    # river location
    if (mouse[0] >= coord[2][0]-15 and mouse[0] <= coord[2][0]+15)\
            and (mouse[1] >= coord[2][1]-15 and mouse[1] <= coord[2][1]+15):
        pygame.draw.circle(screen, darkRed, (coord[2][0], coord[2][1]), 15)
        screen.blit(riverText, (240, 360))
        if click[0] == 1:
            run_river()

# Main program

# Initalising the screen
pygame.init()
SIZE = 720, 640
screen = pygame.display.set_mode(SIZE)

# Run the game loop
game = True
while game:
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

    screen.fill((0, 0, 0))
    create_earth()
    pygame.display.set_caption("Earth")
    locations()
    pygame.display.flip()


pygame.quit()
