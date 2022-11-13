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
    def __init__(self, x_pos, y_pos, screen, type, image_path, scale=1.0, scale_both_images=True,
                 bin_type_image_path=""):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.type = type
        self.scale = scale
        self.scale_both_images = scale_both_images

        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        if self.scale_both_images:
            self.image = pygame.transform.scale(self.image, (100 * self.scale, 100 * self.scale))
        else:
            self.image = pygame.transform.scale(self.image, (100, 100))

        self.bin_type_image_path = bin_type_image_path
        self.bin_type_image = None

        # Load the bin type image and store it if an image was given
        if self.bin_type_image_path != "":
            self.bin_type_image = pygame.image.load(self.bin_type_image_path)
            self.bin_type_image = pygame.transform.scale(self.bin_type_image, (35 * self.scale, 50 * self.scale))

        self.bounding_box = None

    def draw(self):
        self.bounding_box = self.screen.blit(self.image, (self.x_pos, self.y_pos))

        # If an image to indicate the type of item that should go in this bin has been given, then try and place the
        # bin type image in the center of the bin on the screen
        if self.bin_type_image is not None:
            center_pos = self.bounding_box.center
            bin_image_dimensions = self.bin_type_image.get_size()
            self.screen.blit(self.bin_type_image, (center_pos[0] - (bin_image_dimensions[0]/2), center_pos[1] - (
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
    def __init__(self, screen, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.screen = screen

        self.font = pygame.font.SysFont(None, 36)

        self.score = 0

    def incrementScore(self):
        self.score += 1

    def decrementScore(self):
        self.score -= 1

    def draw(self):
        img = self.font.render("Score: {}".format(self.score), True, (0, 0, 0))
        self.screen.blit(img, (self.x_pos, self.y_pos))



