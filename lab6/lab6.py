import numpy as np
import networkx as nx
from random import sample, randint
import matplotlib.pyplot as plt

def DA_WAY(ways, start_da_way, end = False):
    temp_ways = ways.copy()
    mx, my = temp_ways.shape
    new_start_da_way = start_da_way
    da_way_to_queen = [new_start_da_way]

    there_no_queen, there_no_queen[new_start_da_way] = np.zeros(mx, dtype=bool), True  
    while not end:
        new_da_way = np.where((temp_ways[new_start_da_way] != 0) & (~there_no_queen))[0]  
        if new_da_way.size == 0:  
            break
        new_da_way = np.random.choice(new_da_way) 
        temp_ways[new_start_da_way, new_da_way], temp_ways[new_da_way, new_start_da_way] = 0, 0
        da_way_to_queen.append(new_da_way)
        new_start_da_way = new_da_way
        there_no_queen[new_da_way] = True  
        end = np.all(temp_ways[new_start_da_way] == 0)
    da_way_to_queen.append(start_da_way)

    return da_way_to_queen

def sum_DA_WAY(ways, da_way):
    sum_da_way = 0
    for i in range(len(da_way) - 1):
        dar_way = da_way[i]
        dac_way = da_way[i+1]
        sum_da_way += ways[dar_way][dac_way]
    return (da_way, sum_da_way)


def DA_WAY_crossover(way1, way2):
    da_way_part = randint(2, N-1)
    p = way1[:da_way_part]
    if type(p) != list:
        p = p.tolist()
    for i in range(da_way_part, len(way2)):
        if way2[i] not in p:
            p.append(way2[i])
        else:
            p.append(-1)
    p[-1] = START_DA_WAY
    for i in range(len(p)):
        if p[i] == -1:
            for j in range(0, N):
                if j not in p:
                    p[i] = j
                    break
    p = np.array(p)
    return p

def DA_WAY_mutation(p):
    global N
    inds = sample(range(1, N), 2)
    P = np.array(p)
    P[inds[0]], P[inds[1]] = P[inds[1]], P[inds[0]]
    return P

def graf_for_DA_WAY(result):
    if type(result[0]) != list:
        da_way_to_queen = result[0].tolist()
    else:
        da_way_to_queen = result[0]
    edges = [(da_way_to_queen[i], da_way_to_queen[i + 1]) for i in range(len(da_way_to_queen) - 1)]
    graf = nx.complete_graph(N)
    position = nx.spring_layout(graf)
    nx.draw(graf, position, with_labels=True, node_size=200, node_color="red", font_size=6)
    nx.draw_networkx_edges(graf, position, edgelist=edges, edge_color='green', width=2)
    plt.show()

def main_func():
    generation = []
    for i in range(K):
        g = DA_WAY(ways_to_queen, START_DA_WAY)
        generation.append(sum_DA_WAY(ways_to_queen, g))

    all_generations = [generation]
    best_sum = min([i[1] for i in generation])
    repeat = 1

    f_mut = open(f"D:\\GitHub\\OsnoviResheniy\\mutation{res_num}.txt", 'w')
    while repeat != Z:
        f_mut.write(f"\nПоколение {len(all_generations)}:\n")
        next_generation = []
        for i in range(len(generation)):
            if randint(0, 100) < Pk:
                next_generation.append(generation[i])
            else:
                partner_id = i
                while partner_id == i:
                    partner_id = randint(0, (len(generation)-1))
                    
                f_mut.write("Родители:\n")
                f_mut.write(f"Родитель 1: {generation[i]}\n")
                f_mut.write(f"Родитель 2: {generation[partner_id]}\n")

                child1 = DA_WAY_crossover(generation[i][0], generation[partner_id][0])
                child2 = DA_WAY_crossover(generation[partner_id][0], generation[i][0])

                f_mut.write("Дети:\n")
                f_mut.write(f"Ребёнок 1: {(child1, sum_DA_WAY(ways_to_queen, child1))}\n")
                f_mut.write(f"Ребёнок 2: {(child2, sum_DA_WAY(ways_to_queen, child2))}\n")

                if randint(0, 100) < Pm:
                    child1_mut = DA_WAY_mutation(child1)
                    child2_mut = DA_WAY_mutation(child2)

                    f_mut.write("Дети после мутации:\n")
                    f_mut.write(f"Ребёнок 1: {(child1_mut, sum_DA_WAY(ways_to_queen, child1_mut))}\n")
                    f_mut.write(f"Ребёнок 2: {(child2_mut, sum_DA_WAY(ways_to_queen, child2_mut))}\n")

                    P1 = sum_DA_WAY(ways_to_queen, child1_mut)
                    P2 = sum_DA_WAY(ways_to_queen, child2_mut)
                else:
                    P1 = sum_DA_WAY(ways_to_queen, child1)
                    P2 = sum_DA_WAY(ways_to_queen, child2)

                contest = [generation[i][1], P1[1], P2[1]]
                win = min(contest)
                win_id = contest.index(win)

                if win_id == 0:
                    next_generation.append(generation[i])
                elif win_id == 1:
                    next_generation.append(P1)
                elif win_id == 2:
                    next_generation.append(P2)

        new_best_sum = min([i[1] for i in next_generation])
        if new_best_sum == best_sum:
            repeat += 1
        elif new_best_sum < best_sum:
            best_sum = new_best_sum
            repeat = 1

        all_generations.append(next_generation)
        generation = next_generation

    DA_WAY_TO_QUEEN = next(i for i in all_generations[-1] if i[1] == best_sum)
    print("\n-------------------------")
    print(f"Лучший результат: {best_sum}")
    print("-------------------------\n")
    with open(f"D:\\GitHub\\OsnoviResheniy\\result{res_num}.txt", 'w') as f:
        for i in range(len(all_generations)):
            f.write(f"{i+1} | {all_generations[i]}\n")
    return DA_WAY_TO_QUEEN

N = int(input("N = "))
T1 = int(input("Нижняя граница: "))
T2 = int(input("Верхняя граница: "))
Z = int(input("Z = "))
K = int(input("K = "))
Pm = int(input("Pm = "))
Pk = int(input("Pk = "))

res_num = 0

tril = np.tril(np.random.randint(T1, T2, size=(N, N)), -1)
ways_to_queen  = tril + tril.T
print(ways_to_queen)

START_DA_WAY = int(input("стартовая вершина: "))

graf_for_DA_WAY(main_func())

while True:
    ch = input("Продолжить с той же матрицей? (Y/N)")
    if ch == "N":
        break
    res_num += 1
    Z = int(input("Z = "))
    K = int(input("K = "))
    Pm = int(input("Pm = "))
    Pk = int(input("Pk = "))
    graf_for_DA_WAY(main_func())
