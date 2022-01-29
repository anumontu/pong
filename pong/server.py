import json
import select
import socket
import sys
import time

from app.config import SERVER_IP, SERVER_PORT
from app.constants import BUFFER_SIZE, DONT_WRITE_BYTE_CODE

sys.dont_write_bytecode = DONT_WRITE_BYTE_CODE


class GameServer:
    """
    Pong Game Server
    """

    def __init__(self, host: str, port: int):
        """
        Initialize server
        :param host: Server host
        :param port: Server port
        """
        self.input_list = []
        self.channel = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(0)
        self.players = {}

    def run(self, max_players: int):
        """
        Run server and listen for connections
        :param max_players: Maximum number of players allowed
        """
        self.input_list.append(self.server)
        while 1:
            time.sleep(0.01)
            input_r, output_r, except_r = select.select(self.input_list, [], [])
            for conn in input_r:
                if conn == self.server:
                    self.on_accept(max_players)
                    break
                else:
                    data = conn.recv(BUFFER_SIZE)
                if len(data) == 0:
                    self.on_close(conn)
                else:
                    self.on_recv(conn, data, max_players)

    def on_accept(self, max_players: int):
        """
        Accept incoming client connection
        :param max_players: Maximum number of players allowed
        """
        client_sock, client_addr = self.server.accept()
        print(f"{client_addr} has connected")
        if len(self.players) >= max_players:
            print(f"Connection overflow. Max players: {max_players}")
        else:
            self.players[client_addr[1]] = {}
            self.input_list.append(client_sock)

    def on_close(self, conn: socket.socket):
        """
        Client disconnect handling
        :param conn: Client socket connection
        """
        client_addr = conn.getpeername()
        print(f"{client_addr} has disconnected")
        del self.players[client_addr[1]]
        self.input_list.remove(conn)

    def on_recv(self, conn: socket.socket, data: bytes, max_players: int):
        """
        Handle data received
        :param conn: Client socket connection
        :param data: Incoming message
        :param max_players: Maximum number of players allowed
        """
        try:
            player_id = conn.getpeername()[1]
            self.players[player_id] = json.loads(data.decode("utf-8"))
            data = {"max_players": max_players, "players": self.players}
            conn.send(json.dumps(data).encode("utf-8"))
        except json.decoder.JSONDecodeError:
            print("Invalid json data")


if __name__ == "__main__":
    server = GameServer(SERVER_IP, SERVER_PORT)
    try:
        no_of_players = input("Enter number of players:")
        if not no_of_players.isdigit():
            print("Invalid Input")
            sys.exit(1)
        if 1 <= int(no_of_players) <= 4:
            print("Server listening...")
            server.run(int(no_of_players))
        else:
            print("Invalid no of players")
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ctrl C - Stopping server")
        sys.exit(1)
