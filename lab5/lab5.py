import random

def cmp_schedule(tasks, processors):
    load = [0 for i in range(processors)]
    loads = [[] for i in range(processors)]
    for i in tasks:
        load_min_index = load.index(min(load))
        load[load_min_index] += i
        loads[load_min_index].append(i)
    return loads

def pashkeev_back(n, tasks, load, processors):
    for i in range(len(tasks)):
        if n > -1:
            load[n].append(tasks[i]) 
            n -= 1
        if n == -1:
            return pashkeev_forward(0, tasks[i+1:], load, processors)
    return load

def pashkeev_forward(n, tasks, load, processors): 
    for i in range(len(tasks)):
        if n < processors:
            load[n].append(tasks[i]) 
            n += 1
        if n == processors:
            return pashkeev_back(n-1, tasks[i+1:], load, processors)  
    return load

def cron(matrix):
    while True:
        summ = [sum(row) for row in matrix]
        max_index = summ.index(max(summ))
        min_index = summ.index(min(summ))
        delta = max(summ) - min(summ)

        swapped = False

        for elem in matrix[max_index]:
            if elem < delta:
                matrix[max_index].remove(elem)
                matrix[min_index].append(elem)
                swapped = True
                break

        if not swapped:
            for i in range(len(matrix[min_index])):
                for j in range(len(matrix[max_index])):
                    if matrix[max_index][j] > matrix[min_index][i] and matrix[max_index][j] - matrix[min_index][i] < delta:
                        matrix[max_index][j], matrix[min_index][i] = matrix[min_index][i], matrix[max_index][j]
                        swapped = True
                        break
                if swapped: break
        if not swapped or delta in (0, 1): break
    return summ

def main():
    M = int(input("M: "))
    N = int(input("N: "))
    min_val = int(input("Min: "))
    max_val = int(input("Max: "))
    num_massives = 100

    all_rand_cron, all_cmp_cron, all_pashkeev_cron = [], [], []
    rand_win, cmp_win, pashkeev_win = 0, 0, 0

    for i in range(num_massives):
        matrix = [random.randint(min_val, max_val) for _ in range(M)]
        desc_matrix = sorted(matrix, reverse=True)

        desc_matrix_cron = [[] for _ in range(N)]
        for i in matrix: 
            desc_matrix_cron[random.randint(0, N - 1)].append(i)
        for i in desc_matrix_cron: 
            i.sort(reverse=True)

        cmp_result = cmp_schedule(desc_matrix, N)
        pashkeev_result = pashkeev_forward(0, desc_matrix, [[] for _ in range(N)], N)

        cron_rand_result = cron(desc_matrix_cron)
        cron_cmp_result = cron(cmp_result)
        cron_pashkeev_result = cron(pashkeev_result)

        all_rand_cron.append(max(cron_rand_result))
        all_cmp_cron.append(max(cron_cmp_result))
        all_pashkeev_cron.append(max(cron_pashkeev_result))

        max_val_res = min([max(cron_rand_result), max(cron_cmp_result), max(cron_pashkeev_result)])

        if max_val_res == max(cron_rand_result):
            rand_win += 1
            print(desc_matrix, desc_matrix_cron, pashkeev_result, max(cron_rand_result), max(cron_pashkeev_result))
        elif max_val_res == max(cron_pashkeev_result):
            pashkeev_win += 1 
        elif max_val_res == max(cron_cmp_result):
            cmp_win += 1
        
    for i in [all_rand_cron, all_cmp_cron, all_pashkeev_cron]:
        aver = sum(i)/len(i)
        i.append(aver)

    print("---------------Lab 5---------------")
    print('Случайный: ', all_rand_cron[-1], rand_win)
    print('CMP: ', all_cmp_cron[-1], cmp_win)
    print('Пашкеева: ', all_pashkeev_cron[-1], pashkeev_win)

main()
