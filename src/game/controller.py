import time
from .core import TicTacToe3D
from .view import ConsoleInterface
from network.client import GameClient
from network.server import GameServer
from network.discovery import NetworkDiscovery, DiscorveyClient
import threading


class GameController:
    def __init__(self):
        self.game = TicTacToe3D()
        self.view = ConsoleInterface()
        self.network_discovery = NetworkDiscovery()
        self.discovery_client = DiscorveyClient()
        self.server = None
        self.client = None
        self.connection = None
        self.player_symbol = "X"
        self.running = True
        self.opponent_connected = threading.Event()

    def host_game(self):
        self.view.clear()
        self.view.show_message("Hosteando jogo...")

        self.server = GameServer()
        threading.Thread(target=self.server.start).start()

        self.network_discovery.start_server_discovery()

        self.server.ready.wait()
        self.opponent_connected.set()
        self.view.show_message("Jogador conectado! Iniciando...")
        self.connection = self.server.connections[0]
        threading.Thread(target=self._receive_messages).start()
        self._game_loop()

    def join_game(self, ip):
        self.view.clear()
        self.client = GameClient(ip)

        if self.client.connect():
            self.connection = self.client.socket
            self.player_symbol = "O"
            self.opponent_connected.set()
            threading.Thread(target=self._receive_messages).start()
            self.view.show_message("Conectado! O jogo vai começar...")
            self._game_loop()
        else:
            self.view.show_message("Falha na conexão")

    def _game_loop(self):
        try:
            self.opponent_connected.wait()

            while self.running:
                self.view.display_board(self.game.board)

                if self.game.game_over:
                    self._handle_game_over()
                    break

                if self.game.current_player == self.player_symbol:
                    self._handle_local_turn()
                else:
                    self._handle_remote_turn()
        except KeyboardInterrupt:
            self._cleanup()
        finally:
            self._cleanup()

    def _handle_local_turn(self):
        move = None
        while not move:
            move = self.view.get_move_input()
            if move:
                q, r, c = map(lambda x: x - 1, move)
                if not self.game.make_move(q, r, c):
                    self.view.show_message("Jogada inválida!")
                    move = None
                else:
                    self.connection.send(f"{q + 1},{r + 1},{c + 1}".encode())
                    self.view.clear()

    def _handle_remote_turn(self):
        self.view.show_message("Aguardando jogada do oponente...")
        while (
            self.game.current_player != self.player_symbol and not self.game.game_over
        ):
            time.sleep(0.1)

    def _handle_client(self, client_sock):
        self.connection = client_sock
        self.player_symbol = "X"
        threading.Thread(target=self._receive_messages).start()
        self.view.show_message("Jogador conectado! Iniciando jogo...")

    def _receive_messages(self):
        while self.running and not self.game.game_over:
            try:
                data = self.connection.recv(4096)
                if not data:
                    self._handle_disconnection()
                    break

                if data == b"QUIT":
                    self.view.clear()
                    self.view.show_message("O oponente desconectou")
                    self.running = False
                    break
                elif data == "RESTART":
                    self.game.reset_game()
                    self.view.show_message("Novo jogo iniciado!")
                else:
                    q, r, c = map(lambda x: int(x) - 1, data.decode().split(","))
                    self.game.make_move(q, r, c)
                    self.view.clear()
            except (ConnectionResetError, BrokenPipeError):
                self._hande_disconnection()
                break
            except Exception as e:
                self.view.show_message(str(e))
                break

    def _handle_game_over(self):
        if self.game.winner == self.player_symbol:
            self.view.show_message("Você venceu!")
        elif self.game.winner:
            self.view.show_message("Você perdeu!")
        else:
            self.view.show_message("Deu velha!")

        while True:
            resp = input("Jogar novamente? (s/n): ").lower()
            if resp == "s":
                if self.connection:
                    self.connection.send(b"RESTART")
                self._reset_game()
                break
            elif resp == "n":
                if self.connection:
                    self.connection.send(b"QUIT")
                self._cleanup()
                break
            else:
                print("Opção inválida")

    def _handle_disconnection(self):
        self.view.show_message("Conexão com o oponente perdida!")
        self.running = False
        self._cleanup()

    def _cleanup(self):
        if self.server:
            self.server.stop()
        if self.client:
            self.client.disconnect()
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
        self.running = False

    def _reset_game(self):
        self.game.reset_game()
        self.opponent_connected.clear()
        if self.player_symbol == "O":
            self.player_symbol = "X"
        else:
            self.player_symbol = "O"
        self.view.clear()
        self.opponent_connected.set()
