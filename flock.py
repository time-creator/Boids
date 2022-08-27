import pygame

from boid import Boid

from util import distance


class Flock(pygame.sprite.Group):

    def __init__(self,
                 size,
                 perception_radius,
                 r1_factor,
                 r2_factor,
                 r3_factor,
                 color='green'):
        super().__init__()

        self.perception_radius = perception_radius
        self.r1_factor = r1_factor
        self.r2_factor = r2_factor
        self.r3_factor = r3_factor

        for _ in range(size):
            self.add(Boid(r1_factor, r2_factor, r3_factor, color))

    def update(self):
        for sprite in self.sprites():
            if isinstance(sprite, Boid):
                # Update/move all boids in the flock.
                neighbourhood = []
                for other_sprite in self.sprites():
                    if distance(list(sprite.rect.center), list(other_sprite.rect.center)) < self.perception_radius:
                        if sprite != other_sprite:
                            neighbourhood.append(other_sprite)
                sprite.update(neighbourhood, 1, 1, 1)

        for sprite in self.sprites():
            if isinstance(sprite, Boid):
                sprite.move()
