import numpy as np
from random import random

def Alg(T, N, M, p):
    matrix = [row.copy() for row in T]
    mins = np.zeros((M, N))
    lead = np.zeros(N)
    
    for row in range(M):
        current_row = matrix[row].copy()
        finite_mask = ~np.isinf(current_row)
        
        if not np.any(finite_mask):
            continue
            
        # Модифицированное вычисление с нелинейностью
        Tt = np.full(N, np.inf)
        Tt[finite_mask] = np.power(current_row[finite_mask], p) + np.power(lead[finite_mask], p/2)
        
        min_val = np.min(Tt[finite_mask])
        candidates = np.where((Tt == min_val) & finite_mask)[0]
        
        if len(candidates) == 0:
            continue
            
        ind = candidates[0]
        elem = current_row[ind]
        mins[row][ind] = elem
        lead[ind] = elem
        
        if row < M - 1:
            update_mask = ~np.isinf(matrix[row+1])
            matrix[row+1][update_mask] += lead[update_mask]
    
    if np.all(mins == 0):
        return np.inf
    return int(np.max(np.where(mins != 0, mins, -np.inf).max(axis=0).max()))

def Plotnikov_Zverev(T, N, M):
    matrix = [row.copy() for row in T]
    load = np.zeros(N)
    
    for row in range(M):
        finite_mask = ~np.isinf(matrix[row])
        current_row = matrix[row].copy()
        current_row[~finite_mask] = np.inf
        
        if not np.any(finite_mask):
            continue
            
        min_val = np.min(current_row[finite_mask])
        candidates = np.where((current_row == min_val) & finite_mask)[0]
        
        if len(candidates) == 0:
            continue
            
        ind = candidates[0]
        load[ind] = min_val
        
        if row < M - 1:
            update_mask = ~np.isinf(matrix[row+1])
            matrix[row+1][update_mask] += load[update_mask]
    
    return int(np.max(load)) if np.any(load != 0) else np.inf

def Sort(method: int, matrix):
    if method == 1:
        # Без изменений (исходная матрица)
        return matrix.copy()
    elif method == 2:
        # Сортировка по количеству бесконечностей в строке (по возрастанию)
        inf_counts = np.sum(np.isinf(matrix), axis=1)
        return matrix[np.argsort(inf_counts)]
    elif method == 3:
        # Сортировка сначала по количеству бесконечностей, затем по сумме элементов
        inf_counts = np.sum(np.isinf(matrix), axis=1)
        row_sums = np.array([np.sum(row[np.isfinite(row)]) for row in matrix])
        # Сортируем по возрастанию количества бесконечностей и убыванию суммы
        sort_indices = np.lexsort((-row_sums, inf_counts))
        return matrix[sort_indices]
    return matrix.copy()

def generate_matrix(M, N, min_val, max_val, inf_prob):
    """Генерация матрицы с разными значениями для каждого процессора"""
    base = np.random.randint(min_val, max_val + 1, size=(M, N))
    inf_mask = np.random.random(size=(M, N)) < inf_prob
    return np.where(inf_mask, np.inf, base)

def main():
    np.random.seed(42)  # Фиксируем seed для воспроизводимости
    
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
            
            res_minimax = Plotnikov_Zverev(matrix, N, M)
            res_square = Alg(matrix, N, M, 2)
            res_cube = Alg(matrix, N, M, 3)
            
            results[method]['minimax'].append(res_minimax)
            results[method]['square'].append(res_square)
            results[method]['cube'].append(res_cube)
            
            # Сравниваем только конечные результаты
            valid_results = {
                'minimax': res_minimax,
                'square': res_square,
                'cube': res_cube
            }
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

if __name__ == "__main__":
    main()