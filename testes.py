class Aluno:
    def __init__(self, nome, CPF, sexo, idade):
        self.nome = nome
        self.CPF = CPF
        self.sexo = sexo
        self.idade = idade

def armazenar_alunos():
    alunos = {}
    for i in range(3):
        nome = input(f"Digite o nome do aluno {i+1}: ")
        CPF = input(f"Digite o CPF do aluno {i+1}: ")
        sexo = input(f"Digite o sexo do aluno {i+1} (M/F): ")
        idade = int(input(f"Digite a idade do aluno {i+1}: "))
        aluno = Aluno(nome, CPF, sexo, idade)
        alunos[CPF] = aluno
    return alunos

def calcular_media_idade_masculina(alunos):
    total_idade = 0
    count_masculino = 0
    for aluno in alunos.values():
        if aluno.sexo.upper() == 'M':
            total_idade += aluno.idade
            count_masculino += 1
    if count_masculino == 0:
        return 0  # Evita divisão por zero
    return total_idade / count_masculino

# Armazenar alunos em um dicionário
alunos = armazenar_alunos()
for i in alunos.values():
    print(i.nome)

# Calcular e mostrar a média de idade dos alunos do sexo masculino
media_idade_masculina = calcular_media_idade_masculina(alunos)
print(f"A média de idade dos alunos do sexo masculino é: {media_idade_masculina:.2f}")
