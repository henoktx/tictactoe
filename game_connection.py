import socket
import threading

class Jogo_Conexao:
    
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_info = None
    
    def hostear_jogo(self, handle_conexao):
        print("Iniciando servidor...")
        self.notificar()
        
        endereco = socket.gethostbyname(socket.gethostname())
        server = self.tcp_socket
        server.bind((endereco, 7000))
        
        server.listen(1)
        
        cliente, cliente_end = server.accept()
        print("Um jogador se conectou")
        
        threading.Thread(target=handle_conexao, args=(cliente,))
        
        server.close()
        
    def conectar_jogo(self, handle_conexao):
        self.procurar_servidor()
        
        resp = input(f"Deseja se conectar ao servidor {self.server_info[0]}? (s/n) ")

        if resp == "n":
            return
        else:
            cliente = self.tcp_socket
            cliente.connect(self.server_info)
            
            threading.Thread(target=handle_conexao, args=(cliente,)).start()
                
    def notificar(self):
        info_server = (('', 7007))
        mensagem = "tem eu"
        
        server = self.udp_socket 
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
        achou = False
        
        cliente = self.udp_socket
        
        cliente.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cliente.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
        threading.Thread(target=verifica_mensagem_recebida).start()
        
        while True:
            cliente.sendto(mensagem.encode(), ('255.255.255.255', 7007))
            sleep(2)
            
            if achou:
                break
            
            tentativas += 1
        
    def verifica_mensagem_recebida(self):
        cliente = self.udp_socket
        
        while True:
            dados, endereco = cliente.recvfrom(4096)
            dados = str(dados.decode('utf-8'))
            
            if dados == "tem eu":
                achou = True
                self.server_info
                print(f"Servidor {endereco[0]} encontrado")
                cliente.close()
                break;