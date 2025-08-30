import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, angle, velocity):
        super().__init__(x, y, SHOT_RADIUS)

        self.original_image = pygame.image.load("images/laser.png").convert_alpha()
        self.original_image = pygame.transform.rotozoom(self.original_image, 0, 0.5)

        self.angle = angle        
        self.velocity = velocity

        self.heading_offset = 0   

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -(self.angle) + self.heading_offset)
        rotated_rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_image, rotated_rect)

    def update(self, dt):
        self.position += self.velocity * dt