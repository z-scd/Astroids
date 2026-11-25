import sys

import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable


    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0.0

    while True:
        log_state()
        space_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and not pygame.key.get_pressed()[pygame.K_SPACE]
            ):
                space_pressed = True
       
        updatable.update(dt)
        if space_pressed:
            player.shoot()
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for asteroid in list(asteroids):
            for shot in list(shots):
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    break

        screen.fill("black")
        for asteroid in drawable:
            asteroid.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        
        


if __name__ == "__main__":
    main()
