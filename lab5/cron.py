def cron(matrix):
    while True:
        summ = [sum(row) for row in matrix]
        max_index = summ.index(max(summ))
        min_index = summ.index(min(summ))
        delta = max(summ) - min(summ)

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
        if not swapped or delta in (0, 1): break
    return summ

print(cron([[14, 15, 15, 11], [18, 17, 15], [22, 15, 17], [21, 19, 11]]))