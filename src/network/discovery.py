import socket
import threading
import time

class NetworkDiscovery:
    def __init__(self):
        self._running = False
        self.default_response = "DISCOVERY_RESPONSE"

    def start_server_discovery(self, response=None):
        self._running = True
        response = response or self.default_response
        threading.Thread(target=self._server_discovery, args=(response,)).start()

    def stop_server_discovery(self):
        self._running = False

    def _server_discovery(self, response):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind(("", 7007))

            while self._running:
                try:
                    data, addr = sock.recvfrom(4096)
                    if data.decode() == "DISCOVERY_REQUEST":
                        sock.sendto(response.encode(), addr)
                except:
                    continue


class DiscorveyClient:
    def __init__(self, timeout=5):
        self.timeout = timeout

    def find_servers(self):
        servers = []
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(self.timeout)

            sock.sendto(b"DISCOVERY_REQUEST", ("255.255.255.255", 7007))

            start_time = time.time()
            while time.time() - start_time < self.timeout:
                try:
                    data, addr = sock.recvfrom(4096)
                    if data.decode() == "DISCOVERY_RESPONSE":
                        servers.append(addr[0])
                except socket.timeout:
                    break
        
        return servers