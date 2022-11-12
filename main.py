import pygame


class Rubbish:
    def __init__(self, screen, x_pos, y_pos, type, scale, draggable=True, image_path=""):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.scale = scale

        self.image_path = image_path
        # These will be set in: __init__ for self.image and in draw() for self.bounding_box
        self.image = None
        self.bounding_box = None

        # Load the image and store it into self.image if an image was given
        if image_path != "":
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (35 * self.scale, 50 * self.scale))

            self.bounding_box = None

        self.type = type
        self.scale = scale

        self.circle_radius = 10
        self.draggable = draggable

    def draw(self):
        if self.image is not None:
            self.bounding_box = self.screen.blit(self.image, (self.x_pos, self.y_pos))
        else:
            pygame.draw.circle(self.screen, (0, 0, 255), (self.x_pos, self.y_pos), self.circle_radius)

    def get_rect(self):
        """
        Gets the bounding rectangle of the rubbish item, mirrors the get_rect method of pygame.Surface's get_rect()
        :return:
        """
        if self.image is not None:
            return self.bounding_box
        else:
            return pygame.Rect(self.x_pos - self.circle_radius, self.y_pos - self.circle_radius, self.circle_radius * 2,
                               self.circle_radius * 2)

class Bin:
    def __init__(self, x_pos, y_pos, screen, type, image_path, scale=1.0, bin_type_image_path=""):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.type = type
        self.scale = scale

        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (100 * self.scale, 100 * self.scale))

        self.bin_type_image_path = bin_type_image_path
        self.bin_type_image = None

        # Load the bin type image and store it if an image was given
        if self.bin_type_image_path != "":
            self.bin_type_image = pygame.image.load(self.bin_type_image_path)
            self.bin_type_image = pygame.transform.scale(self.bin_type_image, (35 * self.scale, 50 * self.scale))

        self.bounding_box = None

    def draw(self):
        self.bounding_box = self.screen.blit(self.image, (self.x_pos, self.y_pos))

        if self.bin_type_image is not None:
            center_pos = self.bounding_box.center
            bin_image_dimensions = self.bin_type_image.get_size()
            self.screen.blit(self.bin_type_image, (center_pos[0] - (bin_image_dimensions[0]/2), center_pos[0] - (
                    bin_image_dimensions[1]/2)))

    def get_rect(self):
        """
        Gets the bounding rectangle of the bin, mirrors the get_rect method of pygame.Surface's get_rect()
        :return:
        """
        if self.image is not None:
            return self.bounding_box

    def check_collision(self, bounding_box):
        if bounding_box is None:
            return False
        else:
            return self.bounding_box.colliderect(bounding_box)

class Score:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.font = pygame.font.SysFont(None, 36)

        self.score = 0

    def incrementScore(self):
        self.score += 1

    def decrementScore(self):
        self.score -= 1

    def draw(self):
        img = self.font.render("Score: {}".format(self.score), True, (0, 0, 0))
        screen.blit(img, (self.x_pos, self.y_pos))


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([780, 640])

# Run until the user asks to quit
running = True
currently_dragging = False
obj_being_dragged = None

all_rubbish = [Rubbish(screen, 100, 100, 0, 1, image_path="bottle.png"),
               Rubbish(screen, 100, 200, 1, 1, image_path="bottle.png"),
               Rubbish(screen, 300, 250, 0, 1),
               Rubbish(screen, 250, 300, 0, 1)]

all_bins = [Bin(300,300,screen, 0, "bin.png", bin_type_image_path="bottle.png")]

# Variables used for dragging rubbish
offset_x, offset_y = 0, 0

score = Score(0,0)

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If one of the mouse buttons has been pressed down
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If it was the left mouse button
            if event.button == 1:
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

    # Fill the background with white
    screen.fill((255, 255, 255))

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

    # Display it to the screen
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
