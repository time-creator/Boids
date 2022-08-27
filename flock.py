import pygame

from boid import Boid

from util import distance


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
