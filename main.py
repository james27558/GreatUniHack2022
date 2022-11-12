import pygame


class Rubbish:
    def __init__(self, screen, x_pos, y_pos, type, scale, draggable=True, image_path=""):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.image_path = image_path
        self.image = None

        # Load the image and store it into self.image if an image was given
        if image_path != "":
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (50, 50))
            print(self.image.get_rect())

        self.type = type
        self.scale = scale

        self.draggable = draggable

    def draw(self):
        if self.image is not None:
            self.screen.blit(self.image, (self.x_pos, self.y_pos))
        else:
            pygame.draw.circle(self.screen, (0, 0, 255), (self.x_pos, self.y_pos), 10)


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
currently_dragging = False
obj_being_dragged = None
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Fill the background with white
    screen.fill((255, 255, 255))

    all_rubbish = [Rubbish(screen, 100, 100, 0, 1, image_path="bottle.png"),
                   Rubbish(screen, 300, 250, 0, 1),
                   Rubbish(screen, 250, 300, 0, 1)]

    # Draw all rubbish
    for rubbish in all_rubbish:
        rubbish.draw()

    # Display it to the screen
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
