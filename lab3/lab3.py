import random
import math

# Распределение нагрузки
def distribute_task_to_processor(processor_loads, task):
    min_load_index = processor_loads.index(min(processor_loads))
    processor_loads[min_load_index] += task
    return min_load_index + 1  

# Перераспределение нагрузки между процессорами
def rebalance_loads(processor_loads):
    max_load_index = processor_loads.index(max(processor_loads))
    min_load_index = processor_loads.index(min(processor_loads))
    
    # Переносим часть нагрузки от самого загруженного процессора к самому свободному
    excess_load = (processor_loads[max_load_index] - processor_loads[min_load_index]) // 2
    processor_loads[max_load_index] -= excess_load
    processor_loads[min_load_index] += excess_load
    
    return processor_loads

# Алгоритм минимальных элементов
def schedule_min_elements(matrix, barrier):
    processor_loads = [0] * N  
    for i, row in enumerate(matrix):
        min_element = min(row)
        proc_id = distribute_task_to_processor(processor_loads, min_element)
        
        if min_element >= barrier:
            # Переход на алгоритм Плотникова-Зверева
            schedule_plotnikov_zverev(matrix[i:], processor_loads, barrier)
            break
    return processor_loads, max(processor_loads)

# Алгоритм Плотникова-Зверева
def schedule_plotnikov_zverev(matrix, processor_loads, barrier):
    for i, row in enumerate(matrix):
        max_element = max(row)
        proc_id = distribute_task_to_processor(processor_loads, max_element)
        
        # Проверка необходимости перераспределения нагрузки
        max_load = max(processor_loads)
        min_load = min(processor_loads)
        if (max_load - min_load) >= barrier:
            # Перераспределение нагрузки
            processor_loads = rebalance_loads(processor_loads)

def main():
    rand_win_max = 0
    asc_win_max = 0
    desc_win_max = 0

    all_rand_max = []
    all_asc_max = []
    all_desc_max = []

    rand_win_min = 0
    asc_win_min = 0
    desc_win_min = 0

    all_rand_min = []
    all_asc_min = []
    all_desc_min = []

    for i in range(num_massives):
        # Генерация случайного массива
        matrix = [[random.randint(min_val, max_val) for _ in range(N)] for _ in range(M)]

        random_sorted_matrix = matrix
        asc_sorted_matrix = sorted(matrix, key=sum)
        desc_sorted_matrix = sorted(matrix, key=sum, reverse=True)

        # Максимальные значения строк
        max_values = [max(row) for row in matrix]
        max_barrier = math.ceil(sum(max_values) / N)

        # Минимальные значения строк
        min_values = [min(row) for row in matrix]
        min_barrier = math.ceil(sum(min_values) / N)

        # Выполнение алгоритма для разных вариантов сортировки
        rand_loads_max, max_rand = schedule_min_elements(random_sorted_matrix, max_barrier)
        asc_loads_max, max_asc = schedule_min_elements(asc_sorted_matrix, max_barrier)
        desc_loads_max, max_desc = schedule_min_elements(desc_sorted_matrix, max_barrier)

        rand_loads_min, min_rand = schedule_min_elements(random_sorted_matrix, min_barrier)
        asc_loads_min, min_asc = schedule_min_elements(asc_sorted_matrix, min_barrier)
        desc_loads_min, min_desc = schedule_min_elements(desc_sorted_matrix, min_barrier)
    

        all_rand_max.append(max_rand)
        all_asc_max.append(max_asc)
        all_desc_max.append(max_desc)

        all_rand_min.append(min_rand)
        all_asc_min.append(min_asc)
        all_desc_min.append(min_desc)

        # Определение победителя среди сортировок по максимальной нагрузке
        max_val_res = min([max(rand_loads_max), max(asc_loads_max), max(desc_loads_max)])

        if max_val_res == max(rand_loads_max):
            rand_win_max += 1
        elif max_val_res == max(asc_loads_max):
            asc_win_max += 1
        elif max_val_res == max(desc_loads_max):
            desc_win_max += 1 

        min_val_res = min([max(rand_loads_min), max(asc_loads_min), max(desc_loads_min)])

        if min_val_res == max(rand_loads_min):
            rand_win_min += 1
        elif min_val_res == max(asc_loads_min):
            asc_win_min += 1
        elif min_val_res == max(desc_loads_min):
            desc_win_min += 1

    # Вычисление среднего значения нагрузки
    for i in [all_rand_max, all_asc_max, all_desc_max]:
        aver = sum(i)/len(i)
        i.append(aver)

    for i in [all_rand_min, all_asc_min, all_desc_min]:
        aver = sum(i)/len(i)
        i.append(aver)

    # Вывод результатов
    print("---------Lab 3---------")
    print("Максимальные барьеры:")
    print("Случайно: ", all_rand_max[-1], rand_win_max) 
    print("По возрастанию: ", all_asc_max[-1], asc_win_max)
    print("По убыванию: ", all_desc_max[-1], desc_win_max, '\n')

    print("Минимальные барьеры:")
    print("Случайно: ", all_rand_min[-1], rand_win_min) 
    print("По возрастанию: ", all_asc_min[-1], asc_win_min)
    print("По убыванию: ", all_desc_min[-1], desc_win_min, '\n')

M = int(input("M: "))
N = int(input("N: "))
min_val = int(input("Min: "))
max_val = int(input("Max: "))
num_massives = 100

main()
