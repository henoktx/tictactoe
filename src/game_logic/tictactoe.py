from connection import game_connection
import socket
import os

class Game:
    
    def __init__(self):
        self.quadro = []
        self.carregar_quadro()
        self.vez = "X"
        self.voce = "X"
        self.oponente = "O"
        self.vencedor = None
        self.vitoria = False
        self.velha = False
        self.contador = 0
        self.conexao = game_connection.Jogo_Conexao()
        
    def iniciar_server(self):
        self.voce = "X"
        self.oponente = "O"
        
        self.conexao.hostear_jogo(self)
        
    def conectar_jogo(self):
        self.voce = "O"
        self.oponente = "X"
        
        self.conexao.conectar_jogo(self)
        
    def handle_conexao(self, jogador):
        self.instrucoes()
        
        while True:
            if not self.vitoria | self.velha:    
                if self.vez == self.voce:
                    jogada = input("Faça uma jogada (quadro,linha,coluna): ")
                    
                    jogada_processada = self.processa_jogada(jogada)
                    print(jogada_processada)
                    
                    if self.jogada_valida(jogada_processada):
                        jogador.send(jogada.encode('utf-8'))
                        os.system("clear")
                        self.gerencia_jogadas(jogada_processada, self.voce)
                        self.vez = self.oponente
                    else:
                        print("Jogada inválida :|\n")
                else:
                    dados = jogador.recv(4092)
                    jogada_oponente = dados.decode('utf-8')
                    jogada_oponente_processada = self.processa_jogada(jogada_oponente)
                    if not dados:
                        print("Vixe!")
                        break
                    else:
                        print(f"Jogada do oponente: {jogada_oponente}")
                        self.gerencia_jogadas(jogada_oponente_processada, self.oponente)
                        self.vez = self.voce
            else:
                resp = input("\nDeseja iniciar um novo jogo?(s/n) ")
                if resp == "s":
                    jogador.send("s".encode("utf-8"))
                    print("Aguardando resposta do oponente...")
                    if jogador.recv(1024).decode("utf-8") == "s":
                        os.system("clear")
                        self.novo_jogo()
                        print("Novo jogo começando...\n")
                        continue
                    else:
                        print("\nOponente não quer continuar :/")
                        break
                elif resp == "n":
                    jogador.send("n".encode("utf-8"))
                    break
                else:
                    print("Não entendi :/")
                    continue
            
        jogador.close()
            
    def instrucoes(self):
        print("\nInstruções:\n")
        print("\t→ Use sempre as jogadas no formato 'quadro,linha,coluna' (sem espaços entre as vírgulas)\n")
        print("\t→ Sempre quando for contar um quadro, linha ou coluna, inicie pelo 1\n")
        print("\t→ Ganha quem colocar 4 marcadores horizontalmente, ou verticalmente, ou diagonalmente") 
        print("\tno mesmo quadro ou combinando-os em sequencia entre diferentes quadros, ou na mesma posicao em quadros diferentes\n")
        print("\t→ Bom jogo!\n") 
            
    def processa_jogada(self, jogada):
        jogada_processada = jogada.split(',')
        
        for i in range(len(jogada_processada)):
            jogada_processada[i] = (int(jogada_processada[i]) - 1) 
            
        return jogada_processada        
            
    def jogada_valida(self, jogada):    
        try:
            quadro = int(jogada[0])
            linha = int(jogada[1])
            coluna = int(jogada[2])
            
            if quadro > 4 | quadro <= 0 | linha > 4 | linha <= 0 | coluna > 4 | coluna <= 0:
                return False
            elif self.quadro[int(jogada[0])][int(jogada[1])][int(jogada[2])] != " ":
                return False
            else:
                return True
        except:
            return False

    def gerencia_jogadas(self, jogada, jogador):
        if self.vitoria:
            return
        if self.velha:
            return
        
        self.contador += 1
        self.quadro[int(jogada[0])][int(jogada[1])][int(jogada[2])] = jogador
        self.desenhar_quadros()
        
        if self.verifica_vitoria():
            if self.vencedor == self.voce:
                print("Você ganhou :)")
                return 
            else:
                print("Você perdeu :(")
                return 
        else:
            if self.verifica_velha():
                print("Deu velha :|")
                return
        
    def verifica_velha(self):
        if self.contador == 64:
            self.velha = True
            return True
        else:
            return False
        
    def desenhar_quadros(self):
        print(" ")
        for quadro in range(4):
            for linha in range(4):
                print(" | ".join(self.quadro[quadro][linha]))
                if linha != 3:
                    print("-------------")
            print("\n")
    
    def verifica_vitoria(self):
        for quadro in range(4):    
            for linha in range(4):
                for coluna in range (4):
                    if self.quadro[0][linha][coluna] == self.quadro[1][linha][coluna] == self.quadro[2][linha][coluna] == self.quadro[3][linha][coluna] != " ":
                        self.vencedor = self.quadro[0][linha][coluna]
                        self.vitoria = True
                        return True
                    
                if self.quadro[0][linha][0] == self.quadro[1][linha][1] == self.quadro[2][linha][2] == self.quadro[3][linha][3] != " ":
                    self.vencedor = self.quadro[0][linha][0]
                    self.vitoria = True
                    return True
                if self.quadro[3][linha][0] == self.quadro[2][linha][1] == self.quadro[1][linha][2] == self.quadro[0][linha][3] != " ":
                    self.vencedor = self.quadro[3][linha][0]
                    self.vitoria = True
                    return True
                if self.quadro[quadro][linha][0] == self.quadro[quadro][linha][1] == self.quadro[quadro][linha][2] == self.quadro[quadro][linha][3] != " ":
                    self.vencedor = self.quadro[quadro][linha][0]
                    self.vitoria = True
                    return True
            for coluna in range(4):
                if self.quadro[0][0][coluna] == self.quadro[1][1][coluna] == self.quadro[2][2][coluna] == self.quadro[3][3][coluna] != " ":
                    self.vencedor = self.quadro[0][0][coluna]
                    self.vitoria = True
                    return True
                if self.quadro[0][3][coluna] == self.quadro[1][2][coluna] == self.quadro[2][1][coluna] == self.quadro[3][0][coluna] != " ":
                    self.vencedor = self.quadro[0][3][coluna]
                    self.vitoria = True
                    return True 
                if self.quadro[quadro][0][coluna] == self.quadro[quadro][1][coluna] == self.quadro[quadro][2][coluna] == self.quadro[quadro][3][coluna] != " ":
                    self.vencedor = self.quadro[quadro][0][coluna]
                    self.vitoria = True
                    return True
            
            if self.quadro[quadro][0][0] == self.quadro[quadro][1][1] == self.quadro[quadro][2][2] == self.quadro[quadro][3][3] != " ":
                self.vencedor = self.quadro[quadro][0][0]
                self.vitoria = True
                return True
            if self.quadro[quadro][0][3] == self.quadro[quadro][1][2] == self.quadro[quadro][2][1] == self.quadro[quadro][3][0] != " ":
                self.vencedor = self.quadro[quadro][0][3]
                self.vitoria = True
                return True
            
        if self.quadro[0][0][0] == self.quadro[1][1][1] == self.quadro[2][2][2] == self.quadro[3][3][3] !=  " ":
                self.vencedor = self.quadro[0][0][0]
                self.vitoria = True
                return True
        if self.quadro[0][0][3] == self.quadro[1][1][2] == self.quadro[2][2][1] == self.quadro[3][3][0] != " ":
                self.vencedor = self.quadro[0][0][3]
                self.vitoria = True
                return True
        return False
    
    def carregar_quadro(self):
        self.quadro.clear()
        self.quadro = [[[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]]
    
    def novo_jogo(self):
        self.vitoria = False
        self.vencedor = None
        self.velha = False
        self.contador = 0
        self.carregar_quadro()