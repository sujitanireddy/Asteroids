import sys
import pygame
from constants import *
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():

    #Initializing pygame
    pygame.init()
    pygame.mixer.init()

    #Setting up the screen and title
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load("images/space.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Asteroids")

    #Playing music
    pygame.mixer.music.load("audio_files/game_music.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    #Player died sound
    player_died_sound = pygame.mixer.Sound("audio_files/damage.ogg")
    player_died_sound.set_volume(0.5)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Shot.containers = (shots, updatable, drawable)
    
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                pygame.mixer.music.fadeout(300)           # optional: fade out background
                ch = player_died_sound.play()             # returns a Channel
                while ch.get_busy():                      # wait until the sound finishes
                    pygame.time.delay(10)
                print("Game over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()

        #screen.fill("black")
        screen.blit(background, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
