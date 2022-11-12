import pygame


class Rubbish:
    def __init__(self, screen, x_pos, y_pos, type, scale, draggable=True, image_path=""):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.image_path = image_path
        # These will be set in: __init__ for self.image and in draw() for self.bounding_box
        self.image = None
        self.bounding_box = None

        # Load the image and store it into self.image if an image was given
        if image_path != "":
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (50, 50))

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


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([780, 640])

# Run until the user asks to quit
running = True
currently_dragging = False
obj_being_dragged = None

all_rubbish = [Rubbish(screen, 100, 100, 0, 1, image_path="bottle.png"),
               Rubbish(screen, 300, 250, 0, 1),
               Rubbish(screen, 250, 300, 0, 1)]

# Variables used for dragging rubbish
offset_x, offset_y = 0, 0

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

    # Display it to the screen
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
