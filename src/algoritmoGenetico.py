import random
import csv 


#constantes
tabela_itens=[]
tabela_cidades=[]


def tabela (local):
    lista = []
    with open (local, encoding = 'utf-8') as itens:
        tabela = csv.reader(itens, delimiter=',')
        for l in tabela:
            lista.append(l)
    return lista 


def rota_inicial():
    rota = []
    lista = tabela('src/itens.csv')

    for _ in range(3):
        aleatorio = random.choice(lista)
        rota.append(aleatorio)
        lista.remove(aleatorio)
    
    return rota 


def fitness(rota):
    lucro = 0
    custo = 0
    peso = 0
    tempo_gasto = 0
    partida = rota[0]
    chegada = rota[len(rota)-1]

    tab = tabela_cidades

    #custo primeira e ultima viagem
    for l in tab:
        if (l[0] == 'Escondidos' and partida[4] in l):
            custo = custo + int(l[3])
            tempo_gasto = tempo_gasto + int(l[2])
        if (l[0] == 'Escondidos' and chegada[4] in l):
            custo = custo + int(l[3])
            tempo_gasto = tempo_gasto + int(l[2])

    #custo das viagens intermediarias 
    for i in range(len(rota)):
        lucro = lucro + int(rota[i][3])
        peso = peso + int(rota[i][1])
        tempo_gasto = tempo_gasto + int(rota[i][2])
        if (i<=len(rota)-2):
            for l in tab:
                if (rota[i][4] in l and rota[i+1][4] in l):
                    custo = custo + int(l[3])
                    tempo_gasto = tempo_gasto + int(l[2])
    
    #se passou do peso maximo ou do limite de horas 
    if (peso > 20 or tempo_gasto > 72):
        return -1
    else:
        return lucro - custo
                
    
def mutar(rota):
    nova_rota = list(rota)

    indice = random.randint(0, len(rota) - 1)
    aleatorio = random.choice(tabela_itens)
    
    if (aleatorio not in nova_rota):
        nova_rota[indice] = aleatorio
    else:
        index = nova_rota.index(aleatorio)
        indice = random.randint(0, len(rota) - 1)
        nova_rota[indice], nova_rota[index] = nova_rota[index], nova_rota[indice]

    if (fitness(nova_rota)<=fitness(rota)):
        nova_rota.append(random.choice(tabela_itens))
    
    if (fitness(nova_rota)==-1):
        nova_rota.pop()

    return nova_rota


def selecao(lista):
    nova_lista = sorted(lista, key=fitness, reverse=True)
    return nova_lista[0:10]


def crossover(populacao, mutada):
    populacao_crossover = []
    for ind1 in populacao:
        for ind2 in mutada:
            # geracao do cross_over
            i = random.randint(0, len(populacao[0]) - 1)
            if (ind1[0:i] not in ind2[i:]):
                populacao_crossover.append(ind1[0:i] + ind2[i:])
                populacao_crossover.append(ind2[0:i] + ind1[i:])
    return populacao_crossover


print('Iniciando...')
random.seed()

# população inicial
populacao = [rota_inicial() for _ in range(0,10)]
print('teste')
#gerar tabelas 
tabela_cidades = tabela('src/cidades.csv')
tabela_itens = tabela('src/itens.csv')

geracoes = 0
perdas = 0
ant = -1
while True:
    pop_mutada = [mutar(individuo) for individuo in populacao]
    pop_crossover = crossover(populacao, pop_mutada)

    populacao = selecao(populacao + pop_mutada + pop_crossover)
    
    geracoes += 1
    if geracoes % 50 == 0:
        print(fitness(populacao[0]), geracoes)

    # critério de parada
    if fitness(populacao[0]) > ant:
        ant = fitness(populacao[0])
        perdas = 0
    else:
        perdas+=1
    if perdas == 500:
        break
            
print('Finalizado!')