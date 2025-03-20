from random import randint, randrange
import numpy as np

def divide_into_intervals(number, N):
    interval_size = number // N
    intervals = []
    start = 1
    for i in range(N):
        end = start + interval_size - 1
        intervals.append((start, end))
        start = end + 1 if i < (N-1) else end
    intervals[-1] = (intervals[-1][0], 255)
    return intervals

def invert_nth_bit(num, n):
    binary_num = '{:08b}'.format(num)
    inverted_bit = '0' if binary_num[n] == '1' else '1'
    new_binary_num = binary_num[:n] + inverted_bit + binary_num[n+1:]
    inverted_int = int(new_binary_num, 2)
    return inverted_int

def Alg(T, N, M, p):
    matrix = []
    for i in T: 
        matrix.append(i)
    mins = np.zeros((M, N))
    lead = np.zeros(N)
    for row in range(0, M):
        if row != M-1:
            current_row = matrix[row]
            Tt = np.power(current_row, p)
            for i in range(0, len(lead)):
                Tt = Tt + lead[i]**p
                Tt[i] -= lead[i]**p
            ind = np.argmin(Tt)
            elem = current_row[ind]
            mins[row][ind] = elem
            lead[ind] = elem
            matrix[row+1] = matrix[row+1] + lead
        elif row == M-1:
            current_row = matrix[row]
            Tt = np.power(current_row, p)
            for i in range(0, len(lead)):
                Tt = Tt + lead[i]**p
                Tt[i] -= lead[i]**p
            ind = np.argmin(Tt)
            elem = current_row[ind]
            mins[row][ind] = elem
            lead[ind] = elem
    tasks = np.array([])
    for i in np.transpose(mins):
        non_zero_i = i[i != 0]
        if non_zero_i.size > 0:
            tasks = np.append(tasks, non_zero_i[-1])
    return int(max(tasks))

def Plotnikov_Zverev(T, N, M):
    matrix = []
    for i in T: 
        matrix.append(i)
    load = np.zeros(N)
    path = []
    for row in range(M):
        matrix[row] += load
        tmp_row = matrix[row].copy()
        e, i = np.min(tmp_row), np.argmin(tmp_row)
        load[i] = e
        path.append(i)
    return int(max(load))

def calculate_adaptation(DNA, p):
    if p == 0:
        return Plotnikov_Zverev(DNA, N, M)
    elif p == 2:
        return Alg(DNA, N, M, 2)
    elif p == 3:
        return Alg(DNA, N, M, 3)

def MUTATE(DNAp):
    elemind = randint(0, len(DNAp)-1)  
    genind = randint(0, len(DNAp[elemind])-1) 
    p = randint(0, 7) 
    mutated = invert_nth_bit(int(DNAp[elemind][genind]), p)
    DNAp[elemind][genind] = mutated  
    return DNAp

def CROSSOVER(p1, p2, split):
    global PM
    DNAp = p1[0:split] + p2[split:]
    r = randrange(100)
    if r < PM and PM != 100:
        return DNAp
    else:
        DNAp = MUTATE(DNA)
        return DNAp

def evaluate_criteria(generation):
    criteria_results = {
        "min_max_gene": min([individual[1] for individual in generation if max(individual[0]) == min([max(ind[0]) for ind in generation])]),
        "min_sum_square": min([individual[1] for individual in generation if sum(x**2 for x in individual[0]) == min([sum(x**2 for x in ind[0]) for ind in generation])]),
        "min_sum_cube": min([individual[1] for individual in generation if sum(x**3 for x in individual[0]) == min([sum(x**3 for x in ind[0]) for ind in generation])]),
    }
    return criteria_results

def main(gen, p):
    GENERATIONS, BEST = {0 : gen}, min([specie[1] for specie in gen])
    COUNTER = 1
    dictid = 0
    while COUNTER != Z:
        nextgen = []
        for i in range(len(gen)): 
            r = randrange(100)
            if r < PK and PK != 100:
                nextgen.append(gen[i])
                
            else:
                partner_id = i
                while partner_id == i:
                    partner_id = randint(0, (len(gen)-1))
                
                split = randint(0, len(T)-1)

                Pdna1 = CROSSOVER(gen[i][0], gen[partner_id][0], split)
                Pdna2 = CROSSOVER(gen[partner_id][0], gen[i][0], split)
                P1 = (Pdna1, calculate_adaptation(Pdna1, p))
                P2 = (Pdna2, calculate_adaptation(Pdna2, p))

                contest = [gen[i][1], P1[1], P2[1]]
                win = min(contest)
                win_id = contest.index(win)

                if win_id == 0:
                    nextgen.append(gen[i])
                elif win_id == 1:
                    nextgen.append(P1)
                elif win_id == 2:
                    nextgen.append(P2)
        
        newBEST = min([specie[1] for specie in nextgen])
        if newBEST == BEST:
            COUNTER += 1
        elif newBEST < BEST:
            BEST = newBEST
            COUNTER = 1
        
        dictid += 1
        GENERATIONS[dictid] = nextgen
        gen = nextgen
    return COUNTER, BEST, GENERATIONS

# Входные данные
'''M = int(input("M = "))
N = int(input("N = "))
min_val = int(input("Min = "))
max_val = int(input("Max = "))
Z = int(input("Z (колво повторов) = "))
K = int(input("K (колво особей в поколении) = "))
PM = int(input("PM = "))
PK = int(input("PK = "))'''
M = 12
N = 4
min_val = 10
max_val = 20
Z = 100
K = 100
PM = 80
PK = 80

T = [[randint(min_val, max_val) for _ in range(N)] for _ in range(M)]
INTERVALS = divide_into_intervals(255, N)

gen_minmax, gen_square, gen_cube = [], [], []
all_minmax, all_square, all_cube = [], [], []
win_minmax, win_square, win_cube = 0, 0, 0

for i in range(K):
    DNA = []
    for j in T: 
        DNA.append([randint(min_val, max_val) for _ in range(N)])
    gen_minmax.append((DNA, calculate_adaptation(DNA, 0)))
    gen_square.append((DNA, calculate_adaptation(DNA, 2)))
    gen_cube.append((DNA,   calculate_adaptation(DNA, 3)))

counts_minmax, best_minmax, gens_minmax = main(gen_minmax, 0)
counts_square, best_square, gens_square = main(gen_square, 2)
counts_cube, best_cube, gens_cube = main(gen_cube, 3)

with open("minimax.txt", "w", encoding='utf-8') as file:
    file.write("===============Минимакс===============\n")
    file.write(f"ЛУЧШАЯ ПРИСПОСОБЛЯЕМОСТЬ: {best_minmax}\n")
    file.write(f"КОЛИЧЕСТВО ПОВТОРОВ: {counts_minmax}\n")
    file.write(f"КОЛИЧЕСТВО ПОЛУЧЕННЫХ ПОКОЛЕНИЙ: {len(list(gens_minmax.keys()))}\n")
    for key in gens_minmax:
        generation_as_lists_minmax = [(np.array(dna[0]).tolist(), dna[1]) for dna in gens_minmax[key]]
        file.write(f"Поколение {key}: \n")
        for i in generation_as_lists_minmax:
            all_minmax.append(i[1])
            for j in i[0]:
                if i[0][len(i[0])-1] == j:
                    file.write(f"{j} ")
                else:
                    file.write(f"{j}\n")
            file.write(f"{i[1]}\n")
            file.write('-----------------\n')
    file.write("========================================\n")

with open("square.txt", "w", encoding='utf-8') as file:
    file.write("==============Квадратичный==============\n")
    file.write(f"ЛУЧШАЯ ПРИСПОСОБЛЯЕМОСТЬ: {best_square}\n")
    file.write(f"КОЛИЧЕСТВО ПОВТОРОВ: {counts_square}\n")
    file.write(f"КОЛИЧЕСТВО ПОЛУЧЕННЫХ ПОКОЛЕНИЙ: {len(list(gens_square.keys()))}\n")
    for key in gens_square:
        generation_as_lists_square = [(np.array(dna[0]).tolist(), dna[1]) for dna in gens_square[key]]
        file.write(f"Поколение {key}: \n")
        for i in generation_as_lists_square:
            all_square.append(i[1])
            for j in i[0]:
                if i[0][len(i[0])-1] == j:
                    file.write(f"{j} ")
                else:
                    file.write(f"{j}\n")
            file.write(f"{i[1]}\n")
            file.write('-----------------\n')
    file.write("============================================\n")

with open("cube.txt", "w", encoding='utf-8') as file:
    file.write("================Кубический================\n")
    file.write(f"ЛУЧШАЯ ПРИСПОСОБЛЯЕМОСТЬ: {best_cube}\n")
    file.write(f"КОЛИЧЕСТВО ПОВТОРОВ: {counts_cube}\n")
    file.write(f"КОЛИЧЕСТВО ПОЛУЧЕННЫХ ПОКОЛЕНИЙ: {len(list(gens_cube.keys()))}\n")
    for key in gens_cube:
        generation_as_lists_cube = [(np.array(dna[0]).tolist(), dna[1]) for dna in gens_cube[key]]
        file.write(f"Поколение {key}: \n")
        for i in generation_as_lists_cube:
            all_cube.append(i[1])
            for j in i[0]:
                if i[0][len(i[0])-1] == j:
                    file.write(f"{j} ")
                else:
                    file.write(f"{j}\n")
            file.write(f"{i[1]}\n")
            file.write('-----------------\n')
    file.write("============================================\n")
    
for i in range(K):
    min_val_res = min([generation_as_lists_minmax[i][1], generation_as_lists_square[i][1], generation_as_lists_cube[i][1]])

    if min_val_res == generation_as_lists_minmax[i][1]:
        win_minmax += 1
    elif min_val_res == generation_as_lists_square[i][1]:
        win_square += 1 
    elif min_val_res == generation_as_lists_cube[i][1]:
        win_cube += 1

for i in [all_minmax, all_square, all_cube]:
    i.append(sum(i)/len(i))

print("\n---------------Lab 6---------------")
print('Минимаксный:  ', round(all_minmax[-1], 2), '|', win_minmax, '|', len(gens_minmax))
print('Квадратичный: ', round(all_square[-1], 2), '|', win_square, '|', len(gens_square))
print('Кубический:   ', round(all_cube[-1], 2), '|', win_cube, '|', len(gens_cube))

print("\nРезультаты успешно записаны в файл.\n")


