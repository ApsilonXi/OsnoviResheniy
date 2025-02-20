import random
import math

def init_processor_loads(num_processors):
    return [0] * num_processors

# Распределение нагрузки
def distribute_task_to_processor(processor_loads, task):
    min_load_index = processor_loads.index(min(processor_loads))
    processor_loads[min_load_index] += task
    return min_load_index + 1  

# Алгоритм минимальных элементов
def schedule_min_elements(matrix, barrier):
    processor_loads = init_processor_loads(N)  
    #print(f"\nПрименение алгоритма минимальных элементов до барьера {barrier}:")
    for i, row in enumerate(matrix):
        min_element = min(row)
        proc_id = distribute_task_to_processor(processor_loads, min_element)
        #print(f"Задача {i+1}, минимальный элемент: {min_element} назначен на процессор {proc_id}")
        
        #print(processor_loads)
        
        if min_element >= barrier:
            #print(f"Барьер {barrier} достигнут на задаче {i+1}, переходим на алгоритм Плотникова-Зверева.")
            schedule_plotnikov_zverev(matrix[i:], processor_loads) 
            break
    return processor_loads, max(processor_loads)

def schedule_plotnikov_zverev(matrix, processor_loads):
    for i, row in enumerate(matrix):
        max_element = max(row)
        proc_id = distribute_task_to_processor(processor_loads, max_element)
        #print(processor_loads)

def main():
    for i in range(num_massives):
        #Генерация случайного массива
        matrix = [[random.randint(min_val, max_val) for _ in range(N)] for _ in range(M)]

        random_sorted_matrix = matrix
        asc_sorted_matrix = sorted(matrix, key=sum)
        desc_sorted_matrix = sorted(matrix, key=sum, reverse=True)

        all_rand = []
        all_asc = []
        all_desc = []

        rand_win = 0
        asc_win = 0
        desc_win = 0

        # Минимальные значения строк
        min_values = [min(row) for row in matrix]
        min_barrier = math.ceil(sum(min_values) / N)

        # Максимальные значения строк
        max_values = [max(row) for row in matrix]
        max_barrier = math.ceil(sum(max_values) / N)

        #print("\nМинимальный барьер:", min_barrier)
        #print("Максимальный барьер:", max_barrier)

        rand_loads, max_rand = schedule_min_elements(random_sorted_matrix, max_barrier)
        asc_loads, max_asc = schedule_min_elements(asc_sorted_matrix, max_barrier)
        desc_loads, max_desc = schedule_min_elements(desc_sorted_matrix, max_barrier)

        all_rand.append(max_rand)
        all_asc.append(max_asc)
        all_desc.append(max_desc)

        max_val_res = min([max(rand_loads), max(asc_loads), max(desc_loads)])

        if max_val_res == max(rand_loads):
            rand_win += 1
        elif max_val_res == max(asc_loads):
            asc_win += 1
            '''print(tasks, max(result_cmp))
            print(task_desc, max(result_cmp_desc))'''
        elif max_val_res == max(desc_loads):
            desc_win += 1 

    for i in [all_rand, all_asc, all_desc]:
        aver = sum(i)/len(i)
        i.append(aver)

    print("---------Lab 3---------")
    print("Случайно: ", all_rand[len(all_rand)-1], max_rand) 
    print("По возрастанию: ", all_asc[len(all_asc)-1], max_asc)
    print("По убыванию: ", all_desc[len(all_desc)-1], max_desc)

M = int(input("M: "))
N = int(input("N: "))
min_val = int(input("Min: "))
max_val = int(input("Max: "))
num_massives = 100

main()
