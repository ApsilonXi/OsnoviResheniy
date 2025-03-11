import numpy as np
from random import randint, randrange
import sys
sys.stdout.reconfigure(encoding='utf-8')

def divide_into_intervals(number, N): #принимает конечное число интервала и количество необходимых интервалов, возвращает список кортежей интервалов
    interval_size = number // N
    intervals = []
    start = 1
    for i in range(N):
        end = start + interval_size - 1
        intervals.append((start, end))
        start = end + 1 if i < (N-1) else end
    intervals[-1] = (intervals[-1][0], 255)
    return intervals

def invert_nth_bit(num, n): #инвертация бита, принимает число и номер бита, возвращает число с измененным битом
    binary_num = '{:08b}'.format(num)
    inverted_bit = '0' if binary_num[n] == '1' else '1'
    new_binary_num = binary_num[:n] + inverted_bit + binary_num[n+1:]
    inverted_int = int(new_binary_num, 2)
    return inverted_int

def calculate_adaptation(DNA):
    global T, INTERVALS
    matrix = [[] for _ in range(N)]
    for i in range(len(DNA)):
        for i_nter in range(len(INTERVALS)):
            if DNA[i] in range(*(INTERVALS[i_nter])): #если число принадлежит интервалу
                matrix[i_nter].append(T[i]) #добавить в столбец(строку) соответствующей номеру данного интервала
    print("=====================================")
    for i in matrix: print(i)
    print("=====================================")
    sums = [sum(row) for row in matrix]
    #print(sums, max(sums))
    return max(sums) #вернуть приспособляемость

def MUTATE(DNAp):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(DNAp)
    print(calculate_adaptation(DNAp))
    elemind = randint(0, len(DNAp)-1)
    #if DNAp[elemind] == infinity -> exit
    #еще раз прокинуть мутацию пока не пройдет через все процессоры?
    p = randint(0, 7)
    mutated = invert_nth_bit(DNAp[elemind], p)
    print(f"инвертирован {p}-й бит, мутация осуществлена: {DNAp[elemind]} -> {mutated}")
    DNAp[elemind] = mutated
    print(DNAp)
    print(calculate_adaptation(DNAp))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return DNAp

def CROSSOVER(p1, p2, split):
    global PM
    DNAp = p1[0:split] + p2[split:]
    r = randrange(100)
    if r < PM and PM != 100:
        print(f"вероятность оператора мутации = {r} {PM}, мутация не произошла")
        return DNAp
    else:
        print(f"вероятность оператора мутации = {r} {PM}, осуществление процесса мутации...")
        DNAp = MUTATE(DNAp)
        return DNAp

M, N, t1, t2, Z, K = int(input("M = ")), int(input("N = ")), int(input("t1 = ")), int(input("t2 = ")), int(input("Z (колво повторов) = ")), int(input("K (колво особей в поколении) = "))
PM = int(input("PM = "))
PK = int(input("PK = "))
T = np.array([randint(t1, t2) for j in range(M)])
print(T)

'''M, N, K, Z = 5, 3, 3, 3
T = np.array([11, 16, 12, 20, 13])
print(T)'''

INTERVALS = divide_into_intervals(255, N) #получаем список интервалов вида [(0, n), (n+1, m), ... (x, N)]
print(INTERVALS)


gen = []
for i in range(N):
    DNA = []
    for i in T: DNA.append(randint(0, 255))
    gen.append((DNA, calculate_adaptation(DNA)))
print(f"\nПЕРВОЕ ПОКОЛЕНИЕ: {gen}")

GENERATIONS = {0 : gen}
dictid = 0

BEST = min([specie[1] for specie in gen])
print("лучшая приспособляемость: ", BEST)

COUNTER = 1

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
            
            split = randint(0, len(T)-1)
            print(f"разбитие по {split}...")

            Pdna1 = CROSSOVER(gen[i][0], gen[partner_id][0], split)
            print(f"ПОЛУЧЕН ПОТОМОК {Pdna1}")
            Pdna2 = CROSSOVER(gen[partner_id][0], gen[i][0], split)
            print(f"ПОЛУЧЕН ПОТОМОК {Pdna2}")
            P1 = (Pdna1, calculate_adaptation(Pdna1))
            P2 = (Pdna2, calculate_adaptation(Pdna2))

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

print("\n=====================================")
print(f"ЛУЧШАЯ ПРИСПОСОБЛЯЕМОСТЬ: {BEST}")
print(f"КОЛИЧЕСТВО ПОВТОРОВ: {COUNTER}")
print(f"КОЛИЧЕСТВО ПОЛУЧЕННЫХ ПОКОЛЕНИЙ: {len(list(GENERATIONS.keys()))}")
for key in GENERATIONS:
    print(key, GENERATIONS[key])
print("=====================================\n")

