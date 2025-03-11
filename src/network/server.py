import socket
import threading


class GameServer:
    def __init__(self, host="", port=7000):
        self.host = host
        self.port = port
        self._running = False
        self.connections = []
        self.ready = threading.Event()

    def start(self):
        self._running = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(1)

            client_sock, _ = sock.accept()
            self.connections.append(client_sock)
            self.ready.set()

    def stop(self):
        self._running = False
        for conn in self.connections:
            try:
                conn.send(b"QUIT")
                conn.close()
            except:
                pass
        self.connections.clear()
