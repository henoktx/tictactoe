import socket


class GameClient:
    def __init__(self, server_ip, server_port=7000):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.connected = False

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            self.connected = True
            return self.connected
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False

    def disconnect(self):
        try:
            self.socket.send(b"QUIT")
            self.socket.close()
        except:
            pass
        self.connect = False
