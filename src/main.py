from game.controller import GameController


def main():
    controller = GameController()
    controller.view.clear()

    print("Jogo da Velha 3D")
    print("1. Hostear jogo")
    print("2. Conectar a um jogo")
    choice = input("Escolha uma opção: ")

    if choice == "1":
        controller.host_game()
    elif choice == "2":
        servers = controller.discovery_client.find_servers()
        if servers:
            print("\nServidores encontrados:")
            for i, ip in enumerate(servers):
                print(f"{i + 1}. {ip}")
            selection = int(input("Escolha um servidor: ")) - 1
            controller.join_game(servers[selection])
        else:
            print("Nenhum servidor encontrado")
    else:
        print("Opção inválida")


if __name__ == "__main__":
    main()
