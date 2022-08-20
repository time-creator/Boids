import pygame
import random
from boid import Boid


WIDTH = 1000
HEIGHT = 600
FPS_CLOCK = pygame.time.Clock()
FPS = 30


def main():
    # Initialise the screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Flocking Simulation")

    # Create some Boids
    flock = [Boid(
        random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10),
        [random.randint(-5, 5), random.randint(-5, 5)]
    ) for _ in range(100)]

    # Create one "ill" bird
    flock[-1].color = 'green'

    for bird in flock:
        pygame.draw.circle(screen, pygame.Color(bird.color), (bird.x, bird.y), 3)

    # Event (Main) loop
    while True:
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
            pygame.draw.circle(screen, pygame.Color(bird.color), (bird.x, bird.y), 3)

            # "Ill"; if-statement needs readability update
            if any(bird.x - 10 < b.x < bird.x + 10 and bird.y - 10 < b.y < bird.y + 10 and b.color == 'green'
                   for b in flock if b != bird):
                if random.randint(1, 10) == 10:
                    bird.color = 'green'

            bird.update()

            if bird.ill_since > 500:
                flock.remove(bird)

            if bird.x < 0:
                bird.x = WIDTH
            elif bird.x > WIDTH:
                bird.x = 0
            if bird.y < 0:
                bird.y = HEIGHT
            elif bird.y > HEIGHT:
                bird.y = 0

        pygame.display.update()

        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
