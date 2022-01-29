from enum import Enum

DONT_WRITE_BYTE_CODE = True
BUFFER_SIZE = 2000
WIDTH = 720
HEIGHT = 720
BALL_RADIUS = 15
PAD_WIDTH = 10
PAD_HEIGHT = 150
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2


class Color(Enum):
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)


class Velocity(Enum):
    """
    Paddle velocity
    """

    PADDLE = 8


class PaddlePosition(Enum):
    """
    Paddle InitialPosition
    """

    LEFT = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
    RIGHT = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
    TOP = [WIDTH // 2, HALF_PAD_WIDTH - 1]
    BOTTOM = [WIDTH // 2, HEIGHT + 1 - HALF_PAD_WIDTH]


class PaddleLocation(Enum):
    """
    Paddle Location
    """

    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
