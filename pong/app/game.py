import json
import socket
import sys

from .ball import Ball
from .config import SERVER_IP, SERVER_PORT
from .constants import (
    BALL_RADIUS,
    HALF_PAD_HEIGHT,
    HEIGHT,
    PAD_WIDTH,
    WIDTH,
    PaddleLocation,
    PaddlePosition,
)
from .paddle import Paddle


class Game:
    """
    Pong Game
    """

    def __init__(self):
        """
        Initialize pong game
        """
        self.me, self.conn = self.connect()
        self.max_players = 0
        self.paddle = None
        self.other_paddles = []
        self.primary = False
        self.running = False
        self.server_data = {}
        self.ball = Ball()

    @staticmethod
    def connect():
        """
        Create connection with server
        """
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((SERVER_IP, SERVER_PORT))
            me = str(conn.getsockname()[1])
            print(f"Client connected to {SERVER_IP}:{SERVER_PORT} with id: {me}")
            return [me, conn]
        except socket.error:
            print(f"Couldn't connect to game server in: {SERVER_IP}:{SERVER_PORT}")
            sys.exit(1)

    def run(self):
        """
        Start game (can only be done by primary client)
        """
        if not self.running and self.primary:
            self.running = True

    def pause(self):
        """
        Pause game (can only be done by primary client)
        """
        if self.running and self.primary:
            self.running = False
            self.ball = Ball()

    def run_pause(self):
        """
        Start/Pause game (can only be done by primary client)
        Game will start as soon as required number of players join
        """
        if len(self.server_data.keys()) == self.max_players:
            self.run()
        else:
            self.pause()

    def define_player(self):
        """
        Initialize player
        """
        if self.server_data:
            if self.me == sorted(self.server_data.keys())[0]:  # the first client connection
                self.primary = True
        if not self.paddle:
            if self.primary or self.other_paddles:
                other_loc = [_paddle.loc for _paddle in self.other_paddles]
                if PaddleLocation.LEFT.value not in other_loc:
                    self.paddle = Paddle(PaddlePosition.LEFT.value, PaddleLocation.LEFT.value, f"Player {self.me}")
                elif PaddleLocation.RIGHT.value not in other_loc:
                    self.paddle = Paddle(PaddlePosition.RIGHT.value, PaddleLocation.RIGHT.value, f"Player {self.me}")
                elif PaddleLocation.TOP.value not in other_loc:
                    self.paddle = Paddle(PaddlePosition.TOP.value, PaddleLocation.TOP.value, f"Player {self.me}")
                elif PaddleLocation.BOTTOM.value not in other_loc:
                    self.paddle = Paddle(PaddlePosition.BOTTOM.value, PaddleLocation.BOTTOM.value, f"Player {self.me}")

    def update_server_data(self):
        """
        Send and receive server data
        """
        data = {}
        if self.paddle:
            data = {
                "ball": {"pos": self.ball.pos, "vel": self.ball.vel},
                "paddle": {
                    "pos": self.paddle.pos,
                    "loc": self.paddle.loc,
                    "vel": self.paddle.vel,
                    "name": self.paddle.name,
                },
                "running": self.running,
                "primary": self.primary,
                "name": self.paddle.name,
            }
        self.conn.send(json.dumps(data).encode("utf-8"))
        server_data = json.loads(self.conn.recv(2000).decode("utf-8"))
        self.max_players = (
            server_data["max_players"] if server_data and "max_players" in server_data else self.max_players
        )
        self.server_data = server_data["players"] if server_data and "players" in server_data else self.server_data

    def update_multiplayer_data(self):
        """
        Update other players data
        """
        self.other_paddles = []
        for player_id in self.server_data.keys():
            if player_id != self.me:
                player_data = self.server_data[player_id]
                if "primary" in player_data and player_data["primary"] and "running" in player_data:
                    self.running = player_data["running"]
                if "paddle" in player_data:
                    self.other_paddles.append(
                        Paddle(
                            player_data["paddle"]["pos"],
                            player_data["paddle"]["loc"],
                            player_data["paddle"]["name"],
                            player_data["paddle"]["vel"],
                        )
                    )
                if not self.primary and "primary" in player_data and player_data["primary"] and "ball" in player_data:
                    self.ball.pos = player_data["ball"]["pos"]
                    self.ball.vel = player_data["ball"]["vel"]

    @classmethod
    def validate_left_paddle_pos(cls, paddle: Paddle):
        """
        Validate left paddle position
        :param paddle: Paddle object
        """
        if paddle.pos[1] < HALF_PAD_HEIGHT:
            paddle.pos[1] = HALF_PAD_HEIGHT
        elif paddle.pos[1] > HEIGHT - HALF_PAD_HEIGHT:
            paddle.pos[1] = HEIGHT - HALF_PAD_HEIGHT

    @classmethod
    def validate_right_paddle_pos(cls, paddle: Paddle):
        """
        Validate right paddle position
        :param paddle: Paddle object
        """
        if paddle.pos[1] < HALF_PAD_HEIGHT:
            paddle.pos[1] = HALF_PAD_HEIGHT
        elif paddle.pos[1] > HEIGHT - HALF_PAD_HEIGHT:
            paddle.pos[1] = HEIGHT - HALF_PAD_HEIGHT

    @classmethod
    def validate_top_paddle_pos(cls, paddle: Paddle):
        """
        Validate top paddle position
        :param paddle: Paddle object
        """
        if paddle.pos[0] < HALF_PAD_HEIGHT:
            paddle.pos[0] = HALF_PAD_HEIGHT
        elif paddle.pos[0] > WIDTH - HALF_PAD_HEIGHT:
            paddle.pos[0] = HEIGHT - HALF_PAD_HEIGHT

    @classmethod
    def validate_bottom_paddle_pos(cls, paddle: Paddle):
        """
        Validate bottom paddle position
        :param paddle: Paddle object
        """
        if paddle.pos[0] < HALF_PAD_HEIGHT:
            paddle.pos[0] = HALF_PAD_HEIGHT
        elif paddle.pos[0] > WIDTH - HALF_PAD_HEIGHT:
            paddle.pos[0] = HEIGHT - HALF_PAD_HEIGHT

    def update_paddle_pos(self):
        """
        Update paddle position
        """
        for _paddle in self.other_paddles + [self.paddle]:
            if _paddle.loc in [PaddleLocation.LEFT.value, PaddleLocation.RIGHT.value]:
                _paddle.pos[1] += _paddle.vel
            else:
                _paddle.pos[0] += _paddle.vel
            getattr(Game, f"validate_{_paddle.loc}_paddle_pos")(_paddle)

    def update_ball_pos(self):
        """
        Update ball position (Can be done only by primary client)
        """
        if self.running and self.primary:
            self.ball.pos[0] += int(self.ball.vel[0])
            self.ball.pos[1] += int(self.ball.vel[1])

    def check_ball_collision_left_pos(self, paddle: Paddle):
        """
        Check ball collision on left edge
        :param paddle: Paddle object
        """
        if int(self.ball.pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(self.ball.pos[1]) in range(
            paddle.pos[1] - HALF_PAD_HEIGHT, paddle.pos[1] + HALF_PAD_HEIGHT, 1
        ):
            self.ball.vel[0] = -self.ball.vel[0]
            self.ball.vel[0] *= 1.1
            self.ball.vel[1] *= 1.1
        elif int(self.ball.pos[0]) <= BALL_RADIUS + PAD_WIDTH:
            self.ball = Ball()

    def check_ball_collision_right_pos(self, paddle: Paddle):
        """
        Check ball collision on right edge
        :param paddle: Paddle object
        """
        if int(self.ball.pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(self.ball.pos[1]) in range(
            paddle.pos[1] - HALF_PAD_HEIGHT, paddle.pos[1] + HALF_PAD_HEIGHT, 1
        ):
            self.ball.vel[0] = -self.ball.vel[0]
            self.ball.vel[0] *= 1.1
            self.ball.vel[1] *= 1.1
        elif int(self.ball.pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
            self.ball = Ball()

    def check_ball_collision_top_pos(self, paddle: Paddle):
        """
        Check ball collision on top edge
        :param paddle: Paddle object
        """
        if int(self.ball.pos[1]) <= BALL_RADIUS + PAD_WIDTH and int(self.ball.pos[0]) in range(
            paddle.pos[0] - HALF_PAD_HEIGHT, paddle.pos[0] + HALF_PAD_HEIGHT, 1
        ):
            self.ball.vel[1] = -self.ball.vel[1]
            self.ball.vel[0] *= 1.1
            self.ball.vel[1] *= 1.1
        elif int(self.ball.pos[1]) <= BALL_RADIUS + PAD_WIDTH:
            self.ball = Ball()

    def check_ball_collision_bottom_pos(self, paddle: Paddle):
        """
        Check ball collision on bottom edge
        :param paddle: Paddle object
        """
        if int(self.ball.pos[1]) >= HEIGHT + 1 - BALL_RADIUS - PAD_WIDTH and int(self.ball.pos[0]) in range(
            paddle.pos[0] - HALF_PAD_HEIGHT, paddle.pos[0] + HALF_PAD_HEIGHT, 1
        ):
            self.ball.vel[1] = -self.ball.vel[1]
            self.ball.vel[0] *= 1.1
            self.ball.vel[1] *= 1.1
        elif int(self.ball.pos[1]) >= HEIGHT + 1 - BALL_RADIUS - PAD_WIDTH:
            self.ball = Ball()

    def check_left_collision(self):
        """
        Check if ball can bounce from left edge
        """
        loc = [_paddle.loc for _paddle in self.other_paddles + [self.paddle]]
        if PaddleLocation.LEFT.value not in loc:
            if int(self.ball.pos[0]) <= PAD_WIDTH + BALL_RADIUS:
                self.ball.vel[0] = -self.ball.vel[0]

    def check_right_collision(self):
        """
        Check if ball can bounce from right edge
        """
        loc = [_paddle.loc for _paddle in self.other_paddles + [self.paddle]]
        if PaddleLocation.RIGHT.value not in loc:
            if int(self.ball.pos[0]) >= WIDTH + 1 - PAD_WIDTH - BALL_RADIUS:
                self.ball.vel[0] = -self.ball.vel[0]

    def check_top_collision(self):
        """
        Check if ball can bounce from top edge
        """
        loc = [_paddle.loc for _paddle in self.other_paddles + [self.paddle]]
        if PaddleLocation.TOP.value not in loc:
            if int(self.ball.pos[1]) <= PAD_WIDTH + BALL_RADIUS:
                self.ball.vel[1] = -self.ball.vel[1]

    def check_bottom_collision(self):
        """
        Check if ball can bounce from bottom edge
        """
        loc = [_paddle.loc for _paddle in self.other_paddles + [self.paddle]]
        if PaddleLocation.BOTTOM.value not in loc:
            if int(self.ball.pos[1]) >= HEIGHT + 1 - PAD_WIDTH - BALL_RADIUS:
                self.ball.vel[1] = -self.ball.vel[1]

    def check_ball_collision(self):
        """
        Check ball collisions with paddle or edges (Can be checked by primary client only)
        """
        if self.primary:
            self.check_left_collision()
            self.check_right_collision()
            self.check_top_collision()
            self.check_bottom_collision()
            for _paddle in self.other_paddles + [self.paddle]:
                getattr(self, f"check_ball_collision_{_paddle.loc}_pos")(_paddle)
