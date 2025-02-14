import numpy as np
import random

def schedule_with_arbitrary_load(T, N, M):
    load = [0 for i in range(N)]
    for i in T:
        min_el = min(i[:N])
        min_index = i.index(min_el)
        if load[min_index] == 0:
            load[min_index] += min_el
        elif load[min_index] > 0:
            load_min_index = load.index(min(load))
            load[load_min_index] += i[load_min_index]
    return load, max(load)

def sorting(N, T, sort_arg = -1):
    if sort_arg == -1:
        return T
    elif sort_arg == 0:
        return sorted(T, key=lambda x: x[N])
    elif sort_arg == 1:
        return sorted(T, key=lambda x: x[N], reverse=True)

# Основная программа
def main():
    num_tasks = int(input("M: "))  # количество заданий
    processors = int(input("N: ")) # количество процессоров
    rand_min = int(input("Min: "))
    rand_max = int(input("Max: "))
    '''num_massives = int(input("Кол-во массивов: ")) # количество списков тасков'''
    num_massives = 100

    all_schedule = []
    all_schedule_asc = []
    all_schedule_desc = []

    schedule_rand = 0
    schedule_asc = 0
    schedule_desc = 0
    
    for i in range(num_massives):
        tasks = np.random.randint(rand_min, rand_max, (num_tasks, processors)).tolist()
        tasks_asc = sorting(processors-1, tasks, 0)
        tasks_desc = sorting(processors-1, tasks, 1)

        result_schedule, max_rand = schedule_with_arbitrary_load(tasks, processors, num_tasks)
        result_schedule_asc, max_asc = schedule_with_arbitrary_load(tasks_asc, processors, num_tasks)
        result_schedule_desc, max_desc = schedule_with_arbitrary_load(tasks_desc, processors, num_tasks)

        all_schedule.append(max_rand)
        all_schedule_asc.append(max_asc)
        all_schedule_desc.append(max_desc)

        max_val_schedule = min([max_rand, max_asc, max_desc])

        if max_val_schedule == max_desc:
            schedule_desc += 1 
        elif max_val_schedule == max_rand:
            schedule_rand += 1
        elif max_val_schedule == max_asc:
            schedule_asc += 1
        
    for i in [all_schedule, all_schedule_asc, all_schedule_desc]:
        aver = sum(i)/len(i)
        i.append(aver)
        
    print("-------Lab 1----------")

    print("Случайно: ", all_schedule[len(all_schedule)-1], schedule_rand) 
    print("По возрастанию: ", all_schedule_asc[len(all_schedule_asc)-1], schedule_asc)
    print("По убыванию: ", all_schedule_desc[len(all_schedule_desc)-1], schedule_desc)
        

if __name__ == "__main__":
    main()
