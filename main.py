import sys

import pygame

from flock import Flock
from settings import WIDTH, HEIGHT, MAX_FPS


def main():
    pygame.init()
    main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids")
    clock = pygame.time.Clock()

    # --- Flock init ---
    flock = Flock(size=100,
                  perception_radius=50,
                  r1_factor=400,
                  r2_factor=20,
                  r3_factor=8,
                  color='green')

    # --- Main Loop ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        main_screen.fill('white')

        # -- Flock ---
        flock.draw(main_screen)
        flock.update()

        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
