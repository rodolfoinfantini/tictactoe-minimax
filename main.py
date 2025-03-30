#!/usr/bin/env python
# coding: utf-8

# # Parte 1 - Jogo da Velha

# ### Passo 1: Criar uma função que escreve na tela o tabuleiro

# In[ ]:

import time
import sys
sys.setrecursionlimit(1000)


def mostra_tabuleiro(tabuleiro):

    print("-------------")  # Marca uma divisão entre telas para controle visual

    for linha in tabuleiro:

        print("|", linha[0], "|", linha[1], "|", linha[2], "|")

        # Marca uma divisão entre telas para controle visual
        print("-------------")


# ### Passo 2: Criar as regras para que o jogo seja finalizado

# In[ ]:


def verifica_vitoria(tabuleiro, jogador):

    # Vamos verificar possibilidade de vitória por sequência horizontal
    for i in range(0, 3):

        if tabuleiro[i][0] == jogador and tabuleiro[i][1] == jogador and tabuleiro[i][2] == jogador:

            return True

    # Vamos verificar possibilidade de vitória por sequência vertical
    for i in range(0, 3):

        if tabuleiro[0][i] == jogador and tabuleiro[1][i] == jogador and tabuleiro[2][i] == jogador:

            return True

    # Vamos verificar possibilidade de vitória na diagonal
    if tabuleiro[0][0] == jogador and tabuleiro[1][1] == jogador and tabuleiro[2][2] == jogador:

        return True

    if tabuleiro[0][2] == jogador and tabuleiro[1][1] == jogador and tabuleiro[2][0] == jogador:

        return True

    return False


# ### Passo 3: Criar a função que inicializa o jogo

# In[ ]:

def jogada_maquina(tabuleiro, jogador):
    tree = generate_tree(Node(Board(tabuleiro, jogador)), jogador)

    possible_scores = [(minimax(node, jogador), node, False)
                       for node in tree.nodes]

    for score in possible_scores:
        if score[0] == 10:
            return score[1].value.played

    # Simular jogadas inimigas para bloquear derrotas
    opponent = get_next_player(jogador)
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == " ":
                tabuleiro[i][j] = opponent
                if verifica_vitoria(tabuleiro, opponent):
                    tabuleiro[i][j] = " "
                    return (i, j)
                tabuleiro[i][j] = " "

    selected = possible_scores[0]
    for score in possible_scores:
        if score[0] > selected[0]:
            selected = score

    return selected[1].value.played


def start_jogo():

    # Criação da lista que gera o tabuleiro
    tabuleiro = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]

    # Jogadores existentes
    jogadores = ["X", "O"]

    # Define o marcador que inicia o jogo
    jogador_atual = jogadores[0]

    # Printa o tabuleiro na tela
    mostra_tabuleiro(tabuleiro)

    # Definindo o posicionamento dos marcadores
    for i in range(1, 10):
        linha = 0
        coluna = 0

        if jogador_atual == "O":
            (linha, coluna) = jogada_maquina(tabuleiro, jogador_atual)
        else:
            linha = int(
                input(f"Jogador {jogador_atual} escolha uma linha 1 - 3: ")) - 1
            coluna = int(
                input(f"Jogador {jogador_atual} escolha uma coluna 1 - 3: ")) - 1

        # Verificando se a posicao escolhida e valida
        if tabuleiro[linha][coluna] != " ":

            print("Posição ocupada.\nEscolha outra opção.")
            linha = int(
                input(f"Jogador {jogador_atual} escolha uma linha 1 - 3: ")) - 1
            coluna = int(
                input(f"Jogador {jogador_atual} escolha uma coluna 1 - 3: ")) - 1

        tabuleiro[linha][coluna] = jogador_atual
        mostra_tabuleiro(tabuleiro)

        if verifica_vitoria(tabuleiro, jogador_atual):

            print(f"Jogador {jogador_atual} venceu!!!")
            return

        # Precisamos alterar entre os jogadores
        jogador_atual = jogadores[i % 2]

    # Caso nenhuma das condições de vitória sejam encontradas, devemos considerar o resultado de empate
    print("O jogo terminou empatado.")


# In[ ]:


def get_next_player(turn):
    if turn == "X":
        return "O"
    return "X"


class Board:
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn
        self.tie = False
        self.winner = None
        if (verifica_vitoria(board, "O")):
            self.winner = "O"
        elif (verifica_vitoria(board, "X")):
            self.winner = "X"

    def play(self, mi, mj):
        board_clone = [["", "", ""], ["", "", ""], ["", "", ""]]
        for i in range(3):
            for j in range(3):
                board_clone[i][j] = self.board[i][j]
        board_clone[mi][mj] = self.turn
        return board_clone

    def all_empty_slots(self):
        slots = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == " ":
                    slots.append((i, j))

        return slots


def generate_tree(node, turn):
    if (node.value.winner is not None):
        return node

    slots = node.value.all_empty_slots()
    if (len(slots) == 0):
        node.value.tie = True
        return node

    next_turn = get_next_player(turn)
    for (i, j) in slots:
        new_board = Board(node.value.play(i, j), next_turn)
        new_board.played = (i, j)
        new_node = generate_tree(Node(new_board), next_turn)
        node.add(new_node)

    return node


def minimax(tree, player, maximizing_player=True, depth=0):
    if (tree.value.winner == player):
        return 10-depth
    if (tree.value.winner == get_next_player(player)):
        return -1+depth
    if (tree.value.tie):
        return 0

    if maximizing_player:
        value = -sys.maxsize
        for node in tree.nodes:
            value = max(value, minimax(
                node, player, not maximizing_player, depth+1))
        return value
    else:
        value = sys.maxsize
        for node in tree.nodes:
            value = min(value, minimax(
                node, player, not maximizing_player, depth+1))
        return value


class Node:
    def __init__(self, value):
        self.nodes = []
        self.value = value

    def add(self, node):
        self.nodes.append(node)


start_jogo()
