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
    processors = int(input("N: ")) # количество процессоров
    num_tasks = int(input("M: "))  # количество заданий
    num_massives = int(input("Кол-во массивов: ")) # количество списков тасков

    all_cmp = []
    all_cmp_asc = []
    all_cmp_desc = []

    all_hdmt = []
    all_hdmt_asc = []
    all_hdmt_desc = []
    
    for i in range(num_massives):
        tasks = random.sample(range(1, 101), num_tasks)
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

    
    for i in [all_cmp, all_cmp_asc, all_cmp_desc]:
        aver = sum(i)/len(i)
        i.append(aver)

    for i in [all_hdmt, all_hdmt_asc, all_hdmt_desc]:
        aver = sum(i)/len(i)
        i.append(aver)
        
    print("-------Lab 1----------")

    print("CMP: ")
    print("Случайно: ", all_cmp[len(all_cmp)-1])
    print("По возрастанию: ", all_cmp_asc[len(all_cmp_asc)-1])
    print("По убыванию: ", all_cmp_desc[len(all_cmp_desc)-1])

    print("----------------------")

    print("HDMT")
    print("Случайно: ", all_hdmt[len(all_hdmt)-1])
    print("По возрастанию: ", all_hdmt_asc[len(all_hdmt_asc)-1])
    print("По убыванию: ", all_hdmt_desc[len(all_hdmt_desc)-1])
        

if __name__ == "__main__":
    main()
