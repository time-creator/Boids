import pygame
import random
from boid import Boid


WIDTH = 600
HEIGHT = 600
FPSCLOCK = pygame.time.Clock()
FPS = 30


def main():
    # Initialise the screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    print(screen.get_size())
    pygame.display.set_caption("Basic Pygame program")

    # Create some Boids
    flock = [Boid(
        random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10),
        [random.randint(-5, 5), random.randint(-5, 5)]
    ) for i in range(20)]
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
            if bird.x < 0:
                bird.x = WIDTH
            elif bird.x > WIDTH:
                bird.x = 0
            if bird.y < 0:
                bird.y = HEIGHT
            elif bird.y > HEIGHT:
                bird.y = 0

        pygame.display.flip()

        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
