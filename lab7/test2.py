import numpy as np

import numpy as np

def generate_random_matrix(M, N, min_val=1, max_val=10, inf_prob=0.2):
    matrix = np.random.randint(min_val, max_val + 1, size=(M, N)).astype(float)
    mask = np.random.random(size=(M, N)) < inf_prob
    for i in range(M):
        if np.all(mask[i]):  
            j = np.random.randint(0, N)  
            mask[i, j] = False 
    matrix[mask] = np.inf
    return matrix

def sort_matrix(matrix, sort_type='Исходная'):
    if sort_type == 'Исходная':
        return matrix.copy()
    rows = []
    for i, row in enumerate(matrix):
        inf_count = np.sum(row == np.inf)
        row_sum = np.sum(row[row != np.inf])
        rows.append((i, inf_count, row_sum))
    if sort_type == 'Кол-во бесконечностей':
        rows.sort(key=lambda x: (-x[1], x[0]))
    elif sort_type == 'Кол-во бесконечностей и сумма':
        rows.sort(key=lambda x: (-x[1], -x[2], x[0]))
    sorted_matrix = np.array([matrix[row[0]] for row in rows])
    return sorted_matrix

def PZ_algorithm(matrix, criterion='Минимакс', sort_type='Исходная'):
    M, N = len(matrix), len(matrix[0])
    tasks = []
    for i in range(M):
        row = matrix[i]
        if criterion == 'Минимакс':
            weight = max([x for x in row if x != np.inf])
        elif criterion == 'Квадратичный':
            weight = sum(x ** 2 for x in row if x != np.inf)
        elif criterion == 'Кубический':
            weight = sum(x ** 3 for x in row if x != np.inf)
        tasks.append((i, weight))
    tasks.sort(key=lambda x: -x[1])
    sums = np.zeros(N)
    
    for task in tasks:
        task_idx = task[0]
        current_pi = np.argmin(sums)
        if matrix[task_idx][current_pi] == np.inf:
            ch = sums.copy()
            while matrix[task_idx][current_pi] == np.inf:
                ch[current_pi] = np.inf
                current_pi = np.argmin(ch)
        sums[current_pi] += matrix[task_idx][current_pi]
    return sums, np.max(sums)

M = int(input("M: "))
N = int(input("N: "))
min_val = int(input("Min: "))
max_val = int(input("Max: "))
num_matrix = 100

all_rand_minimax, all_rand_square, all_rand_cube = [], [], []
all_count_minimax, all_count_square, all_count_cube = [], [], []
all_sum_minimax, all_sum_square, all_sum_cube = [], [], []

rand_win_minimax, rand_win_square, rand_win_cube = 0, 0, 0
count_win_minimax, count_win_square, count_win_cube = 0, 0, 0
sum_win_minimax, sum_win_square, sum_win_cube = 0, 0, 0

for i in range(num_matrix):
    matrix = generate_random_matrix(M, N, min_val, max_val)

    for sort_type in ['Исходная', 'Кол-во бесконечностей', 'Кол-во бесконечностей и сумма']:
        for crit in ['Минимакс', 'Квадратичный', 'Кубический']:
            matrix_sort = sort_matrix(matrix, sort_type)
            sums, makespan = PZ_algorithm(matrix_sort, crit, sort_type)
            match sort_type:
                case 'Исходная':
                    match crit:
                        case 'Минимакс':
                            all_rand_minimax.append(makespan)
                        case 'Квадратичный':
                            all_rand_square.append(makespan)
                        case 'Кубический':
                            all_rand_cube.append(makespan)
                case 'Кол-во бесконечностей':
                    match crit:
                        case 'Минимакс':
                            all_count_minimax.append(makespan)
                        case 'Квадратичный':
                            all_count_square.append(makespan)
                        case 'Кубический':
                            all_count_cube.append(makespan)
                case 'Кол-во бесконечностей и сумма':
                    match crit:
                        case 'Минимакс':
                            all_sum_minimax.append(makespan)
                        case 'Квадратичный':
                            all_sum_square.append(makespan)
                        case 'Кубический':
                            all_sum_cube.append(makespan)

for i in [all_rand_minimax, all_rand_square, all_rand_cube]:
    aver = sum(i)/len(i)
    i.append(aver)

for i in [all_count_minimax, all_count_square, all_count_cube]:
    aver = sum(i)/len(i)
    i.append(aver)

for i in [all_sum_minimax, all_sum_square, all_sum_cube]:
    aver = sum(i)/len(i)
    i.append(aver)

for i in range(num_matrix):
    min_res_val_rand = min(all_rand_minimax[i], all_rand_square[i], all_rand_cube[i])
    if min_res_val_rand == all_rand_minimax[i]:
        rand_win_minimax += 1
    elif min_res_val_rand == all_rand_square[i]:
        rand_win_square += 1
    elif min_res_val_rand == all_rand_cube[i]:
        rand_win_cube += 1 

    min_res_val_count = min(all_count_minimax[i], all_count_square[i], all_count_cube[i])
    if min_res_val_count == all_count_minimax[i]:
        count_win_minimax += 1
    elif min_res_val_count == all_count_square[i]:
        count_win_square += 1
    elif min_res_val_count == all_count_cube[i]:
        count_win_cube += 1

    min_res_val_sum = min(all_sum_minimax[i], all_sum_square[i], all_sum_cube[i])
    if min_res_val_sum == all_sum_minimax[i]:
        sum_win_minimax += 1
    elif min_res_val_sum == all_sum_square[i]:
        sum_win_square += 1
    elif min_res_val_sum == all_sum_cube[i]:
        sum_win_cube += 1

print("\n---------------Lab 7---------------")
print(f"{'Исходная матрица:':<25}{'Ср.знач':<10}{'Победы':<10}")
print(f"{'Минимакс:':<25}{round(all_rand_minimax[-1], 2):<10} | {rand_win_minimax:<5}")
print(f"{'Квадратичный:':<25}{round(all_rand_square[-1], 2):<10} | {rand_win_square:<5}")
print(f"{'Кубический:':<25}{round(all_rand_cube[-1], 2):<10} | {rand_win_cube:<5}")
print(f"\n{'Кол-во бесконечностей:':<25}{'Ср.знач':<10}{'Победы':<10}")
print(f"{'Минимакс:':<25}{round(all_count_minimax[-1], 2):<10} | {count_win_minimax:<5}")
print(f"{'Квадратичный:':<25}{round(all_count_square[-1], 2):<10} | {count_win_square:<5}")
print(f"{'Кубический:':<25}{round(all_count_cube[-1], 2):<10} | {count_win_cube:<5}")
print(f"\n{'Кол-во и суммы:':<25}{'Ср.знач':<10}{'Победы':<10}")
print(f"{'Минимакс:':<25}{round(all_sum_minimax[-1], 2):<10} | {sum_win_minimax:<5}")
print(f"{'Квадратичный:':<25}{round(all_sum_square[-1], 2):<10} | {sum_win_square:<5}")
print(f"{'Кубический:':<25}{round(all_sum_cube[-1], 2):<10} | {sum_win_cube:<5}")


