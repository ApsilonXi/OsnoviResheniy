import random, numpy as np

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

    #print(mins)

    tasks = np.array([])
    for i in np.transpose(mins): tasks = np.append(tasks, i[i != 0][-1])
    #print(tasks, max(tasks))
    return tasks, max(tasks)


def main():
    M = int(input("M: "))
    N = int(input("N: "))
    min_val = int(input("Min: "))
    max_val = int(input("Max: "))
    num_massives = 100

    rand_win_p2 = 0
    asc_win_p2 = 0
    desc_win_p2 = 0

    all_rand_p2 = []
    all_asc_p2 = []
    all_desc_p2 = []

    rand_win_p3 = 0
    asc_win_p3 = 0
    desc_win_p3 = 0

    all_rand_p3 = []
    all_asc_p3 = []
    all_desc_p3 = []

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

        # Определение победителя среди сортировок по максимальной нагрузке
        max_val_res_p2 = min([max(rand_loads_p2), max(asc_loads_p2), max(desc_loads_p2)])

        if max_val_res_p2 == max(rand_loads_p2):
            rand_win_p2 += 1
        elif max_val_res_p2 == max(asc_loads_p2):
            asc_win_p2 += 1
        elif max_val_res_p2 == max(desc_loads_p2):
            desc_win_p2 += 1 
            #print(desc_sorted_matrix, max_desc_p2)

        max_val_res_p3 = min([max(rand_loads_p3), max(asc_loads_p3), max(desc_loads_p3)])

        if max_val_res_p3 == max(rand_loads_p3):
            rand_win_p3 += 1
        elif max_val_res_p3 == max(asc_loads_p3):
            asc_win_p3 += 1
        elif max_val_res_p3 == max(desc_loads_p3):
            desc_win_p3 += 1 

    # Вычисление среднего значения нагрузки
    for i in [all_rand_p2, all_asc_p2, all_desc_p2]:
        aver = sum(i)/len(i)
        i.append(aver)

    for i in [all_rand_p3, all_asc_p3, all_desc_p3]:
        aver = sum(i)/len(i)
        i.append(aver)

    # Вывод результатов
    print("---------------Lab 4---------------")
    print('-------Квадратичный критерий-------')
    print("Случайно: ", all_rand_p2[-1], rand_win_p2) 
    print("По возрастанию: ", all_asc_p2[-1], asc_win_p2)
    print("По убыванию: ", all_desc_p2[-1], desc_win_p2, '\n')
    print('-------Кубический критерий---------')
    print("Случайно: ", all_rand_p3[-1], rand_win_p3) 
    print("По возрастанию: ", all_asc_p3[-1], asc_win_p3)
    print("По убыванию: ", all_desc_p3[-1], desc_win_p3, '\n')

main()