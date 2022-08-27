import random

import pygame

from util import magnitude, vector_add, vector_sub, scalar_division, distance
from settings import WIDTH, HEIGHT


class Boid(pygame.sprite.Sprite):

    def __init__(self, r1_factor, r2_factor, r3_factor, color):
        super().__init__()
        self.image = pygame.surface.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(random.randrange(WIDTH), random.randrange(HEIGHT)))

        self.velocity = [random.randrange(200), random.randrange(200)]
        self.velocity_limit = 4
        self.r1_factor = r1_factor
        self.r2_factor = r2_factor
        self.r3_factor = r3_factor

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
        self.velocity = vector_add(self.velocity, self.boundary_behavior())

        # --- Limiting Speed ---
        if magnitude(self.velocity) > self.velocity_limit:
            self.velocity = [(v / magnitude(self.velocity)) * self.velocity_limit for v in self.velocity]

    def move(self):
        # --- Movement ---
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

        # --- Boundary Checks ---
        # TODO: This behaviour changes influences neighbourhoods because of their current definition.
        if self.rect.centerx < 0:
            self.rect.centerx = WIDTH
        elif self.rect.centerx > WIDTH:
            self.rect.centerx = 0

        if self.rect.centery < 0:
            self.rect.centery = HEIGHT
        elif self.rect.centery > HEIGHT:
            self.rect.centery = 0

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
        # r1_factor = 100 to move 1% towards the perceived center of mass
        velocity_percentage = scalar_division(velocity, self.r1_factor)
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
        velocity_percentage = scalar_division(away_vector, self.r2_factor)
        return velocity_percentage

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
        velocity_percentage = scalar_division(velocity_diff, self.r3_factor)
        return velocity_percentage

    def boundary_behavior(self):
        velocity = [0, 0]
        # if self.rect.centerx < 0 or self.rect.centerx > WIDTH:
        #     velocity[0] = -self.velocity[0]
        #
        # if self.rect.centery < 0 or self.rect.centery > HEIGHT:
        #     velocity[1] = -self.velocity[1]
        return velocity
