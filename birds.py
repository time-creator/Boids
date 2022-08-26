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
        # TODO: One problem might be, that in pygame (0, 0) is the top left. Does this influence velocities / movement?
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
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

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
        perceived_centre_of_mass = [sum(b.rect.centerx for b in boids if b != self) / size,  # x coordinate
                                    sum(b.rect.centery for b in boids if b != self) / size]  # y coordinate
        velocity = vector_sub(perceived_centre_of_mass, list(self.rect.center))
        velocity_percentage = scalar_division(velocity, 100)  # to move 1% towards the perceived center of mass
        return velocity_percentage

    def rule_two(self, boids) -> list[float]:
        """
        Rule 2: Boids try to keep a small distance away from other objects (including other boids).

        :param boids: neighbouring boids
        :return: velocity for rule two
        """
        away_vector = [0, 0]
        for boid in boids:
            if boid != self:
                diff_vector = vector_sub(list(boid.rect.center), list(self.rect.center))
                if magnitude(diff_vector) < 20:
                    # away_vector = away_vector - (boid position - self position)
                    away_vector = vector_sub(away_vector, diff_vector)
        return away_vector

    def rule_three(self, boids) -> list[float]:
        """
        Rule 3: Boids try to match velocity with near boids.

        :param boids: neighbouring boids
        :return: velocity for rule three
        """
        perceived_velocity = [0, 0]
        for boid in boids:
            if boid != self:
                perceived_velocity = vector_add(perceived_velocity, boid.velocity)
        perceived_velocity = scalar_division(perceived_velocity, len(boids) - 1)
        velocity_diff = vector_sub(perceived_velocity, self.velocity)
        percentage_velocity = scalar_division(velocity_diff, 8)
        return percentage_velocity


class Flock(pygame.sprite.Group):

    def __init__(self, size, color):
        super().__init__()

        for _ in range(size):
            self.add(Boid(color))

    def update(self):
        for sprite in self.sprites():
            if isinstance(sprite, Boid):
                # Update/move all boids in the flock.
                sprite.update(self.sprites(), 0, 0, 1)