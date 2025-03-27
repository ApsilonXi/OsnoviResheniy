import numpy as np
from random import random

def Alg(T, N, M, p):
    matrix = T.copy()
    mins = np.zeros((M, N))
    lead = np.zeros(N)
    
    for row in range(M):
        current_row = matrix[row]
        Tt = np.power(current_row, p)
        
        # Обработка бесконечностей
        Tt[np.isinf(Tt)] = np.inf  # Сохраняем бесконечности
        
        # Добавляем lead только к конечным значениям
        for i in range(N):
            if not np.isinf(Tt[i]):
                Tt[i] += lead[i]**p
        
        # Находим минимальное значение, игнорируя бесконечности
        min_val = np.min(Tt[np.isfinite(Tt)]) if np.any(np.isfinite(Tt)) else np.inf
        candidates = np.where(Tt == min_val)[0]
        
        # Если все элементы бесконечны, выбираем первый
        if len(candidates) == 0:
            ind = 0
        else:
            ind = candidates[0]
        
        elem = current_row[ind]
        mins[row][ind] = elem if not np.isinf(elem) else 0
        lead[ind] = elem if not np.isinf(elem) else lead[ind]
        
        if row != M-1:
            # Добавляем lead только к конечным значениям в следующей строке
            for i in range(N):
                if not np.isinf(matrix[row+1][i]):
                    matrix[row+1][i] += lead[i] if not np.isinf(lead[i]) else 0

    tasks = np.array([])
    for i in np.transpose(mins):
        non_zero = i[i != 0]
        if len(non_zero) > 0:
            tasks = np.append(tasks, non_zero[-1])
        else:
            tasks = np.append(tasks, 0)
    
    return tasks, np.max(tasks[np.isfinite(tasks)]) if np.any(np.isfinite(tasks)) else np.inf


def Plotnikov_Zverev(matrix, N, M): 
    load = np.zeros(N)
    path = []
    
    for row in range(M):
        # Добавляем load только к конечным значениям
        for i in range(N):
            if not np.isinf(matrix[row][i]):
                matrix[row][i] += load[i] if not np.isinf(load[i]) else 0
        
        tmp_row = matrix[row].copy()
        
        # Находим минимальное значение, игнорируя бесконечности
        if np.all(np.isinf(tmp_row)):
            e, i = np.inf, 0
        else:
            min_val = np.min(tmp_row[np.isfinite(tmp_row)])
            candidates = np.where(tmp_row == min_val)[0]
            i = candidates[0]
            e = tmp_row[i]
        
        load[i] = e if not np.isinf(e) else load[i]
        path.append(i)
    
    max_load = np.max(load[np.isfinite(load)]) if np.any(np.isfinite(load)) else np.inf
    return load, max_load

def Sort(method: int, matrix):
    if method == 1:
        # Без изменений (исходная матрица)
        return matrix.copy()
    elif method == 2:
        # Сортировка по количеству бесконечностей в строке (по убыванию)
        inf_counts = np.sum(np.isinf(matrix), axis=1)
        return matrix[np.argsort(-inf_counts)]  # минус для сортировки по убыванию
    elif method == 3:
        # Сортировка сначала по количеству бесконечностей (по убыванию), затем по сумме элементов
        inf_counts = np.sum(np.isinf(matrix), axis=1)
        row_sums = np.array([np.sum(row[np.isfinite(row)]) for row in matrix])
        # Сортируем по убыванию количества бесконечностей и убыванию суммы
        sort_indices = np.lexsort((-row_sums, -inf_counts))  # минус для сортировки по убыванию
        return matrix[sort_indices]
    return matrix.copy()

def generate_matrix(M, N, min_val, max_val, inf_prob):
    """Генерация матрицы с разными значениями для каждого процессора"""
    base = np.random.randint(min_val, max_val + 1, size=(M, N))
    inf_mask = np.random.random(size=(M, N)) < inf_prob
    return np.where(inf_mask, np.inf, base)

def main():

    
    M = int(input("M: "))
    N = int(input("N: "))
    min_val = int(input("Min: "))
    max_val = int(input("Max: "))
    num_massives = 100
    inf_prob = 0.3  # Вероятность бесконечности

    results = {
        'original': {'minimax': [], 'square': [], 'cube': []},
        'inf_count': {'minimax': [], 'square': [], 'cube': []},
        'inf_count_sum': {'minimax': [], 'square': [], 'cube': []}
    }
    wins = {
        'original': {'minimax': 0, 'square': 0, 'cube': 0},
        'inf_count': {'minimax': 0, 'square': 0, 'cube': 0},
        'inf_count_sum': {'minimax': 0, 'square': 0, 'cube': 0}
    }

    for _ in range(num_massives):
        T = generate_matrix(M, N, min_val, max_val, inf_prob)

        matrix_original = Sort(1, T)
        matrix_inf_count = Sort(2, T)
        matrix_inf_count_sum = Sort(3, T)

        for method, matrix in [('original', matrix_original),
                             ('inf_count', matrix_inf_count),
                             ('inf_count_sum', matrix_inf_count_sum)]:
            
            # Получаем только максимальные значения (вторые элементы кортежей)
            res_minimax = Plotnikov_Zverev(matrix, N, M)[1]
            res_square = Alg(matrix, N, M, 2)[1]
            res_cube = Alg(matrix, N, M, 3)[1]
            
            results[method]['minimax'].append(res_minimax)
            results[method]['square'].append(res_square)
            results[method]['cube'].append(res_cube)
            
            # Сравниваем только конечные результаты
            valid_results = {
                'minimax': res_minimax,
                'square': res_square,
                'cube': res_cube
            }
            # Фильтруем только конечные значения
            valid_results = {k: v for k, v in valid_results.items() if not np.isinf(v)}
            
            if valid_results:
                winner = min(valid_results, key=valid_results.get)
                wins[method][winner] += 1

    # Вывод результатов
    print("---------------Lab 7---------------")
    print('---------------Исходная матрица---------------')
    print(f'Минимальный: {np.mean(results["original"]["minimax"]):.2f} {wins["original"]["minimax"]}')
    print(f'Квадратичный: {np.mean(results["original"]["square"]):.2f} {wins["original"]["square"]}')
    print(f'Кубический: {np.mean(results["original"]["cube"]):.2f} {wins["original"]["cube"]}')
    
    print('---------------По количеству бесконечностей---------------')
    print(f'Минимальный: {np.mean(results["inf_count"]["minimax"]):.2f} {wins["inf_count"]["minimax"]}')
    print(f'Квадратичный: {np.mean(results["inf_count"]["square"]):.2f} {wins["inf_count"]["square"]}')
    print(f'Кубический: {np.mean(results["inf_count"]["cube"]):.2f} {wins["inf_count"]["cube"]}')
    
    print('---------------По количеству бесконечностей и сумме---------------')
    print(f'Минимальный: {np.mean(results["inf_count_sum"]["minimax"]):.2f} {wins["inf_count_sum"]["minimax"]}')
    print(f'Квадратичный: {np.mean(results["inf_count_sum"]["square"]):.2f} {wins["inf_count_sum"]["square"]}')
    print(f'Кубический: {np.mean(results["inf_count_sum"]["cube"]):.2f} {wins["inf_count_sum"]["cube"]}')

main()