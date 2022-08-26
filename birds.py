import random

import pygame

from util import magnitude, vector_add, vector_sub, scalar_division, distance
from settings import WIDTH, HEIGHT


class Boid(pygame.sprite.Sprite):

    def __init__(self, color):
        super().__init__()
        self.image = pygame.surface.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(random.randrange(WIDTH), random.randrange(HEIGHT)))

        self.velocity = [random.randrange(200), random.randrange(200)]

        self.velocity_limit = 4

    def update(self, boid_neighbourhood, rule_one, rule_two, rule_three):
        # --- Apply Rules And Update Movement Vector ---
        if boid_neighbourhood:
            if rule_one:
                vector_rule_one = self.rule_one(boid_neighbourhood)
                self.velocity = vector_add(self.velocity, vector_rule_one)
            if rule_two:
                vector_rule_two = self.rule_two(boid_neighbourhood)
                self.velocity = vector_add(self.velocity, vector_rule_two)
            if rule_three:
                vector_rule_three = self.rule_three(boid_neighbourhood)
                self.velocity = vector_add(self.velocity, vector_rule_three)

        # --- Boundary Check ---
        self.velocity = vector_add(self.velocity, self.boundary_checking())

        # --- Limiting Speed ---
        if magnitude(self.velocity) > self.velocity_limit:
            self.velocity = [(v / magnitude(self.velocity)) * self.velocity_limit for v in self.velocity]

    def move(self):
        # --- Movement ---
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

    def rule_one(self, boids) -> list[float]:
        """
        Rule 1: Boids try to fly towards the centre of mass of neighbouring boids.

        :param boids: neighbouring boids
        :return: velocity for rule one
        """
        size = len(boids)  # len(boids) - 1 if boids contains self
        # The centre of mass is the average position of neighbouring boids.
        perceived_centre_of_mass = [sum(b.rect.centerx for b in boids if b != self) / size,  # x coordinate
                                    sum(b.rect.centery for b in boids if b != self) / size]  # y coordinate
        velocity = vector_sub(perceived_centre_of_mass, list(self.rect.center))
        velocity_percentage = scalar_division(velocity, 400)  # to move 1% towards the perceived center of mass
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
                if magnitude(diff_vector) < 40:
                    # away_vector = away_vector - (boid position - self position)
                    away_vector = vector_sub(away_vector, diff_vector)
        return scalar_division(away_vector, 20)

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
        perceived_velocity = scalar_division(perceived_velocity, len(boids))  # len(boids) - 1 if self in boids
        velocity_diff = vector_sub(perceived_velocity, self.velocity)
        percentage_velocity = scalar_division(velocity_diff, 8)
        return percentage_velocity

    def boundary_checking(self):
        velocity = self.velocity
        if self.rect.centerx < 0:
            velocity[0] = 10
        elif self.rect.centerx > WIDTH:
            velocity[0] = -10

        if self.rect.centery < 0:
            velocity[1] = 10
        elif self.rect.centery > HEIGHT:
            velocity[1] = -10

        return velocity


class Flock(pygame.sprite.Group):

    def __init__(self, size, color):
        super().__init__()

        for _ in range(size):
            self.add(Boid(color))

    def update(self):
        for sprite in self.sprites():
            if isinstance(sprite, Boid):
                # Update/move all boids in the flock.
                neighbourhood = []
                for other_sprite in self.sprites():
                    if distance(list(sprite.rect.center), list(other_sprite.rect.center)) < 50:
                        if sprite != other_sprite:
                            neighbourhood.append(other_sprite)
                sprite.update(neighbourhood, 1, 1, 1)

        for sprite in self.sprites():
            if isinstance(sprite, Boid):
                sprite.move()
