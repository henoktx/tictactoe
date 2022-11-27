from game_logic import tictactoe

jogo = tictactoe.Game()

resp = input("Você deseja iniciar um servidor ou se conectar?(s/c) ")

if resp == "s":
    jogo.iniciar_server()
else:
    jogo.conectar_jogo()