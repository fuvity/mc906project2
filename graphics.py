from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from math import sqrt, ceil

def getChild(A, B):
    #return (A[0], B[1])
    x = (A[0]+B[0])//2
    y = (A[1]+B[1])//2
    z = Z[x][y]
    return (x, y, z) #Melhores formas de gerar os filhos???? Duvida!!

# Pegando parametros
heightmap_size = 9000 #int(input('Tamanho do mapa:'))
max_iterations = 1000 #int(input('Numero maximo de iterações:))
pop_size = 30#int(input('Tamanho da População: '))
fittest_selection = 40#int(input('Quantos se reproduzirão por geração: ')) QUAL O TAMANHO DA POPULAÇAO EXEMPLO????
fittest_selection = int(pop_size*fittest_selection/100)
mutation_chance = 5#int(input('Chance de Mutação(%): '))   CHANCE DE MUTAÇÃO BOA???
crossover_por_geracao = 50#int(input('Quantos crossover por geracao(%): '))
crossover_por_geracao = int(pop_size*crossover_por_geracao/100)

# Inventando um heightmap
X = np.arange(0, heightmap_size, 1)
Y = np.arange(0, heightmap_size, 1)
X, Y = np.meshgrid(X, Y)
Z = X/(heightmap_size/4) + Y/(heightmap_size/6) + np.sin(X/(heightmap_size/24)) + np.sin(Y/(heightmap_size/24)) + 1
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis,
                       linewidth=1, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.title('Heightmap gerado')
plt.show()

# GA
History = []
children = []
childrenx = []
childreny = []
for _ in range(pop_size):
    x = np.random.randint(heightmap_size)
    y = np.random.randint(heightmap_size)
    z = Z[x][y]
    childrenx.append(x)
    childreny.append(y)
    children.append((x, y, z))

ax = plt.figure()
plt.title('Primeira geração')
p = plt.imshow(Z, cmap=cm.viridis)
plt.colorbar(p)
marker_size = 10
plt.scatter(childrenx, childreny, marker_size, c='r')
plt.show()

for itt in range(max_iterations):
    # Survival of the fittest
    children = sorted(children, key=lambda x: x[2])
    fittest = children[fittest_selection:]
    childrencopy = children
    History.append(fittest[-1])

    # Gerando novas criancas
    children = []
    [children.append(fitboy) for fitboy in fittest] #fittest vai direto pra prox geracao
    for i in range(crossover_por_geracao): # quem faz crossover mistura os pais
        children.append(getChild(fittest[-i], fittest[-i-1]))
    for i in range(len(children)): # mutacao, modelo de mutaçao eh bom o suficiente??? Duvida
        if np.random.randint(100) < mutation_chance:
            child = children.pop(i)
            children.append((child[1], child[0], Z[child[1]][child[0]]))
    for i in range(pop_size-len(children)): # completa ate pop_size, DUVIDA completo com aleatorios mesmo ou usar parametros e probabilidade pra gerar
        children.append(childrencopy[i])
    if itt == max_iterations-1:
        ax = plt.figure()
        plt.title('Última geração')
        p = plt.imshow(Z, cmap=cm.viridis)
        plt.colorbar(p)
        childrenx = []
        childreny = []
        for child in children:
            childrenx.append(child[0])
            childreny.append(child[1])
        marker_size = 10
        plt.scatter(childrenx, childreny, marker_size, c='r')
        plt.show()

# Fazendo as figuras

ax = plt.figure()
plt.title('Coordenadas em Z do Heightmap')
p = plt.imshow(Z, cmap=cm.viridis)
plt.colorbar(p)
childrenx = []
childreny = []
contador = []
childrenz = []
contadorr = 0
contadorsingle = []
i = 0
for fitboy in History:
    childrenx.append(fitboy[0])
    childreny.append(fitboy[1])
    childrenz.append(fitboy[2])
    contador.append(contadorr)
    contadorsingle.append(i)
    i += 1
    contadorr += 5
marker_size = 10
plt.scatter(childrenx, childreny, marker_size, c=contador, cmap=cm.coolwarm)
plt.show()

plt.plot(contadorsingle[:30],childrenz[:30])
plt.show()
