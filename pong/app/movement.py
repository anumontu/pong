import pygame

from .constants import PaddleLocation, Velocity
from .game import Game


class Movement:
    """
    Paddle movements
    """

    @classmethod
    def key_down(cls, event: pygame.event, game: Game):
        """
        Handle key press
        :param event: Event
        :param game: Game object
        """
        if game.paddle.loc in [PaddleLocation.LEFT.value, PaddleLocation.RIGHT.value]:
            if event.key == pygame.K_UP:
                game.paddle.vel = -Velocity.PADDLE.value
            elif event.key == pygame.K_DOWN:
                game.paddle.vel = Velocity.PADDLE.value
        else:
            if event.key == pygame.K_LEFT:
                game.paddle.vel = -Velocity.PADDLE.value
            elif event.key == pygame.K_RIGHT:
                game.paddle.vel = Velocity.PADDLE.value

    @classmethod
    def key_up(cls, event: pygame.event, game: Game):
        """
        Handle key lift
        :param event: Event
        :param game: Game object
        """
        if game.paddle.loc in [PaddleLocation.LEFT.value, PaddleLocation.RIGHT.value]:
            if (event.key == pygame.K_UP and game.paddle.vel == -Velocity.PADDLE.value) or (
                event.key == pygame.K_DOWN and game.paddle.vel == Velocity.PADDLE.value
            ):
                game.paddle.vel = 0
        else:
            if (event.key == pygame.K_LEFT and game.paddle.vel == -Velocity.PADDLE.value) or (
                event.key == pygame.K_RIGHT and game.paddle.vel == Velocity.PADDLE.value
            ):
                game.paddle.vel = 0
