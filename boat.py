# Simple pygame program

# Import and initialize the pygame library
import pygame
import math
import sys

pygame.init()
clock = pygame.time.Clock()
FPS = 60

# width 720, height 640
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 640

# Setting up game screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Boat game")
# Load background image
bg = pygame.image.load("bg.png").convert_alpha()
# Size of the background is set to the width and height of the screen
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_width = bg.get_width()

# Define game variables
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

facingRight = pygame.image.load('ship_RIGHT.png')
facingLeft = pygame.image.load('ship_LEFT.png')
facingUp = pygame.image.load('ship_UP.png')
facingDown = pygame.image.load('ship_DOWN.png')
facingUR = pygame.image.load('ship_UR.png')  # Image is facing up right
facingUL = pygame.image.load('ship_UL.png')  # Image is facing up left
facingDR = pygame.image.load('ship_DR.png')  # Image is facing down right
facingDL = pygame.image.load('ship_DL.png')  # Image is facing down left


# Player(boat) class
class Player:
    def __init__(self, x, y):
        self.x, self.y = int(x), int(y)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.color = (250, 120, 60)
        self.velX, self.velY = 0, 0
        self.left_pressed, self.right_pressed, self.up_pressed, self.down_pressed = False, False, False, False
        self.speed = 4
        self.current_image = facingRight  # temp

    # Draws the boat and controls the image loaded when facing movement direction
    def draw(self, screen):
        # pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(self.current_image, self.color, self.rect)

        if self.left_pressed and not (self.up_pressed or self.down_pressed):
            self.current_image = facingLeft
            screen.blit(self.current_image, (self.x, self.y))
        elif self.up_pressed and not (self.right_pressed or self.left_pressed):
            self.current_image = facingUp
            screen.blit(self.current_image, (self.x, self.y))
        elif self.right_pressed and not (self.up_pressed or self.down_pressed):
            self.current_image = facingRight
            screen.blit(self.current_image, (self.x, self.y))
        elif self.down_pressed and not (self.right_pressed or self.left_pressed):
            self.current_image = facingDown
            screen.blit(self.current_image, (self.x, self.y))
            screen.blit(self.current_image, (self.x, self.y))
        elif self.up_pressed and self.right_pressed:
            self.current_image = facingUR
            screen.blit(self.current_image, (self.x, self.y))
        elif self.up_pressed and self.left_pressed:
            self.current_image = facingUL
            screen.blit(self.current_image, (self.x, self.y))
        elif self.down_pressed and self.right_pressed:
            self.current_image = facingDR
            screen.blit(self.current_image, (self.x, self.y))
        elif self.down_pressed and self.left_pressed:
            self.current_image = facingDL
            screen.blit(self.current_image, (self.x, self.y))
        else:
            screen.blit(self.current_image, (self.x, self.y))
        pygame.display.update()

    def update(self):

        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        if self.up_pressed and self.left_pressed:
            self.velY -= (self.speed / 10)
            self.velX -= (self.speed / 10)
        if self.up_pressed and self.right_pressed:
            self.velY -= (self.speed / 10)
            self.velX = (self.speed / 10)
        if self.down_pressed and self.left_pressed:
            self.velY = (self.speed / 6)
            self.velX -= (self.speed / 6)
        if self.down_pressed and self.right_pressed:
            self.velY = (self.speed / 4)
            self.velX = (self.speed / 4)

        self.x += self.velX
        self.y += self.velY

        if self.y > 0:
            self.y -= 5
        if self.y < SCREEN_HEIGHT - 100:
            self.y += 5
        if self.x > 0:
            self.x -= 5
        if self.x < SCREEN_WIDTH - 100:
            self.x += 5

        # self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)
        pygame.draw.rect(self.current_image, self.color, self.rect)


# Player Initialization
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# Run until the user asks to quit
run = True
while run:
    clock.tick(FPS)
    # Draws the scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        pygame.display.flip()

    # Scrolls the background
    scroll -= 2

    # Resets scroll
    if abs(scroll) > bg_width:
        scroll = 0

    # If button is pressed then true
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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

    # Draws the player(boat)
    player.draw(screen)

    # Update the position of the boat
    player.update()
    pygame.display.flip()
    pygame.display.update()
