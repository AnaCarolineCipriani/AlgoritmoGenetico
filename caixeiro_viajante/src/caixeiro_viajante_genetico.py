import random
import numpy as np
import math
import matplotlib.pyplot as plt

individuos = []
aptidao = []
primeiros_individuos = []

def popula_individuos():
    global individuos
    global primeiros_individuos

    for _ in range(20):
        cromossomos = []
        cidades = list(range(1, 21))

        # escolhe cidades de modo aleatório entre 1 e 20
        for _ in range(20):
            gene = random.choice(cidades)
            cidades.remove(gene)
            cromossomos.append(gene)

        # adiciona a primeira cidade ao final, pois o viajante volta para ela ao final do percurso
        cromossomos.append(cromossomos[0])
        individuos.append(cromossomos)
        
        # guarda a primeira população de indivíduos 
        primeiros_individuos.append(cromossomos)

def calcula_aptidao(x, y):
    global aptidao

    # limpar a lista a cada iteração
    aptidao.clear()
    
    for i in range(20):
        distancia_individuos = []
        total_distancia_cromossomo = 0
        for j in range(20):

            # armazena o índice de duas cidades, sempre -1 pois na lista de x e y não existe índice 20
            indice_cidade1 = individuos[i][j] - 1
            indice_cidade2 = individuos[i][j + 1] - 1  # cidade ao lado da cidade1

            distancia = calcula_distancia_euclidiana(x[indice_cidade1], x[indice_cidade2], y[indice_cidade1], y[indice_cidade2])
            distancia_individuos.append(distancia)

        total_distancia_cromossomo = sum(distancia_individuos)
        aptidao.append(total_distancia_cromossomo)

def ordena_individuos_por_aptidao():
    global individuos
    global aptidao

    # ordena e retorna os índices ordenados
    indices_ordenados = np.argsort(aptidao)
    # transforma o array do numpy para lista
    indices_ordenados = indices_ordenados.flatten().tolist()

    # reorganiza as listas conforme os índices ordenados
    aptidao = [aptidao[i] for i in indices_ordenados]
    individuos = [individuos[i] for i in indices_ordenados]

def reduz_metade_individuos():
    global individuos

    # irá remover os indivíduos do índice 19 ao 10
    for linha in range(19, 9, -1):
        individuos.pop(linha)

def seleciona_individuos(roleta):
    selecao = []
    
    # seleciona 10 indivíudos aleatoriamente utilizando a roleta
    while (len(selecao) < 10):
        individuo = random.choice(roleta)
        
        # verificar se precisa tirar o número escolhido da roleta pra não ser selecionado mais de uma vez
       # while individuo in roleta:
            #roleta.remove(individuo)
            
        # adiciona o índice do indivíduo
        selecao.append(individuo)

    return selecao

def get_pais_selecionados(selecao):
    global individuos

    pais = []
    
    # acessa a cidade através do índice da lista de selecao
    for individuo in selecao:
        pais.append(individuos[individuo])
    return pais

def cria_descendentes(pais):
    global individuos

    # de par em par, são criados dois descendentes
    for pai in range(0, 10, 2):
        local_aleatorio = random.randint(0, 19)

        filho1 = pais[pai].copy()
        filho2 = pais[pai + 1].copy()
        
        # remove o índice 20 que é a primeira cidade visitada, já que serão trocadas as posições
        filho1.pop(20)
        filho2.pop(20)

        filho1, filho2 = do_cycle(filho1, filho2, local_aleatorio)

        # adiciona a primeira cidade ao final
        filho1.append(filho1[0])
        filho2.append(filho2[0])

        individuos.append(filho1)
        individuos.append(filho2)


def do_cycle(filho1, filho2, posicao):
    valor1 = filho1[posicao]

    # troca os valores de lugar conforme a posição
    filho1[posicao] = filho2[posicao]
    filho2[posicao] = valor1

    # em quanto existirem posições duplicadas, serão trocadas as posições
    posicao_duplicada = busca_posicao_duplicada(filho1, posicao)
    if (posicao_duplicada is not None):
        filho1, filho2 = do_cycle(filho1, filho2, posicao_duplicada)
    else:
        posicao_duplicada = busca_posicao_duplicada(filho2, posicao)
        if (posicao_duplicada is not None):
            filho1, filho2 = do_cycle(filho1, filho2, posicao_duplicada)

    return filho1, filho2

def carrega_matriz_de_posicoes(): 
    cidades = np.loadtxt('cidades.mat')
    x = cidades[0]
    y = cidades[1]
    
    return x, y

def cria_roleta():
    roleta = []
    
    # adiciona 10 vezes o índice 0, 9 vezes o 1.. até 1 vez para o índice 9
    for i in range(10):
        for _ in range(10 - i):
            roleta.append(i)
    return roleta

def calcula_distancia_euclidiana(x1, x2, y1, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def busca_posicao_duplicada(filho, posicao):
    posicao_duplicada = None
    
    valor_posicao = filho[posicao]
    
    # retorna o primeiro índice de um número duplicado se existir
    for indice in range(len(filho)):
        valor = filho[indice]
        
        # se valores forem iguais e posições diferentes, há duplicação
        if (valor == valor_posicao and indice != posicao):
            posicao_duplicada = indice
            break
    return posicao_duplicada

def plotar_melhor_caminho(x, y):
    global aptidao
    global individuos

    # melhor caminho é a primeira posição da lista de indivíduos
    cromossomo = individuos[0]

    eixo_x = []
    eixo_y = []
    
    # acessa a lista de cidades, acessa a matriz de posições conforme a cidade e adiciona aos respectivos eixos
    for gene in cromossomo:
        indice_cidade = gene - 1
        posicao_cidade_x = x[indice_cidade]
        posicao_cidade_y = y[indice_cidade]

        eixo_x.append(posicao_cidade_x)
        eixo_y.append(posicao_cidade_y)

    # cria as ligações entre as cidades
    plt.plot(eixo_x, eixo_y, color="cadetblue", linestyle="solid", linewidth=0.8)
    
    # configurações do gráfico
    ax = plt.subplot()
    # título do gráfico  
    ax.set_title("Melhor caminho entre as cidades", fontsize = 12)
    # cria pontos para mostrar a localização das cidades
    ax.scatter(eixo_x, eixo_y, s = 15, color = "navy", marker = "H")
    # mostra o número das cidades no gráfico com a cor índigo
    for indice in cromossomo:
        ax.annotate(indice, (eixo_x[indice], eixo_y[indice]), color="indigo")
      
    plt.show()

def main():
    popula_individuos()
    x, y = carrega_matriz_de_posicoes()
    
    for _ in range(10000):
        roleta = cria_roleta()
        calcula_aptidao(x, y)
        ordena_individuos_por_aptidao()
        reduz_metade_individuos()
        selecao = seleciona_individuos(roleta)
        pais = get_pais_selecionados(selecao)
        cria_descendentes(pais)

    print("Tamanho da População:", 20)
    
    print("População inicial:")
    for linha in primeiros_individuos:
        print(linha)
    
    print("População final:")
    for linha in individuos:
        print(linha)
        
    print("Número de cidades: ", 20)
    print("Melhor custo: ", aptidao[0])
    print("Melhor solução: ", individuos[0])
    plotar_melhor_caminho(x, y)

if __name__ == '__main__':
    main()