import numpy as np, networkx as nx
from random import sample, randint, randrange
import matplotlib.pyplot as plt
import sys
'''N = int(input("количество вершин: "))
t1, t2 = int(input("t1 = ")), int(input("t2 = "))
Z, K = int(input("Z = ")), int(input("K = "))
PM = int(input("PM = "))
PK = int(input("PK = "))'''
sys.stdout.reconfigure(encoding='utf-8')
N = 11
t1 = 10
t2 = 30
PM = 80
PK = 80
Z = 100
K = 100

#START_VERTEX = int(input("стартовая вершина: "))
START_VERTEX = 4

#tril = np.tril(np.random.randint(t1, t2, size=(N, N)), -1)
#matrix  = tril + tril.T
matrix = np.array([[0, 28, 23, 29, 15, 23, 12, 11, 23, 11, 22], [28, 0, 18, 10, 15, 26, 21, 16, 16, 14, 12], [23, 18, 0, 11, 16, 13, 19, 25, 24, 11, 19], [29, 10, 11, 0, 22, 12, 19, 22, 25, 16, 19], [15, 15, 16, 22, 0, 19, 11, 21, 15, 16, 16], [23, 26, 13, 12, 19, 0, 25, 26, 21, 25, 25], [12, 21, 19, 19, 11, 25, 0, 20, 26, 11, 23], [11, 16, 25, 22, 21, 26, 20, 0, 15, 23, 16], [23, 16, 24, 25, 15, 21, 26, 15, 0, 27, 11], [11, 14, 11, 16, 16, 25, 11, 23, 27, 0, 27], [22, 12, 19, 19, 16, 25, 23, 16, 11, 27, 0]])
print(matrix)


def find_path(matrix, start):
    temp = matrix.copy()
    mx, my = temp.shape
    istart = start
    path = [istart]

    end = False
    visited = np.zeros(mx, dtype=bool)  # Initialize an array to track visited vertices
    visited[istart] = True  # Mark the starting vertex as visited
    while not end:
        inew = np.where((temp[istart] != 0) & (~visited))[0]  # Find unvisited adjacent vertices
        if inew.size == 0:  # If there are no unvisited adjacent vertices, end the loop
            break
        inew = np.random.choice(inew)  # Choose the first unvisited adjacent vertex
        temp[istart, inew] = 0
        temp[inew, istart] = 0
        path.append(inew)
        istart = inew
        visited[inew] = True  # Mark the new vertex as visited
        end = np.all(temp[istart] == 0)
    path.append(start)
    #print(path)
    return path

def count_sum(matrix, path):
    sum = 0
    for i in range(len(path) - 1):
        row = path[i]
        column = path[i+1]
        sum += matrix[row][column]
    return (path, sum)


def CROSSOVER(L1, L2):
    global N, START_VERTEX, PM
    split = randint(2, N-1)
    p = L1[0:split]
    if type(p) != list:
        p = p.tolist()
    print(p, split)
    for i in range(split, len(L2)):
        if L2[i] not in p:
            p.append(L2[i])
        else:
            p.append(-1)
    p[-1] = START_VERTEX
    for i in range(len(p)):
        if p[i] == -1:
            for j in range(0, N):
                if j not in p:
                    p[i] = j
                    break
    p = np.array(p)
    print(p)
    r = randrange(100)
    if r < PM and PM != 100:
        print(f"вероятность оператора мутации = {r} {PM}, мутация не произошла")
        return p
    else:
        print(f"вероятность оператора мутации = {r} {PM}, осуществление процесса мутации...")
        p = MUTATE(p)
        return p

def MUTATE(p):
    global N
    inds = sample(range(1, N), 2)
    print(inds)
    P = np.array(p)
    P[inds[0]], P[inds[1]] = P[inds[1]], P[inds[0]]
    print(P)
    return P

gen = []
for i in range(K):
    g = find_path(matrix, START_VERTEX)
    gen.append(count_sum(matrix, g))
print(gen)
COUNTER = 1
BEST = min([specie[1] for specie in gen])
print("лучшая приспособляемость: ", BEST)

GENERATIONS = {0 : gen}
dictid = 0

while COUNTER != Z:
    print("\n=====================================")
    print(f"\nтекущее поколение: {gen}")
    print(f"лучшая приспобляемость: {BEST}")
    print(f"повторений: {COUNTER}")
    print("\n=====================================\n")
    nextgen = []
    for i in range(len(gen)): #для номера особи из поколения
        print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print(f"текущая особь: {gen[i]}, ({i})")
        r = randrange(100)
        if r < PK and PK != 100:
            print(f"вероятность оператора кроссовера = {r} {PK}, особь переходит в следующее поколение")
            nextgen.append(gen[i])

        else:
            print(f"вероятность оператора кроссовера = {r} {PK}, выбор партнера...")
            partner_id = i
            while partner_id == i:
                partner_id = randint(0, (len(gen)-1))
            print(f"ВЫБРАН ПАРТНЕР: {gen[partner_id]}, ({partner_id})")

            Pdna1 = CROSSOVER(gen[i][0], gen[partner_id][0])
            print(f"ПОЛУЧЕН ПОТОМОК {Pdna1}")
            Pdna2 = CROSSOVER(gen[partner_id][0], gen[i][0])
            print(f"ПОЛУЧЕН ПОТОМОК {Pdna2}")
            P1 = count_sum(matrix, Pdna1)
            P2 = count_sum(matrix, Pdna2)

            contest = [gen[i][1], P1[1], P2[1]]
            win = min(contest)
            win_id = contest.index(win)
            print(f"кандидаты в следующее поколение на {i} место: \n- базовый родитель: {gen[i]}\n- потомок1: {P1}\n- потомок2: {P2}")

            if win_id == 0:
                nextgen.append(gen[i])
                print(f"в следующее поколение на {i} место отправляется базовый родитель {gen[i]}")
            elif win_id == 1:
                nextgen.append(P1)
                print(f"в следующее поколение на {i} место отправляется потомок 1 {P1}")
            elif win_id == 2:
                nextgen.append(P2)
                print(f"в следующее поколение на {i} место отправляется потомок 2 {P2}")

    newBEST = min([specie[1] for specie in nextgen])
    if newBEST == BEST:
        COUNTER += 1
    elif newBEST < BEST:
        BEST = newBEST
        COUNTER = 1

    dictid += 1
    GENERATIONS[dictid] = nextgen
    gen = nextgen
print(GENERATIONS)
PATH = next(item for item in (list(GENERATIONS.values()))[-1] if item[1] == BEST)
print("\n=====================================")
print(f"ЛУЧШИЙ ПУТЬ: {PATH}")
print(f"КОЛИЧЕСТВО ПОВТОРОВ: {COUNTER}")
print(f"КОЛИЧЕСТВО ПОЛУЧЕННЫХ ПОКОЛЕНИЙ: {len(list(GENERATIONS.keys()))}")
for key in GENERATIONS:
    print(key, GENERATIONS[key])
print("=====================================\n")

if type(PATH[0]) != list:
    path = PATH[0].tolist()
else:
    path = PATH[0]
input()
edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
G = nx.complete_graph(N)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=300, node_color="green", font_size=12)
nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=3)  # Draw the specific path in red
plt.show()