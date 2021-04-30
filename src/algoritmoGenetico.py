import random
import csv 


#tabelas
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
    lista = tabela('itens.csv')

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
        if (l[0] == 'Escondidos' and chegada[len(chegada)-1] in l):
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
        nova_rota.append(aleatorio)
    else:
        index = nova_rota.index(aleatorio)
        indice = random.randint(0, len(rota) - 1)
        nova_rota[indice], nova_rota[index] = nova_rota[index], nova_rota[indice]
    if (fitness(nova_rota)==-1):
        nova_rota.pop(random.randint(0, len(rota) - 1))
        random.shuffle(nova_rota)

    return nova_rota

def tragedia (pop_mutada):
    nova_lista = pop_mutada[0:2]
    pop_nova = [rota_inicial() for _ in range(0,18)]
    pop_nova = [mutar(individuo) for individuo in pop_nova]
    return nova_lista + pop_nova

def selecao(lista):
    nova_lista = sorted(lista, key=fitness, reverse=True)
    return nova_lista[0:20]

def crossover(populacao, mutada):
    populacao_crossover = []
    filho1 = []
    filho2 = []

    for ind1 in populacao:
        for ind2 in mutada:
            # geracao do cross_over
            i = random.randint(0, len(populacao[0]) - 1)
            filho1 = ind1[0:i]
            filho2 = [cidade for cidade in ind2 if cidade not in filho1]
            geracao = filho1+filho2[0:len(populacao[0])-i]
            populacao_crossover.append(geracao)
    return populacao_crossover

def resultado (rota):
    tab = tabela_cidades
    peso = 0
    tempo_gasto = 0
    partida = rota[0]
    chegada = rota[len(rota)-1]
    for l in tab:
        if (l[0] == 'Escondidos' and partida[4] in l):
            tempo_gasto = tempo_gasto + int(l[2])
        if (l[0] == 'Escondidos' and chegada[len(chegada)-1] in l):
            tempo_gasto = tempo_gasto + int(l[2])

    for i in range(len(rota)):
        peso = peso + int(rota[i][1])
        tempo_gasto = tempo_gasto + int(rota[i][2])
        if (i<=len(rota)-2):
            for l in tab:
                if (rota[i][4] in l and rota[i+1][4] in l):
                    tempo_gasto = tempo_gasto + int(l[2])
    return peso, tempo_gasto


print('Iniciando...')
random.seed()

# população inicial
populacao = [rota_inicial() for _ in range(0,40)]
#gerar tabelas 
tabela_cidades = tabela('cidades.csv')
tabela_itens = tabela('itens.csv')

geracoes = 0
perdas = 0
ant = -1
while True:
    pop_mutada = [mutar(individuo) for individuo in populacao]
    pop_crossover = crossover(populacao, pop_mutada)
    populacao = selecao(populacao + pop_mutada + pop_crossover)
    
    geracoes += 1
    if geracoes % 50 == 0:
        print('Fitness: '+ str(fitness(populacao[0]))+ ' Geração: '+ str(geracoes))

    # critério de parada
    if fitness(populacao[0]) > ant:
        ant = fitness(populacao[0])
        perdas = 0
    else:
        perdas+=1
    if (perdas == 500):
        print ('-------------------')
        print ('-    Tragédia     -')
        print ('-------------------')
        populacao = tragedia(populacao)
    if perdas == 1000:
        break

peso, tempo = resultado(populacao[0])  
print('\n------Resultado------')
populacao[0].insert(0,'Escondidos')
populacao[0].append('Escondidos')
print (populacao[0])
print('Tempo gasto: '+str(tempo)+' Horas'+' Peso total da mochila: '+ str(peso)+' Kg') 