import pygame

from .constants import HALF_PAD_HEIGHT, HALF_PAD_WIDTH, HEIGHT, PAD_WIDTH, WIDTH, Color
from .game import Game
from .paddle import Paddle
from .window import Window


class GameWindow:
    """
    Game window
    """

    def __init__(self):
        """
        Initialize Game Window
        """
        pygame.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 10)
        self.window = Window(size=(WIDTH, HEIGHT), name="Pong")
        self.game = Game()
        self.canvas = pygame.Surface((WIDTH, HEIGHT))

    def draw(self):
        """
        Draw game UI
        """
        self.canvas.fill(Color.BLACK.value)
        self.game.update_server_data()
        self.game.update_multiplayer_data()
        self.game.define_player()
        self.game.run_pause()
        self.draw_default_lines()
        self.game.update_paddle_pos()
        self.game.update_ball_pos()
        self.draw_ball_and_paddles()
        self.game.check_ball_collision()
        self.window.smooth_scaled_blit(self.canvas)

    def draw_left_right_paddle(self, paddle: Paddle):
        """
        Draw left right paddle
        :param paddle: Paddle object
        """
        pygame.draw.polygon(
            self.canvas,
            Color.GREEN.value,
            [
                [paddle.pos[0] - HALF_PAD_WIDTH, paddle.pos[1] - HALF_PAD_HEIGHT],
                [paddle.pos[0] - HALF_PAD_WIDTH, paddle.pos[1] + HALF_PAD_HEIGHT],
                [paddle.pos[0] + HALF_PAD_WIDTH, paddle.pos[1] + HALF_PAD_HEIGHT],
                [paddle.pos[0] + HALF_PAD_WIDTH, paddle.pos[1] - HALF_PAD_HEIGHT],
            ],
            0,
        )

    def draw_top_bottom_paddle(self, paddle: Paddle):
        """
        Draw top bottom paddle
        :param paddle: Paddle object
        """
        pygame.draw.polygon(
            self.canvas,
            Color.GREEN.value,
            [
                [paddle.pos[0] - HALF_PAD_HEIGHT, paddle.pos[1] - HALF_PAD_WIDTH],
                [paddle.pos[0] - HALF_PAD_HEIGHT, paddle.pos[1] + HALF_PAD_WIDTH],
                [paddle.pos[0] + HALF_PAD_HEIGHT, paddle.pos[1] + HALF_PAD_WIDTH],
                [paddle.pos[0] + HALF_PAD_HEIGHT, paddle.pos[1] - HALF_PAD_WIDTH],
            ],
            0,
        )

    def draw_left_paddle(self, paddle: Paddle):
        """
        Draw left paddle
        :param paddle: Paddle object
        """
        self.draw_left_right_paddle(paddle)
        name = self.font.render("Me" if self.game.paddle == paddle else paddle.name, True, (255, 255, 255))
        self.canvas.blit(name, ((PAD_WIDTH + 10), HEIGHT // 2))

    def draw_right_paddle(self, paddle):
        """
        Draw right paddle
        :param paddle: Paddle object
        """
        self.draw_left_right_paddle(paddle)
        name = self.font.render("Me" if self.game.paddle == paddle else paddle.name, True, (255, 255, 255))
        self.canvas.blit(name, ((WIDTH - PAD_WIDTH - 10 - name.get_width()), HEIGHT // 2))

    def draw_top_paddle(self, paddle):
        """
        Draw top paddle
        :param paddle: Paddle object
        """
        self.draw_top_bottom_paddle(paddle)
        name = self.font.render("Me" if self.game.paddle == paddle else paddle.name, True, (255, 255, 255))
        self.canvas.blit(name, ((WIDTH // 2 - name.get_width() // 2), PAD_WIDTH + 10))

    def draw_bottom_paddle(self, paddle):
        """
        Draw bottom paddle
        :param paddle: Paddle object
        """
        self.draw_top_bottom_paddle(paddle)
        name = self.font.render("Me" if self.game.paddle == paddle else paddle.name, True, (255, 255, 255))
        self.canvas.blit(name, ((WIDTH // 2 - name.get_width() // 2), HEIGHT - PAD_WIDTH - 10 - name.get_height()))

    def draw_ball_and_paddles(self):
        """
        Draw ball and paddle
        """
        pygame.draw.circle(self.canvas, Color.RED.value, self.game.ball.pos, 20, 0)
        for _paddle in self.game.other_paddles + [self.game.paddle]:
            getattr(self, f"draw_{_paddle.loc}_paddle")(_paddle)

    def draw_default_lines(self):
        """
        Draw default game lines
        """
        pygame.draw.circle(self.canvas, Color.WHITE.value, [WIDTH // 2, HEIGHT // 2], HEIGHT // 6, 1)
        pygame.draw.line(self.canvas, Color.WHITE.value, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(self.canvas, Color.WHITE.value, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(self.canvas, Color.WHITE.value, [0, PAD_WIDTH], [WIDTH, PAD_WIDTH], 1)
        pygame.draw.line(self.canvas, Color.WHITE.value, [0, WIDTH - PAD_WIDTH], [WIDTH, WIDTH - PAD_WIDTH], 1)
