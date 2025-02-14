from random import randint

def MethodKrona_Start(T, N, M):
    j = 0
    processors = [[] for i in range(N)]
    for task in range(M):
        i = randint(0, N-1)
        processors[i].append(T[j])
        j += 1

def MethodKrona_End(processors):
    load = [sum(k) for k in processors]
    max_proc = load.index(max(load))
    min_proc = load.index(min(load))
    delta = max(load) - min(load)
    while min(processors[max_proc]) < delta:
        tranzit = min(processors[max_proc])
        processors[max_proc].pop(processors[max_proc].index(tranzit))
        processors[min_proc].append(tranzit)
        load = [sum(k) for k in processors]
        delta = max(load) - min(load)
        max_proc = load.index(max(load))
        min_proc = load.index(min(load))
        print(processors)
        print(load)
        print(delta)

    return max(load)

print("----------------------")

M = int(input("M: "))
N = int(input("N: "))
T1 = int(input("Min: "))
T2 = int(input("Max: "))
T = [randint(T1, T2) for i in range(M)]

print("----------------------")

proc = MethodKrona_Start(T, N, M)

print("----------------------\n")
print(f"Результат: {MethodKrona_End(proc)}\n") 
print("----------------------\n")