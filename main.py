import math
import pygame

print(pygame.__version__)


class Boid:

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 90

    def update(self):
        self.x += int(self.speed[0] * math.cos(math.radians(self.direction))
                      - self.speed[1] * math.sin(math.radians(self.direction)))
        self.y += int(self.speed[0] * math.sin(math.radians(self.direction))
                      + self.speed[1] * math.cos(math.radians(self.direction)))

        if self.x > 800:
            self.x = 0
        elif self.x < 0:
            self.x = 800

        if self.y > 500:
            self.y = 0
        elif self.y < 0:
            self.y = 500


def main():
    # Initialise the screen
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    screen.fill((255, 255, 255))
    print(screen.get_size())
    pygame.display.set_caption("Basic Pygame program")

    # Create some Boids
    birds = [Boid(400, 250, (3, 1)), Boid(400, 250, (-3, 2))]
    for bird in birds:
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

        for bird in birds:
            bird.update()
            pygame.draw.circle(screen, pygame.Color('red'), (bird.x, bird.y), 3)

        pygame.display.flip()


if __name__ == '__main__':
    main()
