import numpy as np
from random import randint, sample

N, M = int(input("N = ")), int(input("M = "))
print("введите границы диапазона:")
t1, t2 = int(input("t1 = ")), int(input("t2 = "))
temp = [randint(t1, t2) for _ in range(M)]

T = np.full((M, N), np.inf)
print(temp)
print(T)

for i in range(M):
    for j in range(N):
        T[i][j] = temp[i]
print(T)
for row in T:
    P = randint(0, 1)
    if P == 1:
        k = randint(1, N-1)
        indices_to_change = sample(range(N), k) 
        for idx in indices_to_change:
            row[idx] = np.inf
print(T)

def sorting(number, matrix):
    match(number):
        case 1: 
            sorted_row_indices = np.argsort(np.min(matrix, axis=1))[::-1]
            sorted_matrix = matrix[sorted_row_indices]
            return sorted_matrix
        case 2: 
            rows_with_infinities = matrix[np.any(matrix == np.inf, axis=1)]
            rows_without = matrix[~np.any(matrix == np.inf, axis=1)]
            first = sorting(1, rows_with_infinities)
            second = sorting(1, rows_without)
            return np.concatenate((first, second), axis=0)
        case 3:
            arr = matrix[np.any(matrix == np.inf, axis=1)]
            rows_without_infinities = matrix[~np.any(matrix == np.inf, axis=1)]
            inf_count = [np.count_nonzero(row == np.inf) for row in arr]
            indices = list(range(len(arr)))
            indices.sort(key=lambda x: (inf_count[x], [-float('inf') if val == np.inf else val for val in arr[x]]), reverse=True)
            first = arr[indices]
            second = sorting(1, rows_without_infinities)
            fuck = np.concatenate((first, second), axis=0)
            print(fuck)
            is_this_fucking_ass = int(input("check... "))
            match(is_this_fucking_ass):
                case 0:
                    return fuck
                case 1:
                    print(fuck.tolist())
                    return np.array(eval(input("... ")))

print("\n1)распределение без изменений\n2)с учетом бесконечностей\n3)с учетом количества бесконечностей в строке")
method = int(input("метод сортировки: "))
match(method):
    case 1: S = sorting(1, T)
    case 2: S = sorting(2, T)
    case 3: S = sorting(3, T)


#print(T)

print(S)


def ALG(matrix):
    global M, N
    sums = np.zeros(N)
    curent_pi = 0
    for i in range(M):
        curent_pi = np.argmin(sums)
        if matrix[i][curent_pi] != np.inf:
            sums[curent_pi] += matrix[i][curent_pi]
        else:
            ch = sums.copy()
            while matrix[i][curent_pi] == np.inf:
                ch[curent_pi] = 999
                curent_pi = np.argmin(ch)
            ch = None
            sums[curent_pi] += matrix[i][curent_pi]
    print(sums, np.max(sums))
ALG(S)


'''T = np.array([[np.inf, 4, np.inf, np.inf],
             [7, 7, 7, 7],
             [np.inf, np.inf, 8, 8],
             [3, 3, 3, 3],
             [6, 6, np.inf, np.inf],
             [11, 11, np.inf, 11],
             [4, 4, np.inf, np.inf],
             [10, 10, 10, 10],
             [15, np.inf, np.inf, 15],
             [12, np.inf, 12, 12]])'''