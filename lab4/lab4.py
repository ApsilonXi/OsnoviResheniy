import random, numpy as np
import time

def sort(T, choice):
    match choice:
        case 0: return T
        case 1: return T[np.sum(T, axis=1).argsort()]
        case 2: return T[np.sum(T, axis=1).argsort()[::-1]]

def alg(T, N, M, p):
    matrix = T.copy()
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

    print('1', mins)

    tasks = np.array([])
    for i in np.transpose(mins): tasks = np.append(tasks, i[i != 0][-1])
    #print(tasks, max(tasks))
    return tasks, max(tasks)

def Plotnikov_Zverev(matrix, N, M): 
    start = time.time()
    load = np.zeros(N)
    path = []
    for row in range(M):
        matrix[row] += load
        tmp_row = matrix[row].copy()
        e, i = np.min(tmp_row), np.argmin(tmp_row)
        load[i] = e
        path.append(i)
        print('2', load)
    #return load, path, time.time()-start
    return load, np.max(load)


def main():
    M = int(input("M: "))
    N = int(input("N: "))
    min_val = int(input("Min: "))
    max_val = int(input("Max: "))
    num_massives = 100

    rand_win_p2, asc_win_p2, desc_win_p2 = 0, 0, 0
    rand_win_p3, asc_win_p3, desc_win_p3 = 0, 0, 0
    rand_win_zver, asc_win_zver, desc_win_zver = 0, 0, 0

    all_rand_p2, all_asc_p2, all_desc_p2 = [], [], []
    all_rand_p3, all_asc_p3, all_desc_p3 = [], [], []
    all_rand_zver, all_asc_zver, all_desc_zver = [], [], []

    for i in range(num_massives):
        # Генерация случайного массива
        matrix = np.array([[random.randint(min_val, max_val) for _ in range(N)] for _ in range(M)])

        random_sorted_matrix = matrix
        asc_sorted_matrix = sort(matrix, 1)
        desc_sorted_matrix = sort(matrix, 2)

        # Выполнение алгоритма для разных вариантов сортировки
        rand_loads_p2, max_rand_p2 = alg(random_sorted_matrix, N, M, 2) 
        asc_loads_p2, max_asc_p2 = alg(asc_sorted_matrix, N, M, 2)
        desc_loads_p2, max_desc_p2 = alg(desc_sorted_matrix, N, M, 2)

        all_rand_p2.append(max_rand_p2)
        all_asc_p2.append(max_asc_p2)
        all_desc_p2.append(max_desc_p2)

        rand_loads_p3, max_rand_p3 = alg(random_sorted_matrix, N, M, 3) 
        asc_loads_p3, max_asc_p3 = alg(asc_sorted_matrix, N, M, 3)
        desc_loads_p3, max_desc_p3 = alg(desc_sorted_matrix, N, M, 3)

        all_rand_p3.append(max_rand_p3)
        all_asc_p3.append(max_asc_p3)
        all_desc_p3.append(max_desc_p3)

        rand_loads_zver, max_rand_zver = Plotnikov_Zverev(random_sorted_matrix.tolist(), N, M)
        asc_loads_zver, max_asc_zver = Plotnikov_Zverev(asc_sorted_matrix.tolist(), N, M)
        desc_loads_zver, max_desc_zver =Plotnikov_Zverev(desc_sorted_matrix.tolist(), N, M)

        all_rand_zver.append(max_rand_zver)
        all_asc_zver.append(max_asc_zver)
        all_desc_zver.append(max_desc_zver)

        # Определение победителя среди сортировок по максимальной нагрузке
        max_val_res_p2 = min([max(rand_loads_p2), max(asc_loads_p2), max(desc_loads_p2)])

        if max_val_res_p2 == max(rand_loads_p2):
            rand_win_p2 += 1
        elif max_val_res_p2 == max(asc_loads_p2):
            asc_win_p2 += 1
        elif max_val_res_p2 == max(desc_loads_p2):
            desc_win_p2 += 1 
            

        max_val_res_p3 = min([max(rand_loads_p3), max(asc_loads_p3), max(desc_loads_p3)])

        if max_val_res_p3 == max(rand_loads_p3):
            rand_win_p3 += 1
        elif max_val_res_p3 == max(asc_loads_p3):
            asc_win_p3 += 1
        elif max_val_res_p3 == max(desc_loads_p3):
            desc_win_p3 += 1 

        max_val_res_zver = np.min([np.max(rand_loads_zver), np.max(asc_loads_zver), np.max(desc_loads_zver)])

        if max_val_res_zver == np.max(rand_loads_zver):
            rand_win_zver += 1
        elif max_val_res_zver == np.max(asc_loads_zver):
            asc_win_zver += 1
        elif max_val_res_zver == np.max(desc_loads_zver):
            desc_win_zver += 1 
            print('3', desc_sorted_matrix, desc_loads_zver, max(desc_loads_p2))

    # Вычисление среднего значения нагрузки
    for i in [all_rand_p2, all_asc_p2, all_desc_p2]:
        aver = sum(i)/len(i)
        i.append(aver)

    for i in [all_rand_p3, all_asc_p3, all_desc_p3]:
        aver = sum(i)/len(i)
        i.append(aver)

    for i in [all_rand_zver, all_asc_zver, all_desc_zver]:
        aver = sum(i)/len(i)
        i.append(aver)

    # Вывод результатов
    print("---------------Lab 4---------------")
    print('-------Квадратичный критерий-------')
    print("Случайно: ", all_rand_p2[-1], '|', rand_win_p2) 
    print("По возрастанию: ", all_asc_p2[-1], '|', asc_win_p2)
    print("По убыванию: ", all_desc_p2[-1], '|', desc_win_p2, '\n')
    print('-------Кубический критерий---------')
    print("Случайно: ", all_rand_p3[-1], '|', rand_win_p3) 
    print("По возрастанию: ", all_asc_p3[-1], '|', asc_win_p3)
    print("По убыванию: ", all_desc_p3[-1], '|', desc_win_p3, '\n')
    print('-------Минимаксный критерий---------')
    print("Случайно: ", all_rand_zver[-1], '|', rand_win_zver) 
    print("По возрастанию: ", all_asc_zver[-1], '|', asc_win_zver)
    print("По убыванию: ", all_desc_zver[-1], '|', desc_win_zver, '\n')

main()