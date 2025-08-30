import pygame
import random
from constants import * 
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = radius
        self.original_image = pygame.image.load("images/asteroid.png")

        self.explosion_sound = pygame.mixer.Sound("audio_files/explosion.wav")
        self.explosion_sound.set_volume(0.3)

    def draw(self, screen):
        target_size = (int(self.radius * 2), int(self.radius * 2))
        scaled_image = pygame.transform.scale(self.original_image, target_size)
        rotated_rect = scaled_image.get_rect(center=(self.position.x, self.position.y))
        screen.blit(scaled_image, rotated_rect)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        self.explosion_sound.play()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20,50)
        vector_1 = self.velocity.rotate(random_angle)
        vector_2 = self.velocity.rotate(-random_angle)
        small_asteriods_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_1 = Asteroid(self.position.x, self.position.y, small_asteriods_radius)
        asteroid_1.velocity = vector_1 * 1.2
        asteroid_2 = Asteroid(self.position.x, self.position.y, small_asteriods_radius)
        asteroid_2.velocity = vector_2 * 1.2




        
