import socket
import threading
import game_connection

class Game:
    
    def __init__(self):
        self.quadro = [[[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]]
        self.vez = "X"
        self.voce = None
        self.oponente = None
        self.vencedor = None
        self.acabou = False
        self.contador = 0
        self.conexao = Jogo_Conexao()
        
    def iniciar_server(self):
        self.voce = "X"
        self.oponente = "O"
        
        self.conexao.hostear_jogo(self.handle_conexao)
        
    def conectar_jogo(self):
        self.voce = "O"
        self.oponente = "X"
        
        self.conexao.conectar_jogo(self.handle_conexao)
        
    def handle_conexao(self, jogador):
        while not self.acabou:
            if self.vez == self.voce:
                jogada = input("Faça uma jogada (linha, coluna, quadro): ")
                
                if self.jogada_valida(jogada.split(",")):
                    self.gerencia_jogadas(jogada.split(","), self.voce)
                    self.turn = self.oponente
                    jogador.send(jogada.encode('utf-8'))
                else:
                    print("Jogada inválida")
            else:
                dados = jogador.recv(1024)
                if not dados:
                    print("Vixe!")
                    jogador.close()
                    break
                else:
                    self.gerencia_jogadas(dados.decode("utf-8").split(","), self.oponente)
                    self.vez = self.voce
        jogador.close()

    def gerencia_jogadas(self, jogada, jogador):
        if self.acabou:
            return
        else:
            self.contador += 1
            self.quadro[int(jogada[0])][int(jogada[1])][int(jogada[2])] = jogador
            
    def jogada_valida(self, jogada):
        return self.quadro[int(jogada[0])][int(jogada[1])][int(jogada[2])] == " "
    
    def verifica_vitoria(self):
        for quadro in range(4):    
            for linha in range(4):
                for coluna in range (4):
                    if self.quadro[linha][coluna][0] == self.quadro[linha][coluna][1] == self.quadro[linha][coluna][2] == self.quadro[linha][coluna][3] != " ":
                        self.vencedor = self.quadro[linha][coluna][0]
                        self.acabou = True
                        return True
                    
                if self.quadro[linha][0][0] == quadro[linha][1][1] == quadro[linha][2][2] == quadro[linha][3][3] != " ":
                    self.vencedor = self.quadro[linha][0][0]
                    self.acabou = True
                    return True
                if self.quadro[linha][3][0] == quadro[linha][2][1] == quadro[linha][1][2] == quadro[linha][0][3] != " ":
                    self.vencedor = self.quadro[linha][3][0]
                    self.acabou = True
                    return True
                if self.quadro[linha][0][quadro] == self.quadro[linha][1][quadro] == self.quadro[linha][2][quadro] == self.quadro[linha][3][quadro] != " ":
                    self.vencedor = self.quadro[linha][0][quadro]
                    self.acabou = True
                    return True
            for coluna in range(4):
                if self.quadro[0][coluna][0] == self.quadro[1][coluna][1] == self.quadro[2][coluna][2] == self.quadro[3][coluna][3] != " ":
                    self.vencedor = self.quadro[0][coluna][0]
                    self.acabou = True
                    return True
                if self.quadro[3][coluna][0] == self.quadro[2][coluna][1] == self.quadro[1][coluna][2] == self.quadro[0][coluna][3] != " ":
                    self.vencedor = self.quadro[3][coluna][0]
                    self.acabou = True
                    return True 
                if self.quadro[0][coluna][quadro] == quadro[1][coluna][quadro] == quadro[2][coluna][quadro] == quadro[3][coluna][quadro] != " ":
                    self.vencedor = self.quadro[0][coluna][quadro]
                    self.acabou = True
                    return True
            
            if self.quadro[0][0][quadro] == self.quadro[1][1][quadro] == self.quadro[2][2][quadro] == self.quadro[3][3][quadro] != " ":
                self.vencedor = self.quadro[0][0][quadro]
                self.acabou = True
                return True
            if self.quadro[0][3][quadro] == self.quadro[1][2][quadro] == self.quadro[2][1][quadro] == self.quadro[3][0][quadro] != " ":
                self.vencedor = self.quadro[0][0][quadro]
                self.acabou = True
                return True
            
        if self.quadro[0][0][0] == self.quadro[1][1][1] == self.quadro[2][2][2] == self.quadro[3][3][3] !=  " ":
                self.vencedor = self.quadro[0][0][0]
                self.acabou = True
                return True
        if self.quadro[0][3][0] == self.quadro[1][2][1] == self.quadro[2][1][2] == self.quadro[3][0][3] != " ":
                self.vencedor = self.quadro[0][3][0]
                self.acabou = True
                return True
        return False