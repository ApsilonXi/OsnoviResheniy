import numpy as np

def generate_matrices(M, N, T1, T2):
    matrices = []
    for _ in range(10):
        matrix = np.random.randint(T1, T2 + 1, size=(M, N))
        row_sums = matrix.sum(axis=1)
        matrices.append((matrix, row_sums))
    return matrices

def sort_matrices_by_row_sum(matrices):
    return sorted(matrices, key=lambda x: x[1].sum(), reverse=True)

def cmp_schedule(matrix):
    max_sum = -1
    critical_path = None
    for row in matrix:
        row_sum = sum(row)
        if row_sum > max_sum:
            max_sum = row_sum
            critical_path = row
    return critical_path

def pashkeev_algorithm(matrix, N):
    tasks = sorted(matrix, key=lambda row: sum(row), reverse=True)
    
    processors = [[] for _ in range(N)]
    processor_loads = [0] * N
    
    for task in tasks:
        min_processor_index = processor_loads.index(min(processor_loads))
        processors[min_processor_index].append(task)
        processor_loads[min_processor_index] += sum(task)
    
    return processors, processor_loads

def kron_algorithm(matrix, N):
    M = len(matrix)  # Количество задач
    tasks = [sum(row) for row in matrix]  # Сумма каждой строки матрицы — это сложность задачи
    lower_bound = max(tasks)  # Минимально возможная максимальная нагрузка на процессор (наиболее тяжёлая задача)
    upper_bound = sum(tasks)  # Максимально возможная нагрузка (если все задачи на один процессор)

    def can_distribute_with_max_load(max_load):
        current_load = 0  # Текущая загрузка процессора
        processor_count = 1  # Начинаем с первого процессора

        for task in tasks:
            if current_load + task <= max_load:
                current_load += task  # Добавляем задачу к текущей нагрузке процессора
            else:
                processor_count += 1  # Переходим к следующему процессору
                current_load = task  # Задача назначается новому процессору
                if processor_count > N:
                    return False  # Если процессоров недостаточно, чтобы уложиться в max_load

        return True

    while lower_bound < upper_bound:
        mid_load = (lower_bound + upper_bound) // 2
        if can_distribute_with_max_load(mid_load):
            upper_bound = mid_load  
        else:
            lower_bound = mid_load + 1  
    optimal_max_load = lower_bound
    processors = [[] for _ in range(N)]
    current_load = 0
    current_processor = 0

    for task in tasks:
        if current_load + task <= optimal_max_load:
            processors[current_processor].append(task)
            current_load += task
        else:
            current_processor += 1
            processors[current_processor].append(task)
            current_load = task

    return processors, optimal_max_load

# Главная программа
def main():
    # Ввод данных
    M = int(input("Введите количество процессов (M): "))
    N = int(input("Введите количество процессоров (N): "))
    T1 = int(input("Введите минимальное значение случайного числа (T1): "))
    T2 = int(input("Введите максимальное значение случайного числа (T2): "))

    # 1. Генерация матриц
    matrices = generate_matrices(M, N, T1, T2)

    # 2. Сортировка матриц по убыванию суммы строк
    sorted_matrices = sort_matrices_by_row_sum(matrices)

    # 3. Применение критического пути
    critical_paths = [cmp_schedule(matrix[0]) for matrix in sorted_matrices]

    # 4. Применение алгоритма Пашкеева
    pashkeev_results = [pashkeev_algorithm(matrix[0], N) for matrix in sorted_matrices]

    # 5. Входные данные для алгоритма Крона
    print("Результат алгоритма Крона для отсортированных матриц:")
    for matrix in sorted_matrices:
        result = kron_algorithm(matrix[0], N)
        print("Матрица:")
        for idx, processor in enumerate(result[0]):
            print(f"Процессор {idx + 1}: {list(map(int, processor))}")  # Преобразуем np.int32 в обычные числа
        print(f"Максимальная нагрузка на процессор: {result[1]}")
    
    print("\nРезультат алгоритма Крона для критического пути:")
    for path in critical_paths:
        result = kron_algorithm([path], N)
        print("Критический путь (строка):")
        for idx, processor in enumerate(result[0]):
            print(f"Процессор {idx + 1}: {list(map(int, processor))}")  # Преобразуем np.int32 в обычные числа
        print(f"Максимальная нагрузка на процессор: {result[1]}")
    
    print("\nРезультат алгоритма Крона для алгоритма Пашкеева:")
    for result in pashkeev_results:
        kron_result = kron_algorithm(result[0], N)
        print("Матрица после алгоритма Пашкеева:")
        for idx, processor in enumerate(kron_result[0]):
            print(f"Процессор {idx + 1}: {list(map(int, processor))}")  # Преобразуем np.int32 в обычные числа
        print(f"Максимальная нагрузка на процессор: {kron_result[1]}")

# Запуск программы
if __name__ == "__main__":
    main()

