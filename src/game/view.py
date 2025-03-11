import platform
import os


class ConsoleInterface:
    @staticmethod
    def clear():
        os.system("cls" if platform.system() == "Windows" else "clear")

    @staticmethod
    def display_board(board):
        print("\n" + "=" * 40)
        for q in range(4):
            print(f"\nQuadrante {q + 1}")
            for row in board[q]:
                print(" | ".join(row))
                print("-" * 14)

    @staticmethod
    def get_move_input():
        try:
            move = input("Sua jogada (quadrante,linha,coluna): ")
            return tuple(map(int, move.split(",")))
        except:
            return None

    @staticmethod
    def show_message(message):
        print(f"\n{message}")

    @staticmethod
    def show_instructions():
        print("\nInstruções:")
        print(
            "Para fazer uma jogada, informe o quadrante, linha e coluna separados por vírgula."
        )
        print(
            "Por exemplo, para fazer uma jogada no quadrante 1, linha 2 e coluna 3, digite: 1,2,3"
        )
        print(
            "Ganha quem formar uma linha de 4 símbolos iguais em qualquer dimensão!\n"
        )
