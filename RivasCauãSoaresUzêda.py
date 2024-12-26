dici = {'Sequência ascendente': (- 1, + 1)}
linhas = [[5,3,1],
          [4,9,8],
          [9,9,10]]
        

def verifvencedor(dif, linhas,obj):
    dici = {'Sequência Ascendente': (-1,+1),
            'Sequência Descendente' : (+1,-1),
            'Sequência Pares' : (-2,+2),
            'Sequência Ímpares' : (-2,+2),
            }
    
    if dif == 'Facil':

        valor_obj = dici.get(obj)

        # Horizontal
        for cont in range(3):
            num = linhas[cont][1]

            if obj == 'Sequência Pares' or obj == 'Sequência Ímpares':

                if num % 2 == 0:
                    if linhas[cont][0] == num + 2 and linhas[cont][2] == num - 2:
                        print('Partida Finalizada!')

                if num % 2 != 0:
                    if linhas[cont][0] == num + 2 and linhas[cont][2] == num - 2:
                        print('Partida Finalizada!')

            if linhas[cont][0] == num + valor_obj[0] and linhas[cont][2] == num + valor_obj[1]:
                print('Partida Finalizada!')

verifvencedor('Facil',linhas,'Sequência Pares')
verifvencedor('Facil',linhas,'Sequência Ímpares')