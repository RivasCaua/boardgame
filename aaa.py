from tabulate import tabulate
import csv
from random import randint 
import os

# Funções de cores
def colored(text, color):
    colors = {
        'red': '\033[91m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    return f"{colors[color]}{text}{colors['reset']}"

# Funções 
def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def verif_opc(selecao, opcoes):
    while selecao not in opcoes:
        selecao = input('Digite uma opção correta: ')

    return selecao 


def verifvencedor(dificuldade, tabuleiro, objetivo):
    triunfo = False
    dici = {'Sequência Ascendente': (1, 2),
            'Sequência Descendente': (-1, -2),
            'Sequência Pares': (2, 4),
            'Sequência Ímpares': (2, 4)}

    valor_objetivo = dici.get(objetivo)
    tamanho = len(tabuleiro)

    def check_sequence(sequencia):
        if objetivo in ['Sequência Pares', 'Sequência Ímpares']:
            if all(isinstance(x, int) for x in sequencia) and len(set(x % 2 for x in sequencia)) == 1:
                return True
        elif all(isinstance(x, int) for x in sequencia):
            return sequencia == list(range(sequencia[0], sequencia[0] + valor_objetivo[1] + 1, valor_objetivo[0]))
        return False

    for linha in range(tamanho):
        for coluna in range(tamanho):
            if isinstance(tabuleiro[linha][coluna], int):
                # Verificação horizontal
                if coluna + 2 < tamanho and check_sequence(tabuleiro[linha][coluna:coluna+3]):
                    print('Partida Finalizada! Vencedor!')
                    triunfo = True
                    return triunfo

                # Verificação vertical
                if linha + 2 < tamanho and check_sequence([tabuleiro[linha+k][coluna] for k in range(3)]):
                    print('Partida Finalizada! Vencedor!')
                    triunfo = True
                    return triunfo

                # Verificação diagonal principal
                if linha + 2 < tamanho and coluna + 2 < tamanho and check_sequence([tabuleiro[linha+k][coluna+k] for k in range(3)]):
                    print('Partida Finalizada! Vencedor!')
                    triunfo = True
                    return triunfo

                # Verificação diagonal secundária
                if linha + 2 < tamanho and coluna - 2 >= 0 and check_sequence([tabuleiro[linha+k][coluna-k] for k in range(3)]):
                    print('Partida Finalizada! Vencedor!')
                    triunfo = True
                    return triunfo

    return triunfo


def gerarjogo(modo_jogo):
    if modo_jogo == FACIL:
        salvar = None

        input(f'Para ver o objetivo do {jogador1}, aperte em qualquer tecla: ')
        jogador1_obj = objetivojogador(jogador1)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        input(f'Para ver o objetivo do {jogador2}, aperte em qualquer tecla: ')
        jogador2_obj = objetivojogador(jogador2)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        lista_numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        triunfo = False
        contador_jogadas = 1

        tabuleiro = [['a1', 'a2', 'a3'], 
                     ['b1', 'b2', 'b3'],
                     ['c1', 'c2', 'c3']]
        
        posicoes_letra = {'a': 0, 'b': 1, 'c': 2}
        posicoes_num = {'1': 0, '2': 1, '3': 2}
        
        with open('tabuleiro.csv', 'w', newline='') as arquivo_escrita:
            escritor = csv.writer(arquivo_escrita)

            for linha in tabuleiro:
                escritor.writerow(linha)

        while not triunfo and len(lista_numeros) > 0:
            clear_terminal()
            print(lista_numeros)
            imprimir_tabuleiro(tabuleiro)

            jogada_letra = input('Conforme o tabuleiro apresentado, selecione a letra em que deseja posicionar a sua jogada: ')
            jogada_numero = input('Conforme o tabuleiro apresentado, selecione o número em que deseja posicionar a sua jogada: ')
            
            if jogada_letra in posicoes_letra and jogada_numero in posicoes_num:
                num = int(input('Digite o número que deseja jogar: '))
                if num in lista_numeros:
                    tabuleiro[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = colored(num, 'red' if contador_jogadas % 2 == 1 else 'blue')
                    lista_numeros.remove(num)
                    contador_jogadas += 1

                    triunfo = verifvencedor('Facil', tabuleiro, jogador1_obj if contador_jogadas % 2 == 0 else jogador2_obj)
                    if triunfo:
                        imprimir_tabuleiro(tabuleiro)
                        break

                    if salvar == 'Sim':
                        with open('tabuleiro.csv', 'w', newline='') as arquivo_escrita:
                            escritor = csv.writer(arquivo_escrita)
                            for linha in tabuleiro: 
                                escritor.writerow(linha)
                else:
                    print("Número já jogado ou inválido, tente novamente.")
            else:
                print("Jogada inválida, tente novamente.")

    elif modo_jogo == MEDIO:
        salvar = None

        input(f'Para ver o objetivo do {jogador1}, aperte em qualquer tecla: ')
        jogador1_obj = objetivojogador(jogador1)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        input(f'Para ver o objetivo do {jogador2}, aperte em qualquer tecla: ')
        jogador2_obj = objetivojogador(jogador2)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        lista_numeros = [i for i in range(1, 17)]

        triunfo = False
        contador_jogadas = 1

        tabuleiro = [['a1', 'b1', 'c1', 'd1'],
                     ['a2', 'b2', 'c2', 'd2'],
                     ['a3', 'b3', 'c3', 'd3'],
                     ['a4', 'b4', 'c4', 'd4']]
        
        posicoes_letra = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        posicoes_num = {'1': 0, '2': 1, '3': 2, '4': 3}
        
        with open('tabuleiro.csv', 'w', newline='') as arquivo_escrita:
            escritor = csv.writer(arquivo_escrita)

            for linha in tabuleiro:
                escritor.writerow(linha)

        while not triunfo and len(lista_numeros) > 0:
            clear_terminal()
            print(lista_numeros)
            imprimir_tabuleiro(tabuleiro)

            jogada_letra = input('Conforme o tabuleiro apresentado, selecione a letra em que deseja posicionar a sua jogada: ')
            jogada_numero = input('Conforme o tabuleiro apresentado, selecione o número em que deseja posicionar a sua jogada: ')
            
            if jogada_letra in posicoes_letra and jogada_numero in posicoes_num:
                num = int(input('Digite o número que deseja jogar: '))
                if num in lista_numeros:
                    tabuleiro[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = colored(num, 'red' if contador_jogadas % 2 == 1 else 'blue')
                    lista_numeros.remove(num)
                    contador_jogadas += 1

                    triunfo = verifvencedor('Medio', tabuleiro, jogador1_obj if contador_jogadas % 2 == 0 else jogador2_obj)
                    if triunfo:
                        imprimir_tabuleiro(tabuleiro)
                        break

                    if salvar == 'Sim':
                        with open('tabuleiro.csv', 'w', newline='') as arquivo_escrita:
                            escritor = csv.writer(arquivo_escrita)
                            for linha in tabuleiro: 
                                escritor.writerow(linha)
                else:
                    print("Número já jogado ou inválido, tente novamente.")
            else:
                print("Jogada inválida, tente novamente.")

    elif modo_jogo == DIFICIL:
        salvar = None

        input(f'Para ver o objetivo do {jogador1}, aperte em qualquer tecla: ')
        jogador1_obj = objetivojogador(jogador1)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        input(f'Para ver o objetivo do {jogador2}, aperte em qualquer tecla: ')
        jogador2_obj = objetivojogador(jogador2)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        lista_numeros = [i for i in range(1, 26)]

        triunfo = False
        contador_jogadas = 1

        tabuleiro = [['a1', 'b1', 'c1', 'd1', 'e1'],
                     ['a2', 'b2', 'c2', 'd2', 'e2'],
                     ['a3', 'b3', 'c3', 'd3', 'e3'],
                     ['a4', 'b4', 'c4', 'd4', 'e4'],
                     ['a5', 'b5', 'c5', 'd5', 'e5']]
        
        posicoes_letra = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
        posicoes_num = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}
        
        with open('tabuleiro.csv', 'w', newline='') as arquivo_escrita:
            escritor = csv.writer(arquivo_escrita)

            for linha in tabuleiro:
                escritor.writerow(linha)

        while not triunfo and len(lista_numeros) > 0:
            clear_terminal()
            print(lista_numeros)
            imprimir_tabuleiro(tabuleiro)

            jogada_letra = input('Conforme o tabuleiro apresentado, selecione a letra em que deseja posicionar a sua jogada: ')
            jogada_numero = input('Conforme o tabuleiro apresentado, selecione o número em que deseja posicionar a sua jogada: ')
            
            if jogada_letra in posicoes_letra and jogada_numero in posicoes_num:
                num = int(input('Digite o número que deseja jogar: '))
                if num in lista_numeros:
                    tabuleiro[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = colored(num, 'red' if contador_jogadas % 2 == 1 else 'blue')
                    lista_numeros.remove(num)
                    contador_jogadas += 1

                    triunfo = verifvencedor('Dificil', tabuleiro, jogador1_obj if contador_jogadas % 2 == 0 else jogador2_obj)
                    if triunfo:
                        imprimir_tabuleiro(tabuleiro)
                        break

                    if salvar == 'Sim':
                        with open('tabuleiro.csv', 'w', newline='') as arquivo_escrita:
                            escritor = csv.writer(arquivo_escrita)
                            for linha in tabuleiro: 
                                escritor.writerow(linha)
                else:
                    print("Número já jogado ou inválido, tente novamente.")
            else:
                print("Jogada inválida, tente novamente.")

    return tabuleiro


def imprimir_tabuleiro(tabuleiro):
    tabuleiro_formatado = tabulate(tabuleiro, tablefmt='grid')
    print(tabuleiro_formatado)


def objetivojogador(nome_jogador):
    objetivos = ['Sequência Ascendente', 'Sequência Descendente', 'Sequência Pares', 'Sequência Ímpares']
    jogador_objetivo = objetivos[randint(0, 3)]
    print(f'{nome_jogador}, o seu objetivo é... {jogador_objetivo}')
    return jogador_objetivo


# variáveis e constantes que auxiliam nas seleções do menu 

# Menu inicial 
menu_inicial = ''
INICIAR_JOGO = '1'
VERIF_RANKING = '2'
SAIR = '3'
OPC_INICIAL = [INICIAR_JOGO, VERIF_RANKING, SAIR]

# Menu de jogos
modo_jogo = ''
FACIL = '1'
MEDIO = '2'
DIFICIL = '3'
MODOS = {FACIL, MEDIO, DIFICIL} 

# Código principal 
menu_inicial = input('''SEJA BEM VINDO(A) AO TABULEIRO DE NÚMEROS
                   
1 - INICIAR UM NOVO JOGO
2 - VER RANKING
3 - SAIR
                   
''')

menu_inicial = verif_opc(menu_inicial, OPC_INICIAL)

if menu_inicial == INICIAR_JOGO:
    print('Digite os seus nomes...')
    jogador1 = input('Jogador 1: ')
    jogador2 = input('Jogador 2: ')

    modo_jogo = input('''
---- Escolha o seu modo de jogo ---- 

1 - 3x3 (Fácil)
2 - 4x4 (Médio)
3 - 5x5 (Difícil)
                      
''')
    
    modo_jogo = verif_opc(modo_jogo, MODOS)

    lista_jogo = gerarjogo(modo_jogo)

    imprimir_tabuleiro(lista_jogo)
