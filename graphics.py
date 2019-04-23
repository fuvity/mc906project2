from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from math import sqrt, ceil

def getChild(A, B):
    #return (A[0], B[1])
    return ( (A[0]+B[0])//2, (A[1]+B[1])//2 )

# Pegando parametros
heightmap_size = 1200 #int(input('Tamanho do mapa:'))
max_iterations = 1000 #int(input('Numero maximo de iterações:))
pop_size = 100#int(input('Tamanho da População: '))
fittest_selection = 40#int(input('Quantos se reproduzirão por geração: '))
mutation_chance = 1#int(input('Chance de Mutação(%): '))
crossover_por_geracao = 10#int(input('Quantos crossover por geracao(%): '))

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
for _ in range(pop_size):
    children.append((np.random.randint(heightmap_size), np.random.randint(heightmap_size)))
ax = plt.figure()
plt.title('Primeira geração')
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
for itt in range(max_iterations):
    # Survival of the fittest
    z_values = []
    [z_values.append(Z[k[0]][k[1]]) for k in children]
    soma = sum(z_values)
    zval = np.array(z_values)
    zval /= soma
    idx = np.random.choice(len(children), size=fittest_selection, p=zval)
    fittest = np.array(children)[idx]
    z_values_fittest = np.array(z_values)[idx]

    index_of_fittest = np.where(z_values_fittest == np.amax(z_values_fittest))
    fitboy = fittest[index_of_fittest[0]][0]
    maxfit = z_values_fittest[index_of_fittest[0]][0]
    History.append([fitboy[0], fitboy[1], maxfit])

    # Gerando novas criancas
    children = []
    [children.append(fitboy) for fitboy in fittest] #fittest vai direto pra prox geracao
    for _ in range(crossover_por_geracao): # quem faz crossover mistura os pais
        children.append(getChild(fittest[np.random.randint(fittest_selection)], fittest[np.random.randint(fittest_selection)]))
    for i in range(len(children)): # mutacao
        if np.random.randint(100) < mutation_chance:
            child = children.pop(i)
            children.append((child[1], child[0]))
    for _ in range(pop_size-len(children)): # completa ate pop_size
        children.append((np.random.randint(heightmap_size), np.random.randint(heightmap_size)))
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
contadorr = 0
for fitboy in History:
    childrenx.append(fitboy[0])
    childreny.append(fitboy[1])
    contador.append(contadorr)
    print(fitboy[2])
    contadorr += 5
marker_size = 10
plt.scatter(childrenx, childreny, marker_size, c=contador, cmap=cm.coolwarm)
plt.show()
