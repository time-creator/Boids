import pygame
import random
from boid import Boid


def main():
    # Initialise the screen
    pygame.init()
    screen = pygame.display.set_mode((1200, 750))
    screen.fill((255, 255, 255))
    print(screen.get_size())
    pygame.display.set_caption("Basic Pygame program")

    # Create some Boids
    flock = [Boid(random.randint(50, 1150), random.randint(50, 700), [3, 0]) for i in range(10)]
    for bird in flock:
        pygame.draw.circle(screen, pygame.Color('red'), (bird.x, bird.y), 3)

    pygame.display.flip()

    # Event (Main) loop
    while 1:
        pygame.time.delay(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # This line resets the screen after every step; delete to show trails
        screen.fill((255, 255, 255))

        for bird in flock:
            # equals "show"
            pygame.draw.circle(screen, pygame.Color('red'), (bird.x, bird.y), 3)
            bird.update()

        pygame.display.flip()


if __name__ == '__main__':
    main()
