import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        
        #loading player image
        self.original_image = pygame.image.load("images/player.png")
        self.original_image = pygame.transform.flip(self.original_image, True, True)
        self.original_image = pygame.transform.rotozoom(self.original_image, 0, 0.5)
        self.image = self.original_image

        self.bullet_sound = pygame.mixer.Sound("audio_files/laser.wav")
        self.bullet_sound.set_volume(0.2)
        #pygame.mixer.music.play(-1)

    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):

        #pygame.draw.polygon(screen,"white",self.triangle(), 2)
        rotated_image = pygame.transform.rotate(self.original_image, -self.rotation)
        rotated_rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_image, rotated_rect)

    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            Player.rotate(self, -dt)
        if keys[pygame.K_d]:
            Player.rotate(self, dt)
        if keys[pygame.K_w]:
            Player.move(self,dt)
        if keys[pygame.K_s]:
            Player.move(self,-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self,dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

  
    def shoot(self):

        if self.timer > 0:
            return

        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        MUZZLE_OFFSET = 20
        spawn_pos = self.position + forward * MUZZLE_OFFSET

        velocity = forward * PLAYER_SHOOT_SPEED
        shot = Shot(spawn_pos.x, spawn_pos.y, self.rotation, velocity)

        self.bullet_sound.play()

        self.timer = PLAYER_SHOOT_COOLDOWN

