# Tictactoe 3D
Jogo da velha 3D, multiplayer, com o tabuleiro 4x4x4, via terminal. Para jogar, basta seguir os passos descritos nesse arquivo.
## Requisitos
* Python 3.12

## Execução
1. Primeiramente, clone esse repositório:

```
git clone git@github.com:henoktx/tictactoe.git
```
2. Após isso, vá para a pasta e execute o comando:

```
uv run src/main.py
```
3. Você poderá escolher entre hostear um servidor ou se conectar a um presente na rede.

## Funcionamento
O jogo usa um sistema de descoberta automática do servidor (broadcast), por meio de um socket UDP. Uma vez descoberto o servidor, é estabelecido uma conexão, usando agora socket TCP, e realizada a troca de informações.
