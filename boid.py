import math


class Boid:

    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.acceleration = [0, 0]
        self.direction = 0
        self.maxspeed = 5

    def update(self):
        self.x += int(self.velocity[0] * math.cos(math.radians(self.direction))
                      - self.velocity[1] * math.sin(math.radians(self.direction)))
        self.y += int(self.velocity[0] * math.sin(math.radians(self.direction))
                      + self.velocity[1] * math.cos(math.radians(self.direction)))

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        # limit speed
        norm_velocity = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if norm_velocity > self.maxspeed:
            self.velocity = [v / norm_velocity * self.maxspeed for v in self.velocity]

        # Maybe borders should get checked in the main loop and not here
        if self.x > 1200:
            self.x = 0
        elif self.x < 0:
            self.x = 1200

        if self.y > 750:
            self.y = 0
        elif self.y < 0:
            self.y = 750
