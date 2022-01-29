import pygame

from .game_window import GameWindow
from .movement import Movement


class Main:
    """
    Entry point for clients/players
    """

    def __init__(self):
        """
        Initialize window
        """
        self.game_window = GameWindow()

    def start(self):
        """
        Start the game
        """
        is_open = True
        while is_open:
            self.game_window.draw()
            for event in self.game_window.window.update():
                if event.type == pygame.KEYDOWN:
                    Movement.key_down(event, self.game_window.game)
                elif event.type == pygame.KEYUP:
                    Movement.key_up(event, self.game_window.game)
                elif event.type == pygame.QUIT:
                    is_open = False
