import pygame
from constants import *

def main():
    #Initializing the pygame display module.
    pygame.init()

    #Creates an object to help track time
    clock = pygame.time.Clock()
    dt = 0

    #Initializing a window for display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    #Game Loop begins
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        pygame.display.flip()

        #Declaring FPS = 60
        dt_time = clock.tick(60)
        dt = dt_time/1000

if __name__ == "__main__":
    main()
