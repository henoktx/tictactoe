import socket
import game_connection

class Game:
    
    def __init__(self):
        self.quadro = [[[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]], 
                       [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]]
        self.vez = "X"
        self.voce = "X"
        self.oponente = "O"
        self.vencedor = None
        self.acabou = False
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
        
        while not self.acabou:
            if self.vez == self.voce:
                jogada = input("Faça uma jogada (quadro, linha, coluna): ")
                
                if self.jogada_valida(jogada.split(',')):
                    jogador.send(jogada.encode('utf-8'))
                    self.gerencia_jogadas(jogada.split(','), self.voce)
                    self.vez = self.oponente
                else:
                    print("Jogada inválida :|\n")
            else:
                dados = jogador.recv(4092)
                if not dados:
                    print("Vixe!")
                    break
                else:
                    print("Jogada do oponente:")
                    self.gerencia_jogadas(dados.decode('utf-8').split(','), self.oponente)
                    self.vez = self.voce
        
        jogador.close()

    def gerencia_jogadas(self, jogada, jogador):
        if self.acabou:
            return
        
        self.contador += 1
        self.quadro[int(jogada[0])][int(jogada[1])][int(jogada[2])] = jogador
        self.desenhar_quadros()
        
        if self.verifica_vitoria():
            if self.vencedor == self.voce:
                print("Você ganhou :)")
                exit()
            else:
                print("Você perdeu :(")
                exit()
        else:
            if self.contador == 16:
                print("Deu velha :|")
                exit()
        
            
    def jogada_valida(self, jogada):
        try:
            quadro = int(jogada[0])
            linha = int(jogada[1])
            coluna = int(jogada[2])
            
            if quadro > 3 | linha > 3 | coluna > 3:
                return False
            elif self.quadro[int(jogada[0])][int(jogada[1])][int(jogada[2])] != " ":
                return False
            else:
                return True
        except:
            return False
    
    def verifica_vitoria(self):
        for quadro in range(4):    
            for linha in range(4):
                for coluna in range (4):
                    if self.quadro[0][linha][coluna] == self.quadro[1][linha][coluna] == self.quadro[2][linha][coluna] == self.quadro[3][linha][coluna] != " ":
                        self.vencedor = self.quadro[0][linha][coluna]
                        self.acabou = True
                        return True
                    
                if self.quadro[0][linha][0] == self.quadro[1][linha][1] == self.quadro[2][linha][2] == self.quadro[3][linha][3] != " ":
                    self.vencedor = self.quadro[0][linha][0]
                    self.acabou = True
                    return True
                if self.quadro[3][linha][0] == self.quadro[2][linha][1] == self.quadro[1][linha][2] == self.quadro[0][linha][3] != " ":
                    self.vencedor = self.quadro[3][linha][0]
                    self.acabou = True
                    return True
                if self.quadro[quadro][linha][0] == self.quadro[quadro][linha][1] == self.quadro[quadro][linha][2] == self.quadro[quadro][linha][3] != " ":
                    self.vencedor = self.quadro[quadro][linha][0]
                    self.acabou = True
                    return True
            for coluna in range(4):
                if self.quadro[0][0][coluna] == self.quadro[1][1][coluna] == self.quadro[2][2][coluna] == self.quadro[3][3][coluna] != " ":
                    self.vencedor = self.quadro[0][0][coluna]
                    self.acabou = True
                    return True
                if self.quadro[0][3][coluna] == self.quadro[1][2][coluna] == self.quadro[2][1][coluna] == self.quadro[3][0][coluna] != " ":
                    self.vencedor = self.quadro[0][3][coluna]
                    self.acabou = True
                    return True 
                if self.quadro[quadro][0][coluna] == self.quadro[quadro][1][coluna] == self.quadro[quadro][2][coluna] == self.quadro[quadro][3][coluna] != " ":
                    self.vencedor = self.quadro[quadro][0][coluna]
                    self.acabou = True
                    return True
            
            if self.quadro[quadro][0][0] == self.quadro[quadro][1][1] == self.quadro[quadro][2][2] == self.quadro[quadro][3][3] != " ":
                self.vencedor = self.quadro[quadro][0][0]
                self.acabou = True
                return True
            if self.quadro[quadro][0][3] == self.quadro[quadro][1][2] == self.quadro[quadro][2][1] == self.quadro[quadro][3][0] != " ":
                self.vencedor = self.quadro[quadro][0][0]
                self.acabou = True
                return True
            
        if self.quadro[0][0][0] == self.quadro[1][1][1] == self.quadro[2][2][2] == self.quadro[3][3][3] !=  " ":
                self.vencedor = self.quadro[0][0][0]
                self.acabou = True
                return True
        if self.quadro[0][0][3] == self.quadro[1][1][2] == self.quadro[2][2][1] == self.quadro[3][3][0] != " ":
                self.vencedor = self.quadro[0][3][0]
                self.acabou = True
                return True
        return False
    
    def desenhar_quadros(self):
        print(" ")
        for quadro in range(4):
            for linha in range(4):
                print(' | '.join(self.quadro[quadro][linha]))
                if linha != 3:
                    print("--------------")
            print("\n")
            
    def instrucoes(self):
        print("\nInstruções:\n")
        print("\t→ Use sempre as jogadas no formato 'quadro,linha,coluna'\n")
        print("\t→ Sempre quando for contar comece pelo 0\n")
        print("\t→ Ganha quem colocar 4 marcadares horizontalmente, ou verticalmente, ou diagonalmente") 
        print("\tno mesmo quadro ou combinando-os em sequencia, ou na mesma posicao em quadros diferentes\n")
        print("\t→ Bom jogo!\n")