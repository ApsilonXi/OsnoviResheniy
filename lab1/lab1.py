import random

# Функция для метода критического пути (CMP)
def cmp_schedule(tasks, processors):
    # Инициализируем список с нагрузкой на каждый процессор
    load = [0] * processors
    
    # Распределяем задания по процессорам
    for task in tasks:
        # Назначаем задачу на процессор с минимальной текущей нагрузкой
        min_index = load.index(min(load))
        load[min_index] += task
        
    return load

# Функция для метода половинного деления (HDMT)
def hdmt_schedule(tasks, processors):
    if processors % 2 != 0:
        raise ValueError("Количество процессоров должно быть четным")
    
    # Разделяем на два набора
    half_size = processors // 2
    load_a = [0] * half_size
    load_b = [0] * half_size
    
    # Первый уровень - распределение по двум процессорам
    for i, task in enumerate(tasks):
        if i % 2 == 0:
            load_a[i // 2 % half_size] += task
        else:
            load_b[i // 2 % half_size] += task

    return load_a + load_b

# Основная программа
def main():
    num_tasks = int(input("M: "))  # количество заданий
    processors = int(input("N: ")) # количество процессоров
    rand_min = int(input("Min: "))
    rand_max = int(input("Max: "))
    '''num_massives = int(input("Кол-во массивов: ")) # количество списков тасков'''
    num_massives = 50

    all_cmp = []
    all_cmp_asc = []
    all_cmp_desc = []

    all_hdmt = []
    all_hdmt_asc = []
    all_hdmt_desc = []

    cmp_rand = 0
    cmp_asc = 0
    cmp_desc = 0

    hdmt_rand = 0
    hdmt_asc = 0
    hdmt_desc = 0
    
    for i in range(num_massives):
        tasks = []
        for i in range(num_tasks):
            tasks.append(random.randint(rand_min, rand_max))
        tasks_asc = sorted(tasks)
        task_desc = sorted(tasks, reverse=True)

        result_cmp = cmp_schedule(tasks, processors)
        result_cmp_asc = cmp_schedule(tasks_asc, processors)
        result_cmp_desc = cmp_schedule(task_desc, processors)

        result_hdmt = hdmt_schedule(tasks, processors)
        result_hdmt_asc = hdmt_schedule(tasks_asc, processors)
        result_hdmt_desc = hdmt_schedule(task_desc, processors)

        all_cmp.append(max(result_cmp))
        all_cmp_asc.append(max(result_cmp_asc))
        all_cmp_desc.append(max(result_cmp_desc))

        all_hdmt.append(max(result_hdmt))
        all_hdmt_asc.append(max(result_hdmt_asc))
        all_hdmt_desc.append(max(result_hdmt_desc))

        max_val_cmp = min([max(result_cmp), max(result_cmp_asc), max(result_cmp_desc)])

        if max_val_cmp == max(result_cmp_desc):
            cmp_desc += 1 
        elif max_val_cmp == max(result_cmp):
            cmp_rand += 1
        elif max_val_cmp == max(result_cmp_asc):
            cmp_asc += 1
           
            '''print(tasks_asc, result_cmp_asc)
            print(task_desc, result_cmp_desc)  '''  

        max_val_hdmt = min([max(result_hdmt), max(result_hdmt_asc), max(result_hdmt_desc)])

        if max_val_hdmt == max(result_hdmt_desc):
            hdmt_desc += 1
        elif max_val_hdmt ==  max(result_hdmt):
            hdmt_rand += 1
        elif max_val_hdmt == max(result_hdmt_asc):
            hdmt_asc += 1


        
    for i in [all_cmp, all_cmp_asc, all_cmp_desc]:
        aver = sum(i)/len(i)
        i.append(aver)


    for i in [all_hdmt, all_hdmt_asc, all_hdmt_desc]:
        aver = sum(i)/len(i)
        i.append(aver)
        
    print("----------------------")

    print("CMP: ")
    print("Случайно: ", all_cmp[len(all_cmp)-1], cmp_rand) 
    print("По возрастанию: ", all_cmp_asc[len(all_cmp_asc)-1], cmp_asc)
    print("По убыванию: ", all_cmp_desc[len(all_cmp_desc)-1], cmp_desc)

    print("----------------------")

    print("HDMT")
    print("Случайно: ", all_hdmt[len(all_hdmt)-1], hdmt_rand)
    print("По возрастанию: ", all_hdmt_asc[len(all_hdmt_asc)-1], hdmt_asc)
    print("По убыванию: ", all_hdmt_desc[len(all_hdmt_desc)-1], hdmt_desc)
        

if __name__ == "__main__":
    main()
