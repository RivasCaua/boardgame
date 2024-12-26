#DECLARAÇÃO DE NÃO PLÁGIO 
#Autor: Rivas Cauã Soares Uzêda
#Componente Curricular: MI algorítmos
#Concluido em: 07/07/2024
#Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
#trecho de código de outro colega ou de outro autor, tais como provindos de livros e
#apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
#de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
#do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.

from tabulate import tabulate
from random import randint 
import os
import re
import json

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


def jogadacolorida(num,jogador):
    cores = {'jogador1' : '\033[94m',
             'jogador2' : '\033[91m',
             'reset' : '\033[0m'}
    cor = cores[jogador]
    reset = cores['reset']
    
    return f'{cor}{num}{reset}'


def remover_cores(texto):
    # Remove sequências de escape ANSI
    return re.sub(r'\033\[\d+(;\d+)*m', '', texto)


def salvarjogo(nome_arquivo, estado):
    with open(nome_arquivo,'w') as arquivo:
        json.dump(estado, arquivo)  


def carregarjogo(nome_arquivo):
    with open(nome_arquivo,'r') as arquivo:
        estado_carregado = json.load(arquivo)
        return estado_carregado
    

def adicionarjogador(nome, pontuacao, ranking):
    if nome not in ranking:
        jogador = {"nome" : nome, "pontuacao" : pontuacao}
        ranking.append(jogador)


def atualizarpontuacao(nome, nova_pontuacao):
    for jogador in ranking:
        if jogador["nome"] == nome:
            jogador["pontuacao"] = nova_pontuacao
            break

def exibir_ranking(): 
    ranking_ordenado = sorted(ranking, key=lambda x: x["pontuacao"], reverse=True)
    tabela = tabulate(ranking_ordenado, headers="keys", tablefmt="grid")
    print(tabela)


def carregar_ranking(): 
    global ranking
    if os.path.exists("ranking.json"):
        with open("ranking.json", 'r') as arquivo:
            ranking = json.load(arquivo)
    else:
        ranking = []


def salvar_ranking(nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(ranking, arquivo)


def jogadaespecial(dificuldade, linhas_verif, jogador_especial, lista_num, linhas, jogador_atual):
    
    especial = int(input('''Deseja fazer uma jogada especial?
[1] - SIM
[2] - NAO

-> '''))

    if especial == 1:
        relacao_letra = {'a': 0, 'b': 1, 'c': 2, 'd' : 3, 'e' : 4}
        relacao_num = {'1': 0, '2': 1, '3': 2, '4' : 3, '5' : 4}
        relacao_num_letra = {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'e'}        

        dif = {'Facil' : 3,
               'Medio' : 4,
               'Dificil' : 5}

       

        tipo_remocao = int(input('''Deseja remover uma linha horizontal ou vertical?
[1] - Horizontal
[2] - Vertical

-> '''))

        if tipo_remocao == 1:
            selecao = input('Selecione a linha horizontal que você deseja remover (a-c): ')
                
            if selecao in relacao_letra:
                for cont in range(dif[dificuldade]):
                    numero = linhas_verif[relacao_letra[selecao]][cont]                                                
                    
                    if str(numero).isdigit():
                        numero = int(numero)
                        lista_num.append(numero)
                        lista_num.sort()
                    
                # Reseta a linha para as posições iniciais
                for cont in range(dif[dificuldade]):
                    linhas_verif[relacao_letra[selecao]][cont] = selecao + str(cont+1)                    
                    linhas[relacao_letra[selecao]][cont] = selecao + str(cont+1)
                    


                jogador_especial = True

        elif tipo_remocao == 2:
            selecao = input('Selecione a coluna vertical que você deseja remover (1-3): ')
                
            if selecao in relacao_num:
                for cont in range(dif[dificuldade]):
                    numero = linhas_verif[cont][relacao_num[selecao]]
                    
                    if str(numero).isdigit():
                        numero = int(numero)
                        lista_num.append(numero)
                        lista_num.sort()                           

                for cont in range(dif[dificuldade]):
                    linhas_verif[cont][relacao_num[selecao]] = relacao_num_letra[cont] + str(selecao)
                    linhas[cont][relacao_num[selecao]] = relacao_num_letra[cont] + str(selecao)
                    

        jogador_especial = True

    return jogador_especial, linhas_verif, lista_num, linhas, jogador_atual
        

        

def verifvencedor(dif, linhas, obj, triunfojogador):
    triunfojogador = False
    dici = {'Sequência Ascendente': (-1, +1),
            'Sequência Descendente': (+1, -1),
            'Sequência Pares': (-2, +2),
            'Sequência Ímpares': (-2, +2)}
    
    if dif == 'Facil':

        valor_obj = dici.get(obj)

        # Horizontal
        for cont in range(3):

            num = linhas[cont][1]

            if str(linhas[cont][0]).isdigit() and str(linhas[cont][1]).isdigit() and str(linhas[cont][2]).isdigit():
                
                if num % 2 == 0 and obj == 'Sequência Pares':    
                    if linhas[cont][0] == int(num) + int(valor_obj[0]) and linhas[cont][2] == int(num) + int(valor_obj[1]):          
                            print('Partida Finalizada!')
                            triunfojogador = True

                    elif linhas[cont][0] == int(num) + int(valor_obj[1]) and linhas[cont][2] == int(num) + int(valor_obj[0]):
                            print('Partida Finalizada!')
                            triunfojogador = True 
                                
                if num % 2 != 0 and obj == 'Sequência Ímpares':    
                    if linhas[cont][0] == int(num) + int(valor_obj[0]) and linhas[cont][2] == int(num) + int(valor_obj[1]):          
                            print('Partida Finalizada!') 
                            triunfojogador = True

                    elif linhas[cont][0] == int(num) + int(valor_obj[1]) and linhas[cont][2] == int(num) + int(valor_obj[0]):
                            print('Partida Finalizada!')
                            triunfojogador = True 

                if linhas[cont][0] == int(num) + int(valor_obj[0]) and linhas[cont][2] == int(num) + int(valor_obj[1]):   
                    print('Partida Finalizada!')
                    triunfojogador = True

        # Vertical
        for cont in range(3):

            num = linhas[1][cont]

            if str(linhas[0][cont]).isdigit() and str(linhas[1][cont]).isdigit() and str(linhas[2][cont]).isdigit():

                if num % 2 == 0 and obj == 'Sequência Pares':
                    if linhas[0][cont] == int(num) + int(valor_obj[0]) and linhas[2][cont] == int(num) + int(valor_obj[1]):
                            print('Partida Finalizada')
                            triunfojogador = True 

                    elif linhas[0][cont] == int(num) + int(valor_obj[1]) and linhas[2][cont] == int(num) + int(valor_obj[0]):
                            print('Partida Finalizada!')
                            triunfojogador = True

                if num % 2 != 0 and obj == 'Sequência Ímpares': 
                    if linhas[0][cont] == int(num) + int(valor_obj[0]) and linhas[2][cont] == int(num) + int(valor_obj[1]):
                            print('Partida Finalizada')
                            triunfojogador = True 

                    elif linhas[0][cont] == int(num) + int(valor_obj[1]) and linhas[2][cont] == int(num) + int(valor_obj[0]):
                            print('Partida Finalizada!')
                            triunfojogador = True

                if linhas[0][cont] == int(num) + int(valor_obj[0]) and linhas[cont][2] == int(num) + int(valor_obj[1]):
                    print('Partida Finalizada')
                    triunfojogador = True 

        # Diagonal 
        for cont in range(3):

            num = linhas[1][1]
            
            #Diagonal Principal
            if str(linhas[0][0]).isdigit() and str(linhas[1][1]).isdigit() and str(linhas[2][2]).isdigit():

                if num % 2 == 0 and obj == 'Sequência Pares':
                    
                    if linhas[0][0] == int(num) + int(valor_obj[0]) and linhas[2][2] == int(num) + int(valor_obj[1]):
                        print('Partida Finalizada')
                        triunfojogador = True

                    elif linhas[0][0] == int(num) + int(valor_obj[1]) and linhas[2][2] == int(num) + int(valor_obj[0]):
                        print('Partida Finalizada') 
                        triunfojogador = True

                if num % 2 != 0 and obj == 'Sequência Ímpares':

                    if linhas[0][0] == int(num) + int(valor_obj[0]) and linhas[2][2] == int(num) + int(valor_obj[1]):
                        print('Partida Finalizada')
                        triunfojogador = True

                    elif linhas[0][0] == int(num) + int(valor_obj[1]) and linhas[2][2] == int(num) + int(valor_obj[0]):
                        print('Partida Finalizada') 
                        triunfojogador = True

                if linhas[0][0] == int(num) + int(valor_obj[0]) and linhas[2][2] == int(num) + int(valor_obj[1]):
                    print('Partida Finalizada')
                    triunfojogador = True 

            #Diagonal Secundária
            if str(linhas[0][2]).isdigit() and str(linhas[1][1]).isdigit() and str(linhas[2][0]).isdigit():
                
                if num % 2 == 0 and obj == 'Sequência Pares':
                    if linhas[0][2] == int(num) + int(valor_obj[0]) and linhas[2][0] == int(num) + int(valor_obj[1]):
                        print('Partida Finalizada')
                        triunfojogador = True 

                    elif linhas[0][2] == int(num) + int(valor_obj[1]) and linhas[2][0] == int(num) + int(valor_obj[0]):
                        print('Partida Finalizada')
                        triunfojogador = True 

                if num % 2 != 0 and obj == 'Sequência Ímpares':
                    if linhas[0][2] == int(num) + int(valor_obj[0]) and linhas[2][0] == int(num) + int(valor_obj[1]):
                        print('Partida Finalizada')
                        triunfojogador = True 

                    elif linhas[0][2] == int(num) + int(valor_obj[1]) and linhas[2][0] == int(num) + int(valor_obj[0]):
                        print('Partida Finalizada')
                        triunfojogador = True 

                if linhas[0][2] == int(num) + int(valor_obj[0]) and linhas[2][0] == int(num) + int(valor_obj[1]):
                    print('Partida Finalizada')
                    triunfojogador = True 

    if dif == 'Medio':

        valor_obj = dici.get(obj)
        
        # Horizontal
        for cont in range(4):

            num1 = linhas[cont][1]
            num2 = linhas[cont][2]
            
            if str(linhas[cont][0]).isdigit and str(linhas[cont][1]).isdigit and str(linhas[cont][2]).isdigit() and str(linhas[cont][3]).isdigit():

                if num1 % 2 == 0 and obj == 'Sequência Pares':
                       
                    if int(num2) - int(num1) == 2:
                        if linhas[cont][0] == int(num1) + int(valor_obj[0]) and linhas[cont][3] == int(num2) + int(valor_obj[1]):
                               print('Partida Finalizada')
                               triunfojogador = True   
                        
                        elif int(num1) - int(num2) == 2:
                            if linhas[cont][0] == int(num1) + int(valor_obj[1]) and linhas[cont][3] == int(num2) + int(valor_obj[0]):
                                print('Partida Finalizada')
                                triunfojogador = True 

                if num1 % 2 != 0 and obj == 'SequÊncia Ímpares':

                    if int(num2) - int(num1) == 2:
                        if linhas[cont][0] == int(num1) + int(valor_obj[0]) and linhas[cont][3] == int(num2) + int(valor_obj[1]):
                            print('Partida Finalizada')
                            triunfojogador = True   
                        
                    elif int(num1) - int(num2) == 2:
                        if linhas[cont][0] == int(num1) + int(valor_obj[1]) and linhas[cont][3] == int(num2) + int(valor_obj[0]):
                            print('Partida Finalizada')
                            triunfojogador = True 
                
                if linhas[cont][0] == int(num1) + int(valor_obj[0]) and int(num1) + int(valor_obj[1]) == int(num2) and linhas[cont][3] == int(num2) + int(valor_obj[1]):
                    print('Partida Finalizada')
                    triunfojogador = True 


        # Vertical
        for cont in range(4):

            num1 = linhas[1][cont]
            num2 = linhas[2][cont]

            if str(linhas[0][cont]).isdigit() and str(linhas[1][cont]).isdigit() and str(linhas[2][cont]).isdigit() and str(linhas[3][cont]).isdigit():
                
                if num1 % 2 == 0 and obj == 'Sequência Pares':

                    if int(num2) - int(num1) == 2:
                        if linhas[0][cont] == int(num1) + int(valor_obj[0]) and linhas[3][cont] == int(num2) + int(valor_obj[1]):
                            print('Partida Finalizada')
                            triunfojogador = True 

                    elif int(num1) - int(num2) == 2:
                        if linhas[0][cont] == int(num1) + int(valor_obj[1]) and linhas[3][cont] == int(num2) + int(valor_obj[0]):
                            print('Partida Finalizada')
                            triunfojogador = True 

                if num1 % 2 != 0 and obj == 'Sequência Ímpares':
                    if int(num2) - int(num1) == 2:
                        if linhas[0][cont] == int(num1) + int(valor_obj[0]) and linhas[3][cont] == int(num2) + int(valor_obj[1]):
                            print('Partida Finalizada')
                            triunfojogador = True 

                    elif int(num1) - int(num2) == 2:
                        if linhas[0][cont] == int(num1) + int(valor_obj[1]) and linhas[3][cont] == int(num2) + int(valor_obj[0]):
                            print('Partida Finalizada')
                            triunfojogador = True 
                
                if linhas[0][cont] == int(num1) + int(valor_obj[0]) and int(num1) + int(valor_obj[1]) == int(num2) and linhas[3][cont] == int(num2) + int(valor_obj[1]):
                    print('Partida Finalizada')
                    triunfojogador = True 

        # Diagonal Secundaria
        for cont in range(4):

            num1 = linhas[1][1]
            num2 = linhas[2][2]

            if str(linhas[0][0]).isdigit() and str(linhas[1][1]).isdigit() and str(linhas[2][2]).isdigit() and str(linhas[3][3]).isdigit():
                
                if num1 % 2 == 0 and obj == 'Sequência Pares':
                    if int(num1) - int(num2) == 2:
                        if linhas[0][0] == int(num1) + int(valor_obj[1]) and linhas[3][3] == int(num2) + int(valor_obj[0]):
                            print('Partifa Finalizada')
                            triunfojogador = True

                    if int(num2) - int(num1) == 2:
                        if linhas[0][0] == int(num1) + int(valor_obj[0]) and linhas[3][3] == int(num2) + int(valor_obj[1]):
                            print('Partida Finalizada')
                            triunfojogador = True

                if num1 % 2 != 0 and obj == 'Sequência Ímpares':
                    if int(num1) - int(num2) == 2:
                        if linhas[0][0] == int(num1) + int(valor_obj[1]) and linhas[3][3] == int(num2) + int(valor_obj[0]):
                            print('Partida Finalizada')
                            triunfojogador = True 

                        if linhas[0][0] == int(num1) + int(valor_obj[0]) and linhas[3][3] == int(num2) + int(valor_obj[1]):
                            print('Partida Finalizada')
                            triunfojogador = True
               
                if linhas[0][0] == int(num1) + int(valor_obj[0]) and int(num1) + int(valor_obj[1]) == int(num2) and linhas[3][3] == int(num2) + int(valor_obj[1]):
                    print('Partida Finalizada')
                    triunfojogador = True

        # Diagonal Principal
        for cont in range(4):

            num1 = linhas[1][2]
            num2 = linhas[2][1]

            if str(linhas[0][3]).isdigit() and str(linhas[1][2]).isdigit() and str(linhas[2][1]).isdigit() and str(linhas[3][0]).isdigit():

                if num1 % 2 == 0 and obj == 'Sequência Pares':
                    if int(num1) - int(num2) == 2:
                        if linhas[0][3] == int(num1) + int(valor_obj[1]) and linhas[3][0] == int(num2) + int(valor_obj[0]):
                            print('Partida Finalizada')
                            triunfojogador = True 

                    if int(num2) - int(num1) == 2:
                        if linhas[0][3] == int(num1) + int(valor_obj[0]) and linhas[3][0] == int(num2) + int(valor_obj[1]):
                            print('partida Finalizada')
                            triunfojogador = True 

                if num1 % 2 != 0 and obj == 'Sequência Ímpares':
                    if int(num1) - int(num2) == 2:
                        if linhas[0][3] == int(num1) + int(valor_obj[1]) and linhas[3][0] == int(num2) + int(valor_obj[0]):
                            print('Partida Finalizada')
                            triunfojogador = True 

                    if int(num2) - int(num1) == 2:
                        if linhas[0][3] == int(num1) + int(valor_obj[0]) and linhas[3][0] == int(num2) + int(valor_obj[1]):
                            print('partida Finalizada')
                            triunfojogador = True 
                
                if linhas[0][3] == int(num1) + int(valor_obj[0]) and int(num1) + int(valor_obj[1]) == int(num2) and linhas[3][0] == int(num2) + int(valor_obj[1]):
                    print('Partida Finalizada')
                    triunfojogador = True 

    if dif == 'Dificil':

        valor_obj = dici.get(obj)

        #Horizontal
        for cont in range(5):
            num = linhas[cont][2]

            if str(linhas[cont][0]).isdigit() and str(linhas[cont][1]).isdigit() and str(linhas[cont][2]).isdigit() and str(linhas[cont][3]).isdigit() and str(linhas[cont][4]).isdigit():
                if num % 2 == 0 and obj == 'Sequência Pares':
                    if linhas[cont][0] == int(num) + int(valor_obj[0])*2 and linhas[cont][1] == int(num) + int(valor_obj[0]) and linhas[cont][3] == int(num) + int(valor_obj[1]) and linhas[cont][4] == int(num) + int(valor_obj[1])*2:
                        print('Partida Finalizada')
                        triunfojogador = True

                    if linhas[cont][0] == int(num) + int(valor_obj[1])*2 and linhas[cont][1] == int(num) + int(valor_obj[1]) and linhas[cont][3] == int(num) + int(valor_obj[0]) and linhas[cont][4] == int(num) + int(valor_obj[0])*2:
                        print('Partida Finalizada')
                        triunfojogador = True

                if num % 2 != 0 and obj == 'Sequência Ímpares':
                    if linhas[cont][0] == int(num) + int(valor_obj[0])*2 and linhas[cont][1] == int(num) + int(valor_obj[0]) and linhas[cont][3] == int(num) + int(valor_obj[1]) and linhas[cont][4] == int(num) + int(valor_obj[1])*2:
                        print('Partida Finalizada')
                        triunfojogador = True

                    if linhas[cont][0] == int(num) + int(valor_obj[1])*2 and linhas[cont][1] == int(num) + int(valor_obj[1]) and linhas[cont][3] == int(num) + int(valor_obj[0]) and linhas[cont][4] == int(num) + int(valor_obj[0])*2:
                        print('Partida Finalizada')
                        triunfojogador = True

                if linhas[cont][0] == int(num) + int(valor_obj[0])*2 and linhas[cont][1] == int(num) + int(valor_obj[0]) and linhas[cont][3] == int(num) + int(valor_obj[1]) and linhas[cont][4] == int(num) + int(valor_obj[1])*2:
                    print('Partida Finalizada')
                    triunfojogador = True 
        
        #Vertical
        for cont in range(5):
            num = linhas[2][cont]

            if str(linhas[0][cont]).isdigit() and str(linhas[1][cont]).isdigit() and str(linhas[2][cont]).isdigit() and str(linhas[3][cont]).isdigit() and str(linhas[4][cont]).isdigit():
                if num % 2 == 0 and obj == 'Sequência Pares':
                    if linhas[0][cont] == int(num) + int(valor_obj[0])*2 and linhas[1][cont] == int(num) + int(valor_obj[0]) and linhas[3][cont] == int(num) + int(valor_obj[1]) and linhas[4][cont] == int(num) + int(valor_obj[1])*2:
                        print('Partida Finalziada')
                        triunfojogador = True 

                    elif linhas[0][cont] == int(num) + int(valor_obj[1])*2 and linhas[1][cont] == int(num) + int(valor_obj[1]) and linhas[3][cont] == int(num) + int(valor_obj[0]) and linhas[4][cont] == int(num) + int(valor_obj[0])*2:
                        print('Partida Finalizada')
                        triunfojogador = True 

                if num % 2 != 0 and obj == 'Sequência Ímpares':
                    if linhas[0][cont] == int(num) + int(valor_obj[0])*2 and linhas[1][cont] == int(num) + int(valor_obj[0]) and linhas[3][cont] == int(num) + int(valor_obj[1]) and linhas[4][cont] == int(num) + int(valor_obj[1])*2:
                        print('Partida Finalziada')
                        triunfojogador = True 

                    elif linhas[0][cont] == int(num) + int(valor_obj[1])*2 and linhas[1][cont] == int(num) + int(valor_obj[1]) and linhas[3][cont] == int(num) + int(valor_obj[0]) and linhas[4][cont] == int(num) + int(valor_obj[0])*2:
                        print('Partida Finalizada')
                        triunfojogador = True 

                if linhas[0][cont] == int(num) + int(valor_obj[0])*2 and linhas[1][cont] == int(num) + int(valor_obj[0]) and linhas[3][cont] == int(num) + int(valor_obj[1]) and linhas[4][cont] == int(num) + int(valor_obj[1])*2:
                    print('Partida Finalizada')
                    triunfojogador = True 

        #Diagonal
        for cont in range(5):
            num = linhas[2][2]

            #Diagonal principal
            if str(linhas[0][0]).isdigit() and str(linhas[1][1]).isdigit() and str(linhas[2][2]).isdigit() and str(linhas[3][3]).isdigit() and str(linhas[4][4]).isdigit():
                if num % 2 == 0 and obj == 'Sequência Pares':
                    if linhas[0][0] == int(num) + int(valor_obj[0])*2 and linhas[1][1] == int(num) + int(valor_obj[0]) and linhas[3][3] == int(num) + int(valor_obj[1]) and linhas[4][4] == int(num) + int(valor_obj[1])*2:
                        print('Partida Finalizada')
                        triunfojogador = True 
                    
                    if linhas[0][0] == int(num) + int(valor_obj[1])*2 and linhas[1][1] == int(num) + int(valor_obj[1]) and linhas[3][3] == int(num) + int(valor_obj[0]) and linhas[4][4] == int(num) + int(valor_obj[0])*2:
                        print('Partida FInalizada')
                        triunfojogador = True 

                if num % 2 != 0 and obj == 'Sequência Ímpares':
                    if linhas[0][0] == int(num) + int(valor_obj[0])*2 and linhas[1][1] == int(num) + int(valor_obj[0]) and linhas[3][3] == int(num) + int(valor_obj[1]) and linhas[4][4] == int(num) + int(valor_obj[1])*2:
                        print('Partida Finalizada')
                        triunfojogador = True 
                    if linhas[0][0] == int(num) + int(valor_obj[1])*2 and linhas[1][1] == int(num) + int(valor_obj[1]) and linhas[3][3] == int(num) + int(valor_obj[0]) and linhas[4][4] == int(num) + int(valor_obj[0])*2:
                        print('Partida FInalizada')
                        triunfojogador = True 

                if linhas[0][0] == int(num) + int(valor_obj[0])*2 and linhas[1][1] == int(num) + int(valor_obj[0]) and linhas[3][3] == int(num) + int(valor_obj[1]) and linhas[4][4] == int(num) + int(valor_obj[1])*2:
                    print('Partida Finalizada')
                    triunfojogador = True 

            #Diagonal Secundaria
            if str(linhas[0][4]).isdigit() and str(linhas[1][3]).isdigit() and str(linhas[2][2]).isdigit() and str(linhas[3][1]).isdigit() and str(linhas[4][0]).isdigit():
                if num % 2 == 0 and obj == 'Sequência Pares':
                    if linhas[0][4] == int(num) + int(valor_obj[0])*2 and linhas[1][3] == int(num) + int(valor_obj[0]) and linhas[3][1] == int(num) + int(valor_obj[1]) and linhas[4][0] == int(num) + int(valor_obj[1])*2:
                        print('Partida Finalizada')
                        triunfojogador = True 

                    if linhas[0][4] == int(num) + int(valor_obj[1])*2 and linhas[1][3] == int(num) + int(valor_obj[1]) and linhas[3][1] == int(num) + int(valor_obj[0]) and linhas[4][0] == int(num) + int(valor_obj[0])*2:
                        print('Partida Finalizada')
                        triunfojogador = True
                
                if num % 2 != 0 and obj == 'Sequência Ímpares':
                    if linhas[0][4] == int(num) + int(valor_obj[0])*2 and linhas[1][3] == int(num) + int(valor_obj[0]) and linhas[3][1] == int(num) + int(valor_obj[1]) and linhas[4][0] == int(num) + int(valor_obj[1])*2:
                        print('Partida Finalizada')
                        triunfojogador = True 

                    if linhas[0][4] == int(num) + int(valor_obj[1])*2 and linhas[1][3] == int(num) + int(valor_obj[1]) and linhas[3][1] == int(num) + int(valor_obj[0]) and linhas[4][0] == int(num) + int(valor_obj[0])*2:
                        print('Partida Finalizada')
                        triunfojogador = True

                if linhas[0][4] == int(num) + int(valor_obj[0])*2 and linhas[1][3] == int(num) + int(valor_obj[0]) and linhas[3][1] == int(num) + int(valor_obj[1]) and linhas[4][0] == int(num) + int(valor_obj[1])*2:
                    print('Partida Finalizada')
                    triunfojogador = True 

    return triunfojogador 


def gerarjogo(modo_jogo):
    linhas = []
   
    
    if modo_jogo == FACIL:
        
        jogador1_especial = False
        jogador2_especial = False

        input(f'Para ver o objetivo do {jogador1}, aperte em qualquer tecla: ')
        jogador1_obj = objetivojogador(jogador1)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        input(f'Para ver o objetivo do {jogador2}, aperte em qualquer tecla: ')
        jogador2_obj = objetivojogador(jogador2)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        lista_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        triunfo_jogador1 = False
        triunfo_jogador2 = False
        
        cont_jogadas = 0

        linhas = [['a1', 'a2', 'a3'], 
                  ['b1', 'b2', 'b3'],
                  ['c1', 'c2', 'c3']]
        
        linhas_verif = [['a1', 'a2', 'a3'], 
                        ['b1', 'b2', 'b3'],
                        ['c1', 'c2', 'c3']]
        
        
        posicoes_letra = {'a': 0, 'b': 1, 'c': 2}
        posicoes_num = {'1': 0, '2': 1, '3': 2}
        

        while len(lista_num) > 0:
            cont_jogadas += 1
            clear_terminal()
            print(lista_num)
            imprimir_tabuleiro(linhas)

            if cont_jogadas > 1: 
                if jogo_especial == True: 

                    if jogador1_especial == False and cont_jogadas % 2 != 0:
                        jogador1_especial, linhas_verif, lista_num, linhas, jogador_atual = jogadaespecial('Facil', linhas_verif, jogador1_especial, lista_num, linhas, jogador_atual)                        
                        imprimir_tabuleiro(linhas)

                    elif jogador2_especial == False and cont_jogadas % 2 == 0:
                        jogador2_especial, linhas_verif, lista_num, linhas, jogador_atual = jogadaespecial('Facil', linhas_verif, jogador2_especial, lista_num, linhas, jogador_atual)                                                
                        imprimir_tabuleiro(linhas)
                        

            

            save = int(input('''Deseja salvar o jogo?
[1] - Não
[2] - Sim
                                 
-> '''))        
                
            if save == 2:
                estado_atual = {
                "dificuldade " : 1,
                "jogador1_especial" : jogador1_especial,
                "jogador2_especial" : jogador2_especial,
                "linhas" : linhas,
                "lista_num" : lista_num,
                "linhas_verif" : linhas_verif,
                "posicoes_letra" : posicoes_letra,
                "posicoes_num" : posicoes_num,
                "jogador1_obj" : jogador1_obj,
                "jogador2_obj" : jogador2_obj,
                "jogador_atual" : jogador_atual,
                "jogo_especial" : jogo_especial,
                "cont_jogadas" : cont_jogadas,
                "triunfo_jogador1" : triunfo_jogador1,
                "triunfo_jogador2" : triunfo_jogador2,
                "jogador1" : jogador1,
                "jogador2" : jogador2
                 }
                    
                salvarjogo('save.json',estado_atual)

                
            jogada_letra = input('Conforme o tabuleiro apresentado, selecione a letra em que deseja posicionar a sua jogada: ')
            jogada_numero = input('Conforme o tabuleiro apresentado, selecione o número em que deseja posicionar a sua jogada: ')
            
            if jogada_letra in posicoes_letra and jogada_numero in posicoes_num:
                num = int(input('Digite o número que deseja jogar: '))

                if num not in lista_num or str(linhas_verif[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]]).isdigit():
                    print('Resultado invalido')
                    cont_jogadas -= 1
                
                else:
                    jogador_atual = 'jogador1' if cont_jogadas % 2 != 0 else 'jogador2'
                    linhas_verif[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = num
                    linhas[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = jogadacolorida(num, jogador_atual)                    
                    lista_num.remove(num)

                    triunfo_jogador1 = verifvencedor('Facil', linhas_verif, jogador1_obj, triunfo_jogador1)
                    triunfo_jogador2 = verifvencedor('Facil', linhas_verif, jogador2_obj, triunfo_jogador2)

                    if triunfo_jogador1 == True and triunfo_jogador2 == False:
                        print(f'O jogador {jogador1} Venceu')
                        atualizarpontuacao(jogador1["nome"], int(jogador1["pontuacao"]) + 1)
                        break

                    elif triunfo_jogador1 == False and triunfo_jogador2 == True:
                        print(f'O jogador {jogador2} Venceu')
                        atualizarpontuacao(jogador2["nome"], int(jogador2["pontuacao"]) + 1)
                        break

                    elif triunfo_jogador1 == True and triunfo_jogador2 == True:
                        
                        if cont_jogadas % 2 != 0:
                            print(f'O jogador {jogador1} Venceu')
                            atualizarpontuacao(jogador1["nome"], int(jogador1["pontuacao"]) + 1)
                            break

                        elif cont_jogadas % 2 == 0:
                             print(f'O jogador {jogador2} Venceu')
                             atualizarpontuacao(jogador2["nome"], int(jogador2["pontuacao"]) + 1)
                             break

                    elif triunfo_jogador1 == False and triunfo_jogador2 == False and len(lista_num) == 0: 
                        print('EMPATE')
                        break


                
                    
    elif modo_jogo == MEDIO:
        jogador1_especial = False
        jogador2_especial = False
        salvar = None

        input(f'Para ver o objetivo do {jogador1}, aperte em qualquer tecla: ')
        jogador1_obj = objetivojogador(jogador1)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        input(f'Para ver o objetivo do {jogador2}, aperte em qualquer tecla: ')
        jogador2_obj = objetivojogador(jogador2)
        input(f'Para seguir com o jogo, aperte em qualquer tecla: ')
        clear_terminal()

        lista_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        
        triunfo_jogador1 = False
        triunfo_jogador2 = False
        
        cont_jogadas = 0 

        linhas = [['a1', 'a2', 'a3', 'a4'],
                  ['b1', 'b2', 'b3', 'b4'],
                  ['c1', 'c4', 'c3', 'c4'],
                  ['d1', 'd2', 'd3', 'd4']]
        
        linhas_verif = [['a1', 'a2', 'a3', 'a4'],
                        ['b1', 'b2', 'b3', 'b4'],
                        ['c1', 'c4', 'c3', 'c4'],
                        ['d1', 'd2', 'd3', 'd4']]
        
        posicoes_letra = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        posicoes_num = {'1': 0, '2': 1, '3': 2, '4': 3}

        while len(lista_num) > 0:
            cont_jogadas += 1
            clear_terminal()
            print(lista_num)
            imprimir_tabuleiro(linhas)

            if cont_jogadas > 1: 

                if jogo_especial == True: 

                    if jogador1_especial == False and cont_jogadas % 2 != 0:
                        jogador1_especial, linhas_verif, lista_num, linhas, jogador_atual = jogadaespecial('Facil', linhas_verif, jogador1_especial, lista_num, linhas, jogador_atual)
                        imprimir_tabuleiro(linhas)

                    elif jogador2_especial == False and cont_jogadas % 2 == 0:
                        jogador2_especial, linhas_verif, lista_num, linhas, jogador_atual = jogadaespecial('Facil', linhas_verif, jogador2_especial, lista_num, linhas, jogador_atual)
                        imprimir_tabuleiro(linhas)

            save = int(input('''Deseja salvar o jogo?
[1] - Não
[2] - Sim
                                 
-> '''))        
                
            if save == 2:
                estado_atual = {
                "dificuldade" : 2,
                "jogador1_especial" : jogador1_especial,
                "jogador2_especial" : jogador2_especial,
                "linhas" : linhas,
                "lista_num" : lista_num,
                "linhas_verif" : linhas_verif,
                "posicoes_letra" : posicoes_letra,
                "posicoes_num" : posicoes_num,
                "jogador1_obj" : jogador1_obj,
                "jogador2_obj" : jogador2_obj,
                "jogador_atual" : jogador_atual,
                "jogo_especial" : jogo_especial,
                "cont_jogadas" : cont_jogadas,
                "triunfo_jogador1" : triunfo_jogador1,
                "triunfo_jogador2" : triunfo_jogador2,
                "jogador1" : jogador1,
                "jogador2" : jogador2
                 }
                    
                salvarjogo('save.json',estado_atual)
    

            jogada_letra = input('Conforme o tabuleiro apresentado, selecione a letra em que deseja posicionar a sua jogada: ')
            jogada_numero = input('Conforme o tabuleiro apresentado, selecione o número em que deseja posicionar a sua jogada: ')
            
            if jogada_letra in posicoes_letra and jogada_numero in posicoes_num:
                num = int(input('Digite o número que deseja jogar: '))

                if num not in lista_num or str(linhas_verif[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]]).isdigit():
                    print('Resultado invalido')
                    cont_jogadas -= 1

                else:
                    jogador_atual = 'jogador1' if cont_jogadas % 2 != 0 else 'jogador2'
                    linhas_verif[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = num
                    linhas[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = jogadacolorida(num, jogador_atual) 
                    lista_num.remove(num)

                    triunfo_jogador1 = verifvencedor('Medio', linhas_verif, jogador1_obj, triunfo_jogador1)
                    triunfo_jogador2 = verifvencedor('Medio', linhas_verif, jogador2_obj, triunfo_jogador2)

                    if triunfo_jogador1 == True and triunfo_jogador2 == False:
                        print(f'O jogador {jogador1} Venceu')
                        atualizarpontuacao(jogador1["nome"], int(jogador1["pontuacao"]) + 2)
                        break

                    elif triunfo_jogador1 == False and triunfo_jogador2 == True:
                        print(f'O jogador {jogador2} Venceu')
                        atualizarpontuacao(jogador2["nome"], int(jogador2["pontuacao"]) + 2)
                        break

                    elif triunfo_jogador1 == True and triunfo_jogador2 == True:
                        
                        if cont_jogadas % 2 != 0:
                            print(f'O jogador {jogador1} Venceu')
                            atualizarpontuacao(jogador1["nome"], int(jogador1["pontuacao"]) + 2)
                            break

                        elif cont_jogadas % 2 == 0:
                             print(f'O jogador {jogador2} Venceu')
                             atualizarpontuacao(jogador2["nome"], int(jogador2["pontuacao"]) + 2)
                             break

                    elif triunfo_jogador1 == False and triunfo_jogador2 == False and len(lista_num) == 0: 
                        print('EMPATE')
                        break


                    elif triunfo_jogador1 == False and triunfo_jogador2 == False and len(lista_num) == 0: 
                        print('EMPATE')
                        break

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

        lista_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        
        triunfo_jogador1 = False
        triunfo_jogador2 = False
        
        cont_jogadas = 0

        linhas = [['a1', 'a2', 'a3', 'a4', 'a5'],
                  ['b1', 'b2', 'b3', 'b4', 'b5'],
                  ['c1', 'c2', 'c3', 'c4', 'c5'],
                  ['d1', 'd2', 'd3', 'd4', 'd5'],
                  ['e1', 'e2', 'e3', 'e4', 'e5']]
        
        linhas_verif = [['a1', 'a2', 'a3', 'a4', 'a5'],
                        ['b1', 'b2', 'b3', 'b4', 'b5'],
                        ['c1', 'c2', 'c3', 'c4', 'c5'],
                        ['d1', 'd2', 'd3', 'd4', 'd5'],
                        ['e1', 'e2', 'e3', 'e4', 'e5']]
        
        posicoes_letra = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e' : 4}
        posicoes_num = {'1': 0, '2': 1, '3': 2, '4': 3, '5' : 4}

        while len(lista_num) > 0:
            cont_jogadas += 1
            clear_terminal()
            print(lista_num)
            imprimir_tabuleiro(linhas)

            if cont_jogadas > 1: 

                if jogo_especial == True: 

                    if jogador1_especial == False and cont_jogadas % 2 != 0:
                        jogador1_especial, linhas_verif, lista_num, linhas, jogador_atual = jogadaespecial('Facil', linhas_verif, jogador1_especial, lista_num, linhas, jogador_atual)                        
                        imprimir_tabuleiro(linhas)

                    elif jogador2_especial == False and cont_jogadas % 2 == 0:
                        jogador2_especial, linhas_verif, lista_num, linhas, jogador_atual = jogadaespecial('Facil', linhas_verif, jogador2_especial, lista_num, linhas, jogador_atual)
                        imprimir_tabuleiro(linhas)

            save = int(input('''Deseja salvar o jogo?
[1] - Não
[2] - Sim
                                 
-> '''))        
                
            if save == 2:
                estado_atual = {
                "dificuldade" : 3,
                "jogador1_especial" : jogador1_especial,
                "jogador2_especial" : jogador2_especial,
                "linhas" : linhas,
                "lista_num" : lista_num,
                "linhas_verif" : linhas_verif,
                "posicoes_letra" : posicoes_letra,
                "posicoes_num" : posicoes_num,
                "jogador1_obj" : jogador1_obj,
                "jogador2_obj" : jogador2_obj,
                "jogador_atual" : jogador_atual,
                "jogo_especial" : jogo_especial,
                "cont_jogadas" : cont_jogadas,
                "triunfo_jogador1" : triunfo_jogador1,
                "triunfo_jogador2" : triunfo_jogador2,
                "jogador1" : jogador1,
                "jogador2" : jogador2
                 }
                    
                salvarjogo('save.json',estado_atual)


            jogada_letra = input('Conforme o tabuleiro apresentado, selecione a letra em que deseja posicionar a sua jogada: ')
            jogada_numero = input('Conforme o tabuleiro apresentado, selecione o número em que deseja posicionar a sua jogada: ')
            
            if jogada_letra in posicoes_letra and jogada_numero in posicoes_num:
                num = int(input('Digite o número que deseja jogar: '))

                if num not in lista_num or str(linhas_verif[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]]).isdigit():
                    print('Resultado invalido')
                    cont_jogadas -= 1

                else:
                    jogador_atual = 'jogador1' if cont_jogadas % 2 != 0 else 'jogador2'
                    linhas_verif[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = num
                    linhas[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = jogadacolorida(num, jogador_atual) 
                    lista_num.remove(num)

                    triunfo_jogador1 = verifvencedor('Dificil', linhas_verif, jogador1_obj, triunfo_jogador1)
                    triunfo_jogador2 = verifvencedor('Dificil', linhas_verif, jogador2_obj, triunfo_jogador2)

                    if triunfo_jogador1 == True and triunfo_jogador2 == False:
                        print(f'O jogador {jogador1} Venceu')
                        atualizarpontuacao(jogador1["nome"], int(jogador1["pontuacao"]) + 3)
                        break

                    elif triunfo_jogador1 == False and triunfo_jogador2 == True:
                        print(f'O jogador {jogador2} Venceu')
                        atualizarpontuacao(jogador2["nome"], int(jogador2["pontuacao"]) + 3)
                        break

                    elif triunfo_jogador1 == True and triunfo_jogador2 == True:
                        
                        if cont_jogadas % 2 != 0:
                            print(f'O jogador {jogador1} Venceu')
                            atualizarpontuacao(jogador1["nome"], int(jogador1["pontuacao"]) + 3)
                            break

                        elif cont_jogadas % 2 == 0:
                             print(f'O jogador {jogador2} Venceu')
                             atualizarpontuacao(jogador2["nome"], int(jogador2["pontuacao"]) + 3)
                             break

                    elif triunfo_jogador1 == False and triunfo_jogador2 == False and len(lista_num) == 0: 
                        print('EMPATE')
                        break


                    elif triunfo_jogador1 == False and triunfo_jogador2 == False and len(lista_num) == 0: 
                        print('EMPATE')
                        break

    salvar_ranking("ranking.json")

    return linhas


def imprimir_tabuleiro(tabuleiro):
    tabuleiro_formatado = tabulate(tabuleiro, tablefmt='grid')
    print(tabuleiro_formatado)


def objetivojogador(nom_jogador):
    objetivos = ['Sequência Ascendente', 'Sequência Descendente', 'Sequência Pares', 'Sequência Ímpares']
    jogador = objetivos[randint(0, 3)]
    print(f'{nom_jogador}, o seu objetivo é... {jogador}')
    return jogador


# variáveis e constantes que auxiliam nas seleções do menu 

# Menu inicial 
menu_inicial = ''
INICIAR_JOGO = '1'
CARREGARJOGO = '2'
VERIF_RANKING = '3'
SAIR = '4'
OPC_INICIAL = [INICIAR_JOGO, CARREGARJOGO, VERIF_RANKING, SAIR]

# Especial
menu_especial = ''
SEM_ESPECIAL = '1'
COM_ESPECIAL = '2'
OPC_ESPECIAL = [SEM_ESPECIAL, COM_ESPECIAL]
jogo_especial = None

# Menu de jogos
modo_jogo = ''
FACIL = '1'
MEDIO = '2'
DIFICIL = '3'
MODOS = {FACIL, MEDIO, DIFICIL} 

# Estabelecimento de um ranking
ranking = []

# Código principal 
menu_inicial = input('''SEJA BEM VINDO(A) AO TABULEIRO DE NÚMEROS
                   
1 - INICIAR UM NOVO JOGO
2 - CARREGAR JOGO
3 - VER RANKING
4 - SAIR
                   
''')

menu_inicial = verif_opc(menu_inicial, OPC_INICIAL)

if menu_inicial == INICIAR_JOGO:
    print('Digite os seus nomes...')
    jogador1 = input('Jogador 1: ')
    jogador2 = input('Jogador 2: ')

    adicionarjogador(jogador1, 0, ranking)
    adicionarjogador(jogador2, 0, ranking)

    menu_especial = input('''
---- Escolha se quer a jogada especial ----
                          
1 - Sem Especial
2 - Com Especial
                          
''')
    
    menu_especial = verif_opc(menu_especial, OPC_ESPECIAL)

    if menu_especial == COM_ESPECIAL:
        jogo_especial = True

    else:
        jogo_especial = False

    modo_jogo = input('''
---- Escolha o seu modo de jogo ---- 

1 - 3x3 (Fácil)
2 - 4x4 (Médio)
3 - 5x5 (Difícil)
                      
''')
    
    modo_jogo = verif_opc(modo_jogo, MODOS)

    lista_jogo = gerarjogo(modo_jogo)

    imprimir_tabuleiro(lista_jogo)

if menu_inicial == CARREGARJOGO:
    estado_jogo = carregarjogo('save.json')

    dificuldade = estado_jogo["dificuldade"]
    jogador1_especial = estado_jogo["jogador1_especial"]
    jogador2_especial = estado_jogo["jogador2_especial"]
    linhas = estado_jogo["linhas"]
    lista_num = estado_jogo["lista_num"]
    linhas_verif = estado_jogo["linhas_verif"]
    posicoes_letra = estado_jogo["posicoes_letra"]
    posicoes_num = estado_jogo["posicoes_num"]
    jogador1_obj = estado_jogo["jogador1_obj"]
    jogador2_obj = estado_jogo["jogador2_obj"]
    jogador_atual = estado_jogo["jogador_atual"]
    jogo_especial = estado_jogo["jogo_especial"]
    cont_jogadas = estado_jogo["cont_jogadas"] - 1
    triunfo_jogador1 = estado_jogo["triunfo_jogador1"]
    triunfo_jogador2 = estado_jogo["triunfo_jogador2"]
    jogador1 = estado_jogo["jogador1"]
    jogador2 = estado_jogo["jogador2"]

    while len(lista_num) > 0:
            cont_jogadas += 1
            clear_terminal()
            print(lista_num)
            imprimir_tabuleiro(linhas)

            if cont_jogadas > 1: 
                if jogo_especial == True: 

                    if jogador1_especial == False and cont_jogadas % 2 != 0:
                        jogador1_especial, linhas_verif, lista_num, linhas, jogador_atual = jogadaespecial('Facil', linhas_verif, jogador1_especial, lista_num, linhas, jogador_atual)                        
                        imprimir_tabuleiro(linhas)

                    elif jogador2_especial == False and cont_jogadas % 2 == 0:
                        jogador2_especial, linhas_verif, lista_num, linhas, jogador_atual = jogadaespecial('Facil', linhas_verif, jogador2_especial, lista_num, linhas, jogador_atual)                                                
                        imprimir_tabuleiro(linhas)
                        

            

            save = int(input('''Deseja salvar o jogo?
[1] - Não
[2] - Sim
                                 
-> '''))        
                
            if save == 2:
                estado_atual = {
                "dificuldade" : dificuldade,
                "jogador1_especial" : jogador1_especial,
                "jogador2_especial" : jogador2_especial,
                "linhas" : linhas,
                "lista_num" : lista_num,
                "linhas_verif" : linhas_verif,
                "posicoes_letra" : posicoes_letra,
                "posicoes_num" : posicoes_num,
                "jogador1_obj" : jogador1_obj,
                "jogador2_obj" : jogador2_obj,
                "jogador_atual" : jogador_atual,
                "jogo_especial" : jogo_especial,
                "cont_jogadas" : cont_jogadas,
                "triunfo_jogador1" : triunfo_jogador1,
                "triunfo_jogador2" : triunfo_jogador2,
                "jogador1" : jogador1,
                "jogador2" : jogador2
                 }
                    
                salvarjogo('save.json',estado_atual)

                
            jogada_letra = input('Conforme o tabuleiro apresentado, selecione a letra em que deseja posicionar a sua jogada: ')
            jogada_numero = input('Conforme o tabuleiro apresentado, selecione o número em que deseja posicionar a sua jogada: ')
            
            if jogada_letra in posicoes_letra and jogada_numero in posicoes_num:
                num = int(input('Digite o número que deseja jogar: '))

                if num not in lista_num or str(linhas_verif[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]]).isdigit():
                    print('Resultado invalido')
                    cont_jogadas -= 1
                
                else:
                    jogador_atual = 'jogador1' if cont_jogadas % 2 != 0 else 'jogador2'
                    linhas_verif[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = num
                    linhas[posicoes_letra[jogada_letra]][posicoes_num[jogada_numero]] = jogadacolorida(num, jogador_atual)                    
                    lista_num.remove(num)

                    triunfo_jogador1 = verifvencedor('Facil', linhas_verif, jogador1_obj, triunfo_jogador1)
                    triunfo_jogador2 = verifvencedor('Facil', linhas_verif, jogador2_obj, triunfo_jogador2)

                    if triunfo_jogador1 == True and triunfo_jogador2 == False:
                        print(f'O jogador {jogador1} Venceu')
                        atualizarpontuacao(jogador1["nome"], int(jogador1["pontuacao"]) + dificuldade)
                        break

                    elif triunfo_jogador1 == False and triunfo_jogador2 == True:
                        print(f'O jogador {jogador2} Venceu')
                        atualizarpontuacao(jogador2["nome"], int(jogador2["pontuacao"]) + dificuldade)
                        break

                    elif triunfo_jogador1 == True and triunfo_jogador2 == True:
                        
                        if cont_jogadas % 2 != 0:
                            print(f'O jogador {jogador1} Venceu')
                            atualizarpontuacao(jogador1["nome"], int(jogador1["pontuacao"]) + dificuldade)
                            break

                        elif cont_jogadas % 2 == 0:
                             print(f'O jogador {jogador2} Venceu')
                             atualizarpontuacao(jogador2["nome"], int(jogador2["pontuacao"]) + dificuldade)
                             break

                    elif triunfo_jogador1 == False and triunfo_jogador2 == False and len(lista_num) == 0: 
                        print('EMPATE')
                        break

    salvar_ranking("rankin.json")

elif menu_inicial == VERIF_RANKING: 
    carregar_ranking("ranking.json")

elif menu_inicial == SAIR:
    print("ADIOS")