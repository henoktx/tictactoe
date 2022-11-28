import socket
import threading
import time

class Jogo_Conexao:
    
    def __init__(self):
        self.server_info = None
        self.achou = False
        self.jogo_comecou = False
    
    def hostear_jogo(self, other):
        print("\nIniciando servidor...")
        threading.Thread(target=self.recebe_notifica).start()
        
        endereco = socket.gethostbyname(socket.gethostname())
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((endereco, 7000))
        
        server.listen(1)
        
        cliente, cliente_end = server.accept()
        print(f"Um jogador se conectou ({cliente_end[0]})")
        
        threading.Thread(target=other.handle_conexao, args=(cliente,)).start()
        self.jogo_comecou = True
        server.close()

        
    def conectar_jogo(self, other):
        self.procurar_servidor()
        
        while True:
            resp = input(f"Deseja se conectar ao servidor {self.server_info}?(s/n) ")
            
            if resp == "n":
                return
            elif resp == "s":
                break
            else: 
                print("Não entendi :/\n")
                continue
        
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((self.server_info, 7000))
                
        threading.Thread(target=other.handle_conexao, args=(cliente,)).start()
                
    def recebe_notifica(self):
        info_server = (('', 7007))
        mensagem = "tem eu"
        
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        server.bind(info_server)
        
        while not self.jogo_comecou:
            dados, endereco = server.recvfrom(4096)
            dados = str(dados.decode('utf-8'))
            
            if dados == "algum servidor ai?":
                server.sendto(mensagem.encode(), endereco)
               
    def procurar_servidor(self):
        print("\nProcurando servidor...")
        
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
                self.server_info = endereco[0]
                print(f"Servidor {endereco[0]} encontrado")
                cliente.close()
                break;