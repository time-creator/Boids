import random

import pygame

from util import distance, magnitude, vector_add, vector_sub, scalar_division


class Boid(pygame.sprite.Sprite):

    def __init__(self, color):
        super().__init__()
        self.image = pygame.surface.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(random.randrange(1280), random.randrange(720)))

        self.velocity = [random.randrange(-200, 201), random.randrange(-200, 201)]

    def update(self, boid_neighbourhood, rule_one, rule_two, rule_three):
        # -- Apply Rules ---
        vector_rule_one = self.rule_one(boid_neighbourhood)
        vector_rule_two = self.rule_two(boid_neighbourhood)
        vector_rule_three = self.rule_three(boid_neighbourhood)

        # --- Update Movement Vector ---
        if rule_one:
            self.velocity = vector_add(self.velocity, vector_rule_one)
        if rule_two:
            self.velocity = vector_add(self.velocity, vector_rule_two)
        if rule_three:
            self.velocity = vector_add(self.velocity, vector_rule_three)

        # --- Limiting Speed ---
        if magnitude(self.velocity) > 2:
            self.velocity = [(v / magnitude(self.velocity)) * 2 for v in self.velocity]

        # --- Movement ---
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # --- Boundary Overflow ---
        if self.rect.x > 1280:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = 1280

        if self.rect.y > 720:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = 720

    def rule_one(self, boids) -> list[float]:
        """
        Rule 1: Boids try to fly towards the centre of mass of neighbouring boids.

        :param boids: neighbouring boids
        :return: velocity for rule one
        """
        size = len(boids)
        # The centre of mass is the average position of neighbouring boids.
        perceived_centre_of_mass = [sum(b.rect.x for b in boids if b != self) / size,  # x coordinate
                                    sum(b.rect.y for b in boids if b != self) / size]  # y coordinate
        velocity = vector_sub(perceived_centre_of_mass, list(self.rect.center))
        velocity_percentage = scalar_division(velocity, 100)  # to move 1% towards the perceived center of mass
        return velocity_percentage

    def rule_two(self, boids) -> list[float]:
        away_vector = [0, 0]
        for boid in boids:
            if 0 < distance([self.rect.x, self.rect.y], [boid.rect.x, boid.rect.y]) < 20:
                away_vector[0] -= self.rect.x - boid.rect.x
                away_vector[1] -= self.rect.y - boid.rect.y
        return away_vector

    def rule_three(self, boids) -> list[float]:
        size = len(boids)
        average_neighbour_vector = [0, 0]
        for boid in boids:
            average_neighbour_vector = [sum(x) for x in zip(average_neighbour_vector, boid.velocity)]
        average_update_x = (self.velocity[0] - (average_neighbour_vector[0] / size)) / 8
        average_update_y = (self.velocity[1] - (average_neighbour_vector[1] / size)) / 8
        return [average_update_x, average_update_y]


class Flock(pygame.sprite.Group):

    def __init__(self, size, color):
        super().__init__()

        for _ in range(size):
            self.add(Boid(color))

    def update(self):
        for sprite in self.sprites():
            if isinstance(sprite, Boid):
                # Update/move all boids in the flock.
                sprite.update(self.sprites(), 1, 0, 0)
