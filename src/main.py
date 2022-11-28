from game_logic import tictactoe

jogo = tictactoe.Game()

while True:
    resp = input("Você deseja iniciar um servidor ou se conectar?(s/c) ")

    if resp == "s":
        jogo.iniciar_server()
        break
    elif resp == "c":
        jogo.conectar_jogo()
        break
    else:
        print("Não entendi :/\n")
        continue