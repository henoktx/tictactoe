import socket
import threading
import time

class Jogo_Conexao:
    
    def __init__(self):
        self.server_info = None
        self.achou = False
    
    def hostear_jogo(self, other):
        print("Iniciando servidor...")
        self.recebe_notifica()
        
        endereco = socket.gethostbyname(socket.gethostname())
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((endereco, 7000))
        
        server.listen(1)
        
        cliente, cliente_end = server.accept()
        print("Um jogador se conectou")
        
        threading.Thread(target=other.handle_conexao, args=(cliente,)).start()
        server.close()

        
    def conectar_jogo(self, other):
        self.procurar_servidor()
        
        resp = input(f"Deseja se conectar ao servidor {self.server_info[0]}?(s/n) ")

        if resp == "n":
            return
        else:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((self.server_info[0], 7000))
            
            threading.Thread(target=other.handle_conexao, args=(cliente,)).start()
                
    def recebe_notifica(self):
        info_server = (('', 7007))
        mensagem = "tem eu"
        
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        server.bind(info_server)
        
        while True:
            dados, endereco = server.recvfrom(4096)
            dados = str(dados.decode('utf-8'))
            
            if dados == "algum servidor ai?":
                server.sendto(mensagem.encode(), endereco)
                break;
               
    def procurar_servidor(self):
        print("Procurando servidor...")
        
        mensagem = "algum servidor ai?"

        cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        cliente.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cliente.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        threading.Thread(target=self.verifica_mensagem_recebida_cliente, args=(cliente,)).start()
        
        while True:
            cliente.sendto(mensagem.encode("utf-8"), ('255.255.255.255', 7007))
            time.sleep(2)
            
            if self.achou:
                break
        
    def verifica_mensagem_recebida_cliente(self, cliente):        
        while True:
            dados, endereco = cliente.recvfrom(4096)
            dados = str(dados.decode('utf-8'))
            
            if dados == "tem eu":
                self.achou = True
                self.server_info = endereco
                print(f"Servidor {endereco[0]} encontrado")
                cliente.close()
                break;