import random
import math






def main():
    rand_win = 0
    asc_win = 0
    desc_win = 0

    all_rand = []
    all_asc = []
    all_desc = []

    for i in range(num_massives):
        # Генерация случайного массива
        matrix = [[random.randint(min_val, max_val) for _ in range(N)] for _ in range(M)]

        random_sorted_matrix = matrix
        asc_sorted_matrix = sorted(matrix, key=sum)
        desc_sorted_matrix = sorted(matrix, key=sum, reverse=True)

        # Выполнение алгоритма для разных вариантов сортировки
        rand_loads, max_rand = 0 # сюда функция
        asc_loads, max_asc = 0
        desc_loads, max_desc = 0

        all_rand.append(max_rand)
        all_asc.append(max_asc)
        all_desc.append(max_desc)

        # Определение победителя среди сортировок по максимальной нагрузке
        max_val_res = min([max(rand_loads), max(asc_loads), max(desc_loads)])

        if max_val_res == max(rand_loads):
            rand_win += 1
        elif max_val_res == max(asc_loads):
            asc_win += 1
        elif max_val_res == max(desc_loads):
            desc_win += 1 

    # Вычисление среднего значения нагрузки
    for i in [all_rand, all_asc, all_desc]:
        aver = sum(i)/len(i)
        i.append(aver)

    # Вывод результатов
    print("---------Lab 3---------")
    print("Случайно: ", all_rand[-1], rand_win) 
    print("По возрастанию: ", all_asc[-1], asc_win)
    print("По убыванию: ", all_desc[-1], desc_win)

M = int(input("M: "))
N = int(input("N: "))
min_val = int(input("Min: "))
max_val = int(input("Max: "))
num_massives = 100

main()