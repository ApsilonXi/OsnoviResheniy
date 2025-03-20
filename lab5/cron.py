def cron(matrix):
    while True:
        summ = [sum(row) for row in matrix]
        max_index = summ.index(max(summ))
        min_index = summ.index(min(summ))
        delta = max(summ) - min(summ)
        print(delta)

        swapped = False

        for elem in matrix[max_index]:
            if elem < delta:
                matrix[max_index].remove(elem)
                matrix[min_index].append(elem)
                swapped = True
                break

        if not swapped:
            for i in range(len(matrix[min_index])):
                for j in range(len(matrix[max_index])):
                    if matrix[max_index][j] > matrix[min_index][i] and matrix[max_index][j] - matrix[min_index][i] < delta:
                        matrix[max_index][j], matrix[min_index][i] = matrix[min_index][i], matrix[max_index][j]
                        swapped = True
                        break
                    

                if swapped: break
        print(matrix)
        if not swapped or delta in (0, 1): break
    return summ

def cmp_schedule(tasks, processors):
    load = [0 for i in range(processors)]
    loads = [[] for i in range(processors)]
    for i in tasks:
        load_min_index = load.index(min(load))
        load[load_min_index] += i
        loads[load_min_index].append(i)
    return loads

print(cron([[15, 12, 10], [14, 12, 10], [17, 17], [16, 16]]))
