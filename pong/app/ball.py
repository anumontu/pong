import random

from .constants import HEIGHT, WIDTH


class Ball:
    """
    Pong Ball
    """

    def __init__(self):
        """
        Initialize Ball object
        """
        self.pos = [WIDTH // 2, HEIGHT // 2]
        horizontal_velocity = random.randrange(3, 6)
        vertical_velocity = random.randrange(2, 5)
        while horizontal_velocity == vertical_velocity:
            vertical_velocity = random.randrange(2, 5)

        if random.randrange(0, 2) == 0:
            horizontal_velocity = -horizontal_velocity
        if random.randrange(0, 2) == 0:
            vertical_velocity = -vertical_velocity

        self.vel = [horizontal_velocity, vertical_velocity]
