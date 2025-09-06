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

    #score system initialization 
    score = 0.0
    SCORE_RATE = 10
    font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 20)
    font_color = (255, 255, 255)

    #game over / restart state & UI 
    game_over = False
    big_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 50)
    small_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 20)
    restart_button = pygame.Rect(0, 0, 250, 60)
    restart_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120)

    #session high score (starts showing from second run)
    session_high = None

    #helper to reset the game quickly
    def reset_game():
        nonlocal player, asteroids, shots, updatable, drawable, score, asteroid_field, game_over
        # Clear groups
        for g in (asteroids, shots, updatable, drawable):
            for s in list(g):
                s.kill()

        # Recreate containers
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

        score = 0.0
        game_over = False
        # Optionally resume music if needed
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # handle restart interactions on Game Over (kept, minus prev-run score)
            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button.collidepoint(event.pos):
                        reset_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_game()

        # only update gameplay when not game over
        if not game_over:
            updatable.update(dt)
            score += SCORE_RATE * dt

        # Collisions only when not game over
        if not game_over:
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    pygame.mixer.music.fadeout(300)
                    ch = player_died_sound.play()
                    while ch.get_busy():
                        pygame.time.delay(10)

                    #on Game Over, update session high score (max of completed runs)
                    current = int(score)
                    if session_high is None:
                        session_high = current
                    else:
                        session_high = max(session_high, current)

                    game_over = True

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()

        #screen.fill("black")
        screen.blit(background, (0, 0))

        # Draw live game objects when not game over
        for obj in drawable:
            obj.draw(screen)

        # Draw current score
        score_surface = font.render(f"{int(score)}", True, font_color)
        screen.blit(score_surface, (20, 20))

        # draw session high score during gameplay (appears from second run onward)
        if session_high is not None and not game_over:
            hs_surf = small_font.render(f"H: {session_high}", True, (200, 200, 200))
            screen.blit(hs_surf, (SCREEN_WIDTH - hs_surf.get_width() - 20, 20))

        # Game Over overlay with current score and session high
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            title = big_font.render("GAME OVER", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(title, title_rect)

            final_score_surf = font.render(f"Score: {int(score)}", True, (255, 255, 255))
            final_score_rect = final_score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
            screen.blit(final_score_surf, final_score_rect)

            #session high score (max of this session’s completed runs)
            if session_high is not None:
                prev_score_surf = small_font.render(f"High Score (session): {session_high}", True, (200, 200, 200))
                prev_score_rect = prev_score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                screen.blit(prev_score_surf, prev_score_rect)

            # Restart button
            pygame.draw.rect(screen, (255, 255, 255), restart_button, border_radius=8)
            btn_text = small_font.render("Restart (R)", True, (0, 0, 0))
            btn_rect = btn_text.get_rect(center=restart_button.center)
            screen.blit(btn_text, btn_rect)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()