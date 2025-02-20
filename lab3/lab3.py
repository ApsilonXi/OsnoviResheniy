import random
import math

def init_processor_loads(num_processors):
    return [0] * num_processors

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
    processor_loads = init_processor_loads(N)  
    for i, row in enumerate(matrix):
        min_element = min(row)
        proc_id = distribute_task_to_processor(processor_loads, min_element)
        
        if min_element >= barrier:
            # Переход на алгоритм Плотникова-Зверева
            schedule_plotnikov_zverev(matrix[i:], processor_loads)
            break
    return processor_loads, max(processor_loads)

# Алгоритм Плотникова-Зверева
def schedule_plotnikov_zverev(matrix, processor_loads):
    for i, row in enumerate(matrix):
        max_element = max(row)
        proc_id = distribute_task_to_processor(processor_loads, max_element)
        
        # Проверка необходимости перераспределения нагрузки
        max_load = max(processor_loads)
        min_load = min(processor_loads)
        if max_load - min_load > max_barrier:
            # Перераспределение нагрузки
            processor_loads = rebalance_loads(processor_loads)

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

        # Минимальные значения строк
        min_values = [min(row) for row in matrix]
        min_barrier = math.ceil(sum(min_values) / N)

        # Максимальные значения строк
        max_values = [max(row) for row in matrix]
        global max_barrier
        max_barrier = math.ceil(sum(max_values) / N)

        # Выполнение алгоритма для разных вариантов сортировки
        rand_loads, max_rand = schedule_min_elements(random_sorted_matrix, max_barrier)
        asc_loads, max_asc = schedule_min_elements(asc_sorted_matrix, max_barrier)
        desc_loads, max_desc = schedule_min_elements(desc_sorted_matrix, max_barrier)

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
