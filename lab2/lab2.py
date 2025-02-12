import numpy as np
import random

def generate_matrix(num_tasks, num_processors, min_val, max_val):
    # Генерация случайной матрицы с заданным количеством задач и процессоров
    m = np.random.randint(min_val, max_val + 1, size=(num_tasks, num_processors))
    return m

def schedule_with_arbitrary_load(matrix):
    # Массив для хранения нагрузки на процессоры
    load = np.zeros(matrix.shape[1])

    # Шаг 2 и Шаг 3: Пробегаем по строкам и выбираем минимальный элемент
    for row in matrix:
        min_index = np.argmin(load + row)
        load[min_index] += row[min_index]

    # Возвращаем итоговую максимальную загрузку
    return load, np.max(load)

# Основная программа
def main():
    num_tasks = int(input("M: "))  # количество заданий
    processors = int(input("N: ")) # количество процессоров
    rand_min = int(input("Min: "))
    rand_max = int(input("Max: "))
    '''num_massives = int(input("Кол-во массивов: ")) # количество списков тасков'''
    num_massives = 100

    all_cmp = []
    all_cmp_asc = []
    all_cmp_desc = []

    cmp_rand = 0
    cmp_asc = 0
    cmp_desc = 0
    
    for i in range(num_massives):
        tasks = generate_matrix(num_tasks, processors, rand_min, rand_max)
        tasks_asc = []
        for i in range(len(tasks)):
            tasks_asc.append(sorted(tasks[i]))
        tasks_desc = []
        for i in range(len(tasks)):
            tasks_desc.append(sorted(tasks[i], reverse=True))

        result_cmp, max_1 = schedule_with_arbitrary_load(tasks)
        result_cmp_asc, max_2= schedule_with_arbitrary_load(np.array(tasks_asc))
        result_cmp_desc, max_3= schedule_with_arbitrary_load(np.array(tasks_desc))

        all_cmp.append(max_1)
        all_cmp_asc.append(max_2)
        all_cmp_desc.append(max_3)

        max_val_cmp = min([max_1, max_2, max_3])

        if max_val_cmp == max(max_3):
            cmp_desc += 1 
        elif max_val_cmp == max(max_1):
            cmp_rand += 1
        elif max_val_cmp == max(max_2):
            cmp_asc += 1
        
    for i in [all_cmp, all_cmp_asc, all_cmp_desc]:
        aver = sum(i)/len(i)
        i.append(aver)
        
    print("-------Lab 1----------")

    print("Случайно: ", all_cmp[len(all_cmp)-1], cmp_rand) 
    print("По возрастанию: ", all_cmp_asc[len(all_cmp_asc)-1], cmp_asc)
    print("По убыванию: ", all_cmp_desc[len(all_cmp_desc)-1], cmp_desc)

        

if __name__ == "__main__":
    main()
